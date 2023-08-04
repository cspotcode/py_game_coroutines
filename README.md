# game_coro

Framework-agnostic coroutines for games in Python.

Features:

* Write logic as a python generator, then tick it every
frame.
* Use `yield` to pause till the next frame
* Pause for a given number of frames or seconds by using helpers


## Usage

**Warning: This library is currently experimental!**

There are no tests and limited few docs. For usage, check out [example/example.py](example/example.py). You can run it by doing the following:

1. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository?tool=desktop)
2. `cd py_game_coroutines`
3. `pip install -e .`
4. `pip install arcade==3.0.0dev23` to install the 3.0 development preview of the [Arcade library](https://github.com/pythonarcade/arcade)
5. `python -m example.example` to run the example


## Design, Behavior

*Note: this section is still somewhat unorganized. Treat it as unfinished notes!*

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
