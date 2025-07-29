from typing import Dict

from collections import deque
import threading

import numpy as np


class VideoIngestFragmentMetric:
    """
    Thread-safe rolling statistics tracker for numeric metrics associated with a key.

    Attributes:
        key (str): Logical identifier for the source of the metric (e.g., Camera.id).
        name (str): Name of the metric (e.g., "kafka_consume_age").
        max_items (int): Maximum number of records to retain in the rolling window (default is 100).
    """

    def __init__(self, key: str, name: str, max_items: int = 100):
        self.key = key
        self.name = name
        self._records: deque[float] = deque(maxlen=max_items)
        self._lock = threading.Lock()

    def append(self, value: float):
        """
        Append a new numeric observation to the rolling window.

        Args:
            value (float): New metric value to store.
        """

        if isinstance(value, (int, float)):
            with self._lock:
                self._records.append(float(value))

    def get_stats(self) -> Dict[str, float]:
        """
        Get summary statistics over the current record window.

        Returns:
            Dict[str, float]: Dictionary containing:
                - "avg": Average value.
                - "p99": 99th percentile.
        """

        with self._lock:
            if not self._records:
                return {"avg": 0.0, "p99": 0.0}
            return {
                "avg": float(np.mean(self._records)),
                "p99": float(np.percentile(self._records, 99)),
            }

    def get_avg(self) -> float:
        """
        Return the average of the current metric window.

        Returns:
            float: Average value, or 0.0 if no data is available.
        """

        with self._lock:
            return float(np.mean(self._records)) if self._records else 0.0

    def get_percentile(self, percentile: float) -> float:
        """
        Return the specified percentile of the current metric window.

        Args:
            percentile (float): Percentile to compute (e.g., 99.0).

        Returns:
            float: Computed percentile value, or 0.0 if no data is available.
        """

        with self._lock:
            return float(np.percentile(self._records, percentile)) if self._records else 0.0

    def threshold_exceeded(self, threshold: float) -> bool:
        """
        Check whether the current average value exceeds a threshold.

        Args:
            threshold (float): Threshold to compare against.

        Returns:
            bool: True if the average value exceeds the threshold, False otherwise.
        """

        with self._lock:
            if not self._records:
                return False
            return float(np.mean(self._records)) > threshold

    def __str__(self):
        stats = self.get_stats()
        return f"[{self.key}] {self.name}: avg: {stats['avg']}, p99: {stats['p99']}"
