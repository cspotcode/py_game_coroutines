from weakref import WeakSet

from .misc import CoroutineGenerator
from .context import Context, ContextWithLocalTime
from .coroutine import Coroutine


class CoroutineManager:
    """
    Own and update zero or more coroutines every frame, disposing of them when
    they're finished.
    """
    __slots__ = ("_coroutines", "ctx", "_contexts")

    _coroutines: list[Coroutine]
    ctx: Context
    """
    Coroutine context, can be passed to generators to give them access to
    time information and helpers for waiting some amount of time or ticks.
    """
    _contexts: WeakSet[ContextWithLocalTime]

    def __init__(self) -> None:
        self._coroutines = []
        self._contexts = WeakSet()
        self.ctx = Context(self)

    def start(self, generator: CoroutineGenerator):
        coroutine = Coroutine(generator)
        self._coroutines.append(coroutine)
        return coroutine

    def update(self, delta_time: float):
        # Update each context with time information
        self.ctx.delta_time = delta_time
        for context in self._contexts:
            context.delta_time = delta_time
            context.local_time += delta_time
        
        # Tick each coroutine
        for coroutine in self._coroutines:
            coroutine.update(delta_time)

        # Remove all finished coroutines from the list
        self._coroutines[:] = [c for c in self._coroutines if not c.finished]

    def stop_all(self):
        """
        Stop all managed coroutines
        """
        for c in self._coroutines:
            c.stop()
        self.coroutines = [c for c in self._coroutines if not c.finished]

    def clear(self):
        self._coroutine = WeakSet()
