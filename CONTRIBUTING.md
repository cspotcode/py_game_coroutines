This doc doesn't have any contributing guidance right now, just my to-do list.

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

Pausing?
- Pausable routine should have pausable `ctx`
- `manager.start_pausable()`?
- If root `ctx` creates child `ctx`, do they all pause at once?
- Why not `ctx = ctx.create_local()`?  B/c then can't pause the routine externally, can't do `my_coro.pause()`

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
