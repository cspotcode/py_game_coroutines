from typing import Generator, cast
from py_game_coroutines.misc import CoroutineGenerator


class Coroutine:
    __slots__ = ("_generator", "finished")
    _generator: CoroutineGenerator
    finished: bool

    def __init__(self, generator: CoroutineGenerator) -> None:
        # TODO add ability to pass callable that accepts `Context` and returns
        # generator
        self._generator = generator
        self.finished = False

        # Start the generator, running logic up till the first `yield`
        generator.send(None)

    def update(self, delta_time: float):
        """
        Tick the coroutine
        """
        if self.finished:
            return
        gen = self._generator

        # Tick the generator
        try:
            yielded_value = gen.send(delta_time)
            # Report on accidentally yielding values from coroutines
            if yielded_value is not None:
                raise Exception(
                    "Coroutine yielded a value, not None. " +
                    "This may be a mistake, because yielded values are ignored. " +
                    "Did you mean to `yield from other_generator()` or " +
                    "`return other_generator()`?"
                )
        except StopIteration as e:
            returned_value = e.value
            # If a new generator was returned, trampoline to it
            if isinstance(returned_value, Generator):
                self._generator = gen = cast(CoroutineGenerator, returned_value)
                # Trampolining should mimic `yield from` which immediately sends
                # `None`
                gen.send(None)
            else:
                self.finished = True
    
    def stop(self):
        """
        Tell coroutine to stop.
        """
        if self.finished:
            return
        try:
            self._generator.close()
        finally:
            self.finished = True
