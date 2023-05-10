from typing import Generator, Union


CoroutineGenerator = Generator[None, float, Union['CoroutineGenerator', None]]
"""
Generator function that implements a coroutine.  It must always yield None,
and can expect to receive a delta_time float each tick.  It may return
another CoroutineGenerator for trampolining.
"""

def trampoline(generator):
    """
    yield from a generator, and if it returns another generator, yield from that
    one. This allows state machine coroutines to switch states by returning a
    generator for the new state without filling up the call stack of generators.
    """
    while isinstance(generator, Generator):
        generator = yield from generator()
