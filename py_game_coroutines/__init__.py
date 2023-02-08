from __future__ import annotations

from collections.abc import Generator
from typing import cast

CoroutineGenerator = Generator["CoroutineGenerator", float, None]

#
# Features to add:
# Stopping coroutines early
#

class CoroutineManager:
    """
    Own and update zero or more coroutines every frame, disposing of them when
    they're finished.
    """

    _coroutines: list[Coroutine]

    def __init__(self) -> None:
        self._coroutines = []

    def start(self, generator: CoroutineGenerator):
        coroutine = Coroutine(generator)
        self._coroutines.append(coroutine)
        return coroutine

    def update(self, delta_time: float):
        for coroutine in self._coroutines:
            coroutine.update(delta_time)
        # Remove all finished coroutines from the list
        self._coroutines[:] = [c for c in self._coroutines if not c.finished]


class Coroutine:
    __slots__ = ("_stack", "finished")
    _stack: list[CoroutineGenerator]
    finished: bool

    def __init__(self, generator: CoroutineGenerator) -> None:
        self._stack = [generator]
        self.finished = False
        generator.send(cast(float, None))

    def update(self, delta_time: float):
        if self.finished:
            return
        stack = self._stack
        while True:
            # Tick the generator
            try:
                yielded_or_returned_value = stack[-1].send(delta_time)
            except StopIteration as e:
                yielded_or_returned_value = e.value
                stack.pop()
            # If a new generator was yielded or returned, push it onto the execution stack
            if isinstance(yielded_or_returned_value, Generator):
                generator = cast(CoroutineGenerator, yielded_or_returned_value)
                stack.append(generator)
                generator.send(cast(float, None))
            else:
                # Are all generators exhausted?
                if len(stack) == 0:
                    self.finished = True
                # Break the loop, tick again next frame
                break


def wait_for_seconds(seconds: float):
    """
    A coroutine generator function that will do nothing for X seconds, then return.

    Can be yielded from other coroutines to implement a pause / sleep.
    """
    time_elapsed = 0
    while True:
        time_elapsed += yield
        if time_elapsed > seconds:
            return
