# py_game_coroutines

Run the example with:

```shell
python -m example.example
```

## TODO

Typecheck, including examples, with pyright strict mode and mypy strict mode.
Copy ruff and black configs.
Allow a single coroutine to be ticked manually, w/out a manager?
    Makes the API more complex

Implement `trampoline()`

Think about one-off coroutines
    `ctx` cannot come from manager
    API to create a one-off `ctx`?
    Teach coroutine to update its own `ctx`
    coro = Coroutine(self.boss_behavior) # creates a ctx, passes it to self.boss_behavior

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

## Ideas

Think about coroutine creation.

```python
manager.start(coroutine_fn, arg1, arg2)

# Where
def coroutine_fn(time: Time, arg1, arg2):
    # Wait 3 seconds
    while time.local_time < 3:
      yield
```

How is `time` passed to child coroutines?  Is `start` exposed on the `Time` object, maybe it's a `CoroutineContext` object instead?

```python
def coroutine(ctx: CoroutineContext, arg1, arg2):
    yield ctx.start(other_coroutine)

```

`start()` method can accept either a generator or a callable.  If input is not a generator, will call it expecting to get a generator, passing it a new `ctx` and any args and kwargs.
