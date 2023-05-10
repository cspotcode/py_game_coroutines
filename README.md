# game_coro

Coroutines for games. Write logic as a python generator, then tick it every
frame. Use `yield` to pause till the next frame, or use helpers to pause a given
number of frames or seconds.

This library is currently experimental: no tests, few docs.  For usage, check
out the example: `example/example.py`

Run the example by cloning this repository, then:

```shell
python -m example.example
```

## Design, Behavior

Coroutines should not expect raised exceptions to be swallowed.  
Just like any other call, exceptions will crash the game.

Coroutines can wrap themselves in try-finally to implement cleanup logic.

Coroutines should use `yield from` to delegate to another generator function.

When a coroutine is stopped, generator `.close()` is called.  This follows
standard python rules, where a `GeneratorExit` is raised within the generator.

When coroutine A yields to coroutine B, the return value of B is passed to A.
Any raised exception from B is raised in A.  Just like a normal call stack.

When implementing a state machine, back-and-forth `yield from other_state()`
will eventually fill up the call stack, crashing the game.  Instead,
`return other_state()`.
`return` will close the current generator function, and the coroutine manager
will detect that you've returned another generator and start iterating it.
This only works when returning from your top-level generator.  If in a nested
generator call, use `trampoline()`: `yield from trampoline(other_state())`

## Tips and Tricks

```python
return (yield from self.other())
```

Allows `self.other()` to return a value, which will be returned through
Can trampoline from it.
