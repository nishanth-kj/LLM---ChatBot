import time
from datetime import datetime, timezone

class TimeUtils:

    @staticmethod
    def now_epoch() -> int:
        return int(time.time())

    @staticmethod
    def now_epoch_ms() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def to_epoch(dt: datetime) -> int:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())

    @staticmethod
    def from_epoch(ts: int) -> datetime:
        return datetime.fromtimestamp(ts, tz=timezone.utc)