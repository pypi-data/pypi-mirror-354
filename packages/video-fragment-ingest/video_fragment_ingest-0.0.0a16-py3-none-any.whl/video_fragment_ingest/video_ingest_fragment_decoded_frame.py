from typing import Optional

import time
import numpy as np
import gi

from video_fragment_ingest._generated.models.graph_models_pb2 import Camera

gi.require_version('Gst', '1.0')
from gi.repository import Gst


class DecodedFrame:
    """
    Represents a single decoded video frame, including metadata and raw pixel data.

    Attributes:
        camera (Camera): Metadata about the camera that produced the frame.
        timestamp (float): Presentation timestamp (PTS) of the frame in seconds.
        frame_caps (Gst.Caps): GStreamer capabilities associated with the frame (e.g. resolution, format).
        frame_number (int): Sequential number of the frame in the stream.
        np_frame (np.ndarray): The actual decoded frame data as a NumPy array as RGB.
    """

    def __init__(
            self,
            camera: Camera,
            timestamp: float,
            frame_caps: Gst.Caps,
            frame_number: int,
            np_frame: np.ndarray
    ):
        self.camera = camera
        self.timestamp = timestamp
        self.frame_caps = frame_caps
        self.frame_number = frame_number
        self.np_frame = np_frame

        self._get_resolution()

    def _get_resolution(self):
        """
        Returns the resolution of the frame as a tuple (width, height).
        """
        if self.frame_caps:
            self.width = self.frame_caps.get_structure(0).get_value('width')
            self.height = self.frame_caps.get_structure(0).get_value('height')
        if self.width is None or self.height is None:
            self.height = self.np_frame.shape[0]
            self.width = self.np_frame.shape[1]

    def to_bgr(self) -> Optional[np.ndarray]:
        """
        Converts the RGB frame to BGR format.

        Returns:
            Optional[np.ndarray]: The frame data in BGR format, or None if no frame is available.
        """
        if self.np_frame is None:
            return None

        # Reverse the last dimension (RGB to BGR)
        return self.np_frame[..., ::-1]

    def age(self, reference: Optional[float] = None) -> float:
        """
        Calculates the age of the frame in seconds.

        Args:
            reference Optional(float): Reference time in seconds, if not given 
            uses now (time.time()).

        Returns:
            float: The age of the frame in seconds.
        """

        now = reference if reference is not None else time.time()
        return now - self.timestamp if self.timestamp else 0.0

    def shape(self) -> tuple:
        """
        Returns the shape of the frame as a tuple (height, width, channels).
        """
        return self.np_frame.shape if self.np_frame is not None else (0, 0, 0)
