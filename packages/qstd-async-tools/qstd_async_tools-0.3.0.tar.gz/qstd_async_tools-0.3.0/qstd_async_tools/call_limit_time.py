import asyncio
import functools
import typing
from datetime import datetime


class CallQueue:
    current = 0
    maximum: int
    seconds: float
    maximum_in_seconds: int
    next: typing.List[asyncio.Future[None]]
    timestamps: typing.List[float]

    def __init__(self, maximum: int, seconds: float, maximum_in_seconds: int):
        self.maximum = maximum
        self.seconds = seconds
        self.maximum_in_seconds = maximum_in_seconds
        self.next = []
        self.timestamps = []

    @staticmethod
    def _current_timestamp():
        return datetime.now().timestamp()

    def _cleanup_old_timestamps(self):
        current_timestamp = self._current_timestamp()
        while self.timestamps and current_timestamp - self.timestamps[0] > self.seconds:
            self.timestamps.pop(0)

    async def waiting(self):
        while True:
            if self.current >= self.maximum:
                future = asyncio.Future()
                self.next.append(future)
                await future
                continue

            self._cleanup_old_timestamps()

            if len(self.timestamps) == self.maximum_in_seconds:
                first_timestamp = self.timestamps[0]
                current_timestamp = self._current_timestamp()
                if current_timestamp - first_timestamp > self.seconds:
                    self.timestamps.pop(0)
                else:
                    diff = max(self.seconds - (current_timestamp - first_timestamp), 0.1)
                    await asyncio.sleep(diff)
                    continue

            self.current += 1
            self.timestamps.append(self._current_timestamp())
            break

    def end(self):
        if self.next:
            self.next.pop(0).set_result(None)
        self.current -= 1


def call_limit_time(maximum: int, seconds: float, maximum_in_seconds: typing.Optional[int] = None):
    if maximum_in_seconds is None:
        maximum_in_seconds = maximum
    q = CallQueue(maximum, seconds, maximum_in_seconds)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await q.waiting()
            try:
                return await func(*args, **kwargs)
            finally:
                q.end()

        return wrapper

    return decorator
