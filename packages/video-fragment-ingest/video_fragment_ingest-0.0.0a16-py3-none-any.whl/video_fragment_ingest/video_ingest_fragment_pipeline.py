
from typing import Tuple, Optional

import threading
from concurrent import futures
import queue
from datetime import datetime

import boto3

from ._utils.logging import logger
from ._generated.models.graph_models_pb2 import Camera
from ._generated.models.service_models_pb2 import VideoIngestFragment
from ._gst_mpegts_decoder_pipeline import GstMpegtsDecoderPipeline
from .video_ingest_fragment_decoded_frame import DecodedFrame
from .video_ingest_fragment_metric import VideoIngestFragmentMetric


MINUTE = 60.0


class VideoIngestFragmentPipeline(threading.Thread):
    """
    A threaded (`threading.Thread`) pipeline for ingesting `VideoIngestFragment` messages, downloading the referenced video chunks
    from S3, decoding them into frames, and pushing them to a given output queue.

    The input_queue expects `VideoIngestFragment` messages.

    To start streaming do VideoIngestFragmentPipeline.start().

    Attributes:
        camera_id (str): Identifier for the camera; used to track source and associate metrics.
        output_queue (Queue[DecodedFrame]): Where decoded frames will be pushed.
        metrics_queue (Optional[Queue[VideoIngestFragmentMetric]]): Optional queue where periodic metric snapshots are sent.
    """

    @staticmethod
    def _get_bucket_and_key(s3_uri: str):
        try:
            parts = s3_uri.split('/', 3)
            bucket = parts[2]
            key = parts[3]
            return bucket, key
        except IndexError:
            raise ValueError(f"Invalid S3 URI: {s3_uri}")

    def __init__(
        self,
            camera_id: str,
            output_queue: queue.Queue[DecodedFrame],
            metrics_queue: Optional[queue.Queue[VideoIngestFragmentMetric]] = None
    ):
        super().__init__(daemon=True, name=f"video_fragment_ingest_pipeline_{camera_id}")

        self.camera = Camera(id=camera_id)
        self.input_queue: queue.Queue[VideoIngestFragment] = queue.Queue()
        self.output_queue = output_queue
        self._metrics_queue = metrics_queue

        self._stop_event = threading.Event()

        self._s3_client = boto3.client('s3')

        self._download_executor = futures.ThreadPoolExecutor(max_workers=4)
        self._futures_queue: queue.Queue[Tuple[futures.Future, VideoIngestFragment]] = queue.Queue()

        self._video_task_thread = threading.Thread(target=self._video_task, daemon=True, name=f"video_task_{camera_id}")

        self._camera_not_configured = True
        self.decoder: Optional[GstMpegtsDecoderPipeline] = None

        self.downloaded_frame_age_metric = VideoIngestFragmentMetric(camera_id, "downloaded_frame_age")
        self.input_queue_frame_age_metric = VideoIngestFragmentMetric(camera_id, "input_queue_frame_age")

        self._age_threshold = 10.0
        self._metrics_list = [
            self.downloaded_frame_age_metric,
            self.input_queue_frame_age_metric
        ]

        self._metrics_thread = threading.Thread(
            target=self._metrics_task,
            daemon=True,
            name=f"video_fragment_ingest_metrics_{camera_id}"
        )

    def _metrics_task(self):

        while not self._stop_event.is_set():
            try:
                self._stop_event.wait(MINUTE)

                for metric in self._metrics_list:
                    logger.debug(metric)

                    if metric.threshold_exceeded(self._age_threshold):
                        logger.warning(metric)

                    if self._metrics_queue:
                        self._metrics_queue.put(metric)

                for name, q in [
                    ("input_queue", self.input_queue),
                    ("futures_queue", self._futures_queue),
                ]:
                    if q.qsize() > 1:
                        logger.warning(f"[{self.camera.id}] {name} size: {q.qsize()}")

            except Exception as e:
                logger.exception(f"Error in metrics task for camera {self.camera.id}: {e}")

    def _get_streaming_body(self, msg: VideoIngestFragment):
        try:
            bucket, key = self._get_bucket_and_key(msg.s3_uri)
            response = self._s3_client.get_object(Bucket=bucket, Key=key)
            return response['Body']
        except Exception as e:
            logger.exception(f"Error getting streaming body for {msg.s3_uri}: {e}")
            return None

    def _get_frame_age(self, msg: VideoIngestFragment) -> float:
        try:

            message_timestamp = msg.start_ts.ToDatetime()
            return (datetime.utcnow() - message_timestamp).total_seconds()
        except Exception as e:
            logger.exception(f"Error calculating age for message {msg}: {e}")
            return 0.0

    def _video_task(self):
        while not self._stop_event.is_set():
            try:
                future, msg = self._futures_queue.get_nowait()
            except queue.Empty:
                self._stop_event.wait(0.1)
                continue

            if not self.decoder.ready:
                logger.warning(f"[{msg.camera_id}] Decoder not ready for {msg.s3_uri}")
                self._stop_event.wait(0.1)
                continue

            try:
                body = future.result(timeout=2)
                if not body or not self.decoder:
                    raise ValueError("No body or decoder unavailable")

                chunk = body.read()

                self.decoder.push_chunk(chunk, msg)

                self.downloaded_frame_age_metric.append(self._get_frame_age(msg))

            except futures.TimeoutError:
                logger.warning(f"[{msg.camera_id}] Timeout while waiting for S3 object {msg.s3_uri}")
            except ValueError:
                logger.warning(f"[{msg.camera_id}] Missing data or decoder for {msg.s3_uri}")
            except Exception as e:
                logger.exception(f"[{msg.camera_id}] Unexpected error: {e}")

            self._stop_event.wait(0.1)

    def run(self):
        self._video_task_thread.start()
        self._metrics_thread.start()

        while not self._stop_event.is_set():
            try:
                message = self.input_queue.get_nowait()

                self.input_queue_frame_age_metric.append(self._get_frame_age(message))

                if self._camera_not_configured:
                    self.camera.facility_id = message.facility_id
                    self.camera.customer_id = message.customer_id

                    self.decoder = GstMpegtsDecoderPipeline(
                        camera=self.camera,
                        output_queue=self.output_queue,
                        metrics_queue=self._metrics_queue
                    )
                    self.decoder.start()

                    self._camera_not_configured = False

                future = self._download_executor.submit(self._get_streaming_body, message)
                self._futures_queue.put((future, message))
            except queue.Empty:
                self._stop_event.wait(0.1)

    def stop(self):
        """
        Stop the pipeline and all associated threads.
        """
        self._stop_event.set()
        self._video_task_thread.join(timeout=5)
        self._metrics_thread.join(timeout=5)
        self._download_executor.shutdown(wait=True)

        if self.decoder:
            self.decoder.stop()
            self.decoder.join(timeout=5)

        logger.info(f"Pipeline for camera {self.camera.id} stopped.")
