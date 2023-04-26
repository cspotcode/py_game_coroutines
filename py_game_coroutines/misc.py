from typing import Generator, Union


CoroutineGenerator = Generator[None, float, Union['CoroutineGenerator', None]]
"""
Generator function that implements a coroutine.  It must always yield None,
and can expect to receive a delta_time float each tick.  It may return
another CoroutineGenerator for trampolining.
"""
