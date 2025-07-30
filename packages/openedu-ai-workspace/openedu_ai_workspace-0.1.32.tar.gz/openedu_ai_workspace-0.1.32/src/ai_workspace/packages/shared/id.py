import time
import threading


class IDGenerator:
    _lock = threading.Lock()
    _last_timestamp = 0
    _sequence = 0

    @classmethod
    def generate(cls):
        with cls._lock:
            timestamp = int(time.time() * 1000)
            if timestamp == cls._last_timestamp:
                cls._sequence += 1
            else:
                cls._sequence = 0
                cls._last_timestamp = timestamp
            return f"{timestamp}{cls._sequence:04d}"
