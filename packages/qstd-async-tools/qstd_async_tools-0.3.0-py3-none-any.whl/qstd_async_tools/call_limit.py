import asyncio
import functools


class CallQueue:
    def __init__(self, maximum: int):
        self.maximum = maximum
        self.current = 0
        self.queue = asyncio.Queue()

    async def waiting(self):
        if self.current >= self.maximum:
            future = asyncio.Future()
            await self.queue.put(future)
            await future
        else:
            self.current += 1

    def end(self):
        if not self.queue.empty():
            future = self.queue.get_nowait()
            future.set_result(None)
        else:
            self.current -= 1


def call_limit(maximum: int):
    q = CallQueue(maximum)

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
