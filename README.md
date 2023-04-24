# py_game_coroutines

## Ideas

Pass a `Time` instance into coroutine, it can use for entire lifetime to get `delta_time` and `real_delta_time` values.
Manager will update `Time` each frame before calling into generators.

Expose other niceties on the `Time` instance, like a per-generator lifetime?

Allow coroutines to return values to each other.  Possible if we don't pass `delta_time` via `yield` anymore.

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
