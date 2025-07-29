

from typing import Optional, Dict, Any, Tuple

import time
import queue
import threading

import numpy as np
import gi
import pyds

from ._utils.logging import logger
from ._generated.models.graph_models_pb2 import Camera
from ._generated.models.service_models_pb2 import VideoIngestFragment
from .video_ingest_fragment_decoded_frame import DecodedFrame
from .video_ingest_fragment_metric import VideoIngestFragmentMetric


gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)


class GstMpegtsDecoderPipeline(threading.Thread):

    timestamp_caps = Gst.Caps.from_string("timestamp/x-unix")

    @staticmethod
    def _create_element(element: str, name: str, properties: Optional[Dict[str, Any]] = None) -> Gst.Element:
        """Create a Gst.Element.

        If it fails, logs error, and return None.

        Args:
            element_name (str): Gst element name.
            element_id (str): Element unique identifier.

        Returns:
            Gst.Element: Gst element object. (None if failed)
        """
        gst_elem = Gst.ElementFactory.make(element, name)
        if gst_elem is None:
            raise ValueError(f"Failed to create GStreamer element '{element}' with name '{name}'.")
        if properties:
            for prop, value in properties.items():
                gst_elem.set_property(prop, value)
        return gst_elem

    @staticmethod
    def _link_static(src_pad, dst_pad):
        """
        Helper to link two static pads and log the outcome.
        If linking fails, log an error and quit the main loop.
        """

        result = src_pad.link(dst_pad)
        if result != Gst.PadLinkReturn.OK:
            raise Exception(f"Failed to link {src_pad.get_name()} with {dst_pad.get_name()}. Result: {result}")

    @staticmethod
    def _link_elements(src, sink):
        if not src.link(sink):
            raise Exception(f"Failed to link {src.get_name()} to {sink.get_name()}")

    def __init__(
        self,
        camera: Camera,
        output_queue: queue.Queue[DecodedFrame],
        metrics_queue: Optional[queue.Queue[Dict[str, Dict[str, float]]]] = None,
        output_fps: int = -1,
        fps_agg_interval: int = 60,
        save_decoded_frame: bool = False,
    ):

        super().__init__(daemon=True, name=f"mpegts_decoder_{camera.id}")

        self.camera = camera
        self.output_queue = output_queue
        self.metrics_queue = metrics_queue
        self._output_fps = output_fps
        self._fps_agg_interval = fps_agg_interval
        self._save_decoded_frame = save_decoded_frame

        self._capsfilter_string = "video/x-raw(memory:NVMM), format=RGB"

        self._stop_event = threading.Event()
        self._ready_event = threading.Event()
        self._frame_number = 0
        self._total_frames_in_interval = 0
        self._frames_in_chunk = 0
        self._first_pts = 0
        self._last_pts = 0

        self.decoded_frame_age_metric = VideoIngestFragmentMetric(camera.id, "decoded_frame_age")
        self.emitted_frame_age_metric = VideoIngestFragmentMetric(camera.id, "emitted_frame_age")

        self.metrics_list = [
            self.decoded_frame_age_metric,
            self.emitted_frame_age_metric,
        ]

        self._reference_pts_lock = threading.Lock()
        self._reference_pts: Optional[int] = None

    def _frame_age(self, buffer_pts) -> float:
        return time.time() - (buffer_pts / Gst.SECOND)

    def _handle_bus_element(self, message, loop):
        # (Optional) Process element messages if needed.
        pass

    def _handle_bus_eos(self, message, loop):
        logger.warning(f"[{self.camera.id}] MPEGTSDecoder End-of-stream")
        # loop.quit()

    def _handle_bus_warning(self, message, loop):
        err, debug = message.parse_warning()
        logger.warning(f"[{self.camera.id}] MPEGTSDecoder Warning: {err}: {debug}")

    def _handle_bus_error(self, message, loop):
        err, debug = message.parse_error()
        logger.error(f"[{self.camera.id}] MPEGTSDecoder Error: {err}: {debug}")
        loop.quit()

    def _bus_callback(self, bus, message, loop) -> bool:
        try:
            t = message.type
            if t == Gst.MessageType.EOS:
                self._handle_bus_eos(message, loop)
            elif t == Gst.MessageType.WARNING:
                self._handle_bus_warning(message, loop)
            elif t == Gst.MessageType.ERROR:
                self._handle_bus_error(message, loop)
            elif t == Gst.MessageType.ELEMENT:
                self._handle_bus_element(message, loop)
        except Exception as e:
            logger.exception(f"[{self.camera.id}] Exception in bus callback: {e}")
        return True

    def _on_first_buffer(self, pad, info):
        print("On first buffer callback")

        # caps = pad.get_current_caps()
        # if not caps:
        #     logger.error(f"[{self.camera.id}] No caps on pad {pad.get_name()}")
        #     return Gst.PadProbeReturn.OK

        # logger.info(f"[{self.camera.id}] >>>>>>>>>>>>>>>>>> First buffer caps: {caps}")
        return Gst.PadProbeReturn.REMOVE

    def _create_parser_elements_with_caps(self, caps_string: str) -> Tuple[Gst.Element, Gst.Element]:
        codec = "h264"  # Default codec
        if "h264" in caps_string:
            codec = "h264"
        elif "h265" in caps_string or "hevc" in caps_string:
            codec = "h265"
        else:
            logger.error(f"[{self.camera.id}] Unsupported codec in caps: {caps_string}")
            self.loop.quit()

        self.camera.encoding = codec

        parser = self._create_element(f"{codec}parse", f"{self.camera.id}_{codec}_parse")

        parser_filter = self._create_element(
            element="capsfilter",
            name=f"{self.camera.id}_{codec}_capsfilter",
            properties={
                "caps": Gst.Caps.from_string(f"video/x-{codec}, stream-format=byte-stream, alignment=au")
            }
        )
        return parser, parser_filter

    def _attach_sink_elements(self):

        sink_elements = [self.inter_queue_2, self.decoder, self.videoconvert, self.capsfilter, self.appsink]
        for elem in sink_elements:
            self._pipeline.add(elem)
            elem.sync_state_with_parent()

        self._link_elements(self.parser_filter, self.inter_queue_2)
        self._link_elements(self.inter_queue_2, self.decoder)
        self._link_elements(self.decoder, self.videoconvert)

        if self._output_fps > 0:

            self.videorate = self._create_element(
                element="videorate",
                name=f"{self.camera.id}_videorate",
            )

            cap_string = self._capsfilter_string + f", framerate={self._output_fps}/1"

            self.capsfilter.set_property("caps", Gst.Caps.from_string(cap_string))

            self._pipeline.add(self.videorate)
            self.videorate.sync_state_with_parent()

            self._link_elements(self.videoconvert, self.videorate)
            self._link_elements(self.videorate, self.capsfilter)
        else:
            self._link_elements(self.videoconvert, self.capsfilter)
            self._link_elements(self.capsfilter, self.appsink)

    def _on_demux_pad_added(self, demuxer, src_pad, _):

        cap_string = src_pad.query_caps(None).to_string()
        logger.info(f"[{self.camera.id}] Received new pad '{src_pad.get_name()}' from '{demuxer.get_name()}':\n\t{cap_string}")
        if not cap_string.startswith("video/"):
            logger.error(f"[{self.camera.id}] Unsupported caps: {cap_string}")
            return

        self.parser, self.parser_filter = self._create_parser_elements_with_caps(cap_string)

        if not self.parser:
            return

        for elem in [self.parser, self.parser_filter]:
            self._pipeline.add(elem)
            elem.sync_state_with_parent()

        self._link_static(src_pad, self.inter_queue.get_static_pad("sink"))

        self._link_elements(self.inter_queue, self.parser)
        self._link_elements(self.parser, self.parser_filter)

        self._attach_sink_elements()

    def _decoded_to_cpu(
        self,
        buffer: Gst.Buffer,
    ) -> Optional[np.ndarray]:
        try:
            n_frame = pyds.get_nvds_buf_surface(hash(buffer), 0)
            output_frame = np.array(n_frame, copy=True, order='C')
        except Exception as e:
            logger.error(f"[{self.camera.id}] Error converting buffer to NumPy array: {e}")
            return None

        return output_frame

    def _get_frame_timestamp(self, buffer_pts: int, chunk_start_ts: float) -> float:
        if not self._reference_pts:
            logger.warning(f"[{self.camera.id}] No reference PTS set, using current buffer PTS as reference.")
            self._reference_pts = buffer_pts
            offset = 0.0
        else:
            offset = (buffer_pts - self._reference_pts) / Gst.SECOND

        return chunk_start_ts + offset

    def _on_new_sample(self, appsink):

        sample = appsink.emit("pull-sample")
        if sample:
            buff = sample.get_buffer()
            caps = sample.get_caps()

            if not buff or not caps or buff.pts == Gst.CLOCK_TIME_NONE:
                logger.error(f"[{self.camera.id}] No buffer or caps or pts in sample")
                return Gst.FlowReturn.ERROR

            is_key_frame = bool((buff.get_flags() & Gst.BufferFlags.HEADER))

            if is_key_frame:
                if self._first_pts is not None and self._frames_in_chunk > 0:
                    duration = (self._last_pts - self._first_pts) / Gst.SECOND
                    logger.debug(f"[{self.camera.id}] Frames in chunk: {self._frames_in_chunk}, duration: {duration:.2f} seconds")
                # Reset tracking for new GOP
                self._first_pts = buff.pts
                self._frames_in_chunk = 1  # count this keyframe

                # NOTE: Only check first frame age, because the gop duration will impact the metric
                self.decoded_frame_age_metric.append(self._frame_age(buff.pts))
            else:
                self._frames_in_chunk += 1
            self._last_pts = buff.pts

            logger.debug(f"[{self.camera.id}] Received new frame with PTS: {buff.pts / Gst.SECOND}, is_key_frame: {is_key_frame}")

            frame_timestamp = buff.pts / Gst.SECOND
            np_frame = self._decoded_to_cpu(buff)

            self.output_queue.put(
                DecodedFrame(
                    camera=self.camera,
                    timestamp=frame_timestamp,
                    frame_caps=caps,
                    frame_number=self._frame_number,
                    np_frame=np_frame,
                )
            )
            self._total_frames_in_interval += 1
            self._frame_number += 1

            return Gst.FlowReturn.OK
        return Gst.FlowReturn.ERROR

    def _create_elements(self):

        self._pipeline = Gst.Pipeline.new(f"{self.camera.id}_mpegts_decoder_pipeline")

        mpegts_caps = Gst.Caps.from_string("video/mpegts, systemstream=(boolean)true, packetsize=(int)188")

        self.appsrc = self._create_element(
            element="appsrc",
            name=f"{self.camera.id}_src",
            properties={
                "is-live": True,
                "block": False,
                "format": Gst.Format.TIME,
                "caps": mpegts_caps,
                "emit-signals": True,
                "do-timestamp": False,
                "automatic-eos": False,
            }
        )

        self.tsparse = self._create_element(
            element="tsparse",
            name=f"{self.camera.id}_tsparse",
            properties={
                "alignment": 7,  # 7 means 188 bytes alignment
            }
        )

        self.demuxer = self._create_element(
            element="tsdemux",
            name=f"{self.camera.id}_tsdemux",
        )

        self.demuxer.connect("pad-added", self._on_demux_pad_added, None)

        # Queues to dynamically build the pipeline

        self.inter_queue = self._create_element(
            element="queue",
            name=f"{self.camera.id}_input_queue"
        )

        self.inter_queue_2 = self._create_element(
            element="queue",
            name=f"{self.camera.id}_inter_queue_2",
        )

        self.decoder = self._create_element(
            element="nvv4l2decoder",
            name=f"{self.camera.id}_decoder",
        )

        mem_type = int(pyds.NVBUF_MEM_CUDA_UNIFIED)
        self.videoconvert = self._create_element(
            element="nvvideoconvert",
            name=f"{self.camera.id}_videoconvert",
            properties={
                "nvbuf-memory-type": mem_type
            }
        )

        self.capsfilter = self._create_element(
            element="capsfilter",
            name=f"{self.camera.id}_capsfilter",
            properties={
                "caps": Gst.Caps.from_string(self._capsfilter_string)
            }
        )

        self.appsink = self._create_element(
            element="appsink",
            name=f"{self.camera.id}_appsink",
            properties={
                "emit-signals": True,
                "sync": False,
            }
        )

        self.appsink.connect("new-sample", self._on_new_sample)

        for elem in [self.appsrc, self.demuxer, self.inter_queue]:
            self._pipeline.add(elem)

        self._link_elements(self.appsrc, self.demuxer)
        # The demuxer ! inter_queue linking is handled dynamically in _on_demux_pad_added.

        GLib.timeout_add_seconds(self._fps_agg_interval, self._health_check)

        queue_src_pad = self.inter_queue.get_static_pad("src")
        queue_src_pad.add_probe(Gst.PadProbeType.BUFFER, self._on_first_buffer)

        self.bus = self._pipeline.get_bus()
        self.bus.add_signal_watch()
        self.loop = GLib.MainLoop()
        self.bus.connect("message", self._bus_callback, self.loop)

    def _health_check(self):

        decoded_fps = 0.0
        if self._total_frames_in_interval > 0:
            decoded_fps = round(self._total_frames_in_interval / self._fps_agg_interval, 2)
            self._total_frames_in_interval = 0
        appsrc_level_time = round(self.appsrc.get_property("current-level-time") / Gst.SECOND, 2)

        for metric in self.metrics_list:
            logger.debug(metric)

            if metric.threshold_exceeded(10.0):
                logger.warning(metric)

            if self.metrics_queue:
                self.metrics_queue.put(metric)

        logger.debug(f"[{self.camera.id}] Decoded FPS: {decoded_fps}, Appsrc Level Time: {appsrc_level_time}")

        return True

    def run(self):
        """
        Run the pipeline until a stop signal is received.
        """
        self._ready_event.clear()
        while not self._stop_event.is_set():
            try:
                self._create_elements()
                self._pipeline.set_state(Gst.State.PLAYING)
                self._ready_event.set()
                self.loop.run()
            except Exception as e:
                logger.error(f"[{self.camera.id}] Error in MPEGTSDecoder: {e}")
                self._stop_event.wait(1)
            finally:
                self._pipeline.set_state(Gst.State.NULL)
                self._stop_event.wait(3)
                self._ready_event.clear()

    def push_chunk(self, chunk: bytes, video_fragment_msg: VideoIngestFragment):

        if not self.ready:
            logger.warning(f"[{self.camera.id}] Decoder not ready, cannot push chunk")
            return

        duration = int(video_fragment_msg.duration * Gst.SECOND)
        start_ts_sec = video_fragment_msg.start_ts.ToDatetime().timestamp()
        start_pts = int(start_ts_sec * Gst.SECOND)

        self.appsrc.set_property("blocksize", len(chunk))

        buf = Gst.Buffer.new_allocate(None, len(chunk), None)
        buf.fill(0, chunk)

        buf.pts = start_pts
        buf.dts = start_pts
        buf.duration = duration

        logger.debug(f"[{self.camera.id}] Pushing buffer: PTS={buf.pts / Gst.SECOND}, duration={buf.duration / Gst.SECOND}")

        ret = self.appsrc.emit("push-buffer", buf)
        if ret != Gst.FlowReturn.OK:
            logger.error(f"[{self.camera.id}] push-buffer returned {ret}")

        self.emitted_frame_age_metric.append(self._frame_age(buf.pts))

    def stop(self):
        """
        Signal the decoder to stop gracefully.
        """
        self.loop.quit()
        self._stop_event.set()
        self.appsrc.emit("end-of-stream")
        self._pipeline.set_state(Gst.State.NULL)

    def wait_for_ready(self, timeout: Optional[float] = None) -> bool:
        """
        Wait until the pipeline is ready to process data.

        Args:
            timeout (Optional[float]): Maximum time to wait for the pipeline to be ready.

        Returns:
            bool: True if the pipeline is ready, False if it times out.
        """
        return self._ready_event.wait(timeout)

    @property
    def ready(self) -> bool:
        """
        Check if the pipeline is ready to process data.
        """
        return self._ready_event.is_set()
