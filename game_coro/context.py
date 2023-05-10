from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .manager import CoroutineManager

class Context:
    __slots__ = ('delta_time', '_manager')
    _manager: CoroutineManager
    delta_time: float
    """
    Duration of current frame
    """
    # unscaled_delta_time: float = 0.0
    # """
    # Duration of current frame, unaffected by time scaling (slow-mo, fast-forward)
    # """

    def __init__(self, manager: CoroutineManager):
        self._manager = manager
        self.delta_time = 0.0

    # @property
    # def unscaled_delta_time(self):
    #     return self.delta_time

    def with_local_time(self):
        """
        Create a new context that tracks local time since creation, with now
        being local_time == 0.
        """
        ctx = ContextWithLocalTime(self._manager)
        self._manager._contexts.add(ctx)
        return ctx
    
    def wait(self, delay: float):
        """
        Wait until a given delay has passed.  If you pass 0, will still wait
        at least a single tick.
        """
        time = 0.0
        yield
        time += self.delta_time
        while time < delay:
            yield
            time += self.delta_time

    def wait_ticks(self, ticks: float):
        """
        Pause the given number of ticks.  Passing 1 is equivalent to not using
        this helper at all, because it will wait a single tick, just like a bare
        `yield` statement.
        """
        for _x in range(ticks):
            yield

class ContextWithLocalTime(Context):
    __slots__ = ('local_time','__weakref__')
    local_time: float
    """
    Time since this context was created
    """

    def __init__(self, manager: CoroutineManager):
        super().__init__(manager)
        self.local_time = 0.0

    def wait_until(self, wait_until_local_time: float):
        """
        Wait until a given `local_time` is reached.
        """
        while self.local_time < wait_until_local_time:
            yield
