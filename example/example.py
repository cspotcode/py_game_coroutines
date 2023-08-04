"""
An example of animation through coroutines using the Arcade framework.

Although your projects can use any framework you'd like, this example
uses the development preview of the Arcade framework. You can install
it by running the following command from the terminal::

    pip install arcade==3.0.0dev23

"""
import math
import game_coro
import arcade


def animation_coroutine(ctx: game_coro.Context, sprite: arcade.Sprite) -> game_coro.CoroutineGenerator:
    # Everything before the first yield runs when you `.start()` it, to setup
    # the routine.
    sprite.alpha = 128

    # Each yield statement will pause the coroutine until the next `.update()`
    yield

    # Spin the sprite for 5 seconds
    time_elapsed = 0.0
    while time_elapsed < 5:
        # For simple cases, receive each frame's delta_time from yield
        delta_time = yield
        sprite.angle += 360 * delta_time
        time_elapsed += delta_time

    # move right 4 px every frame, for the next 60 frames
    for x in range(60):
        sprite.center_x += 4
        # Use yield as a statement
        yield
    
    ctx = ctx.with_local_time()
    start_y = sprite.center_y
    # For the next 3 seconds, bob up and down like a sine wave
    while ctx.local_time < 3:
        sprite.center_y = start_y + math.sin(ctx.local_time * 4 * math.pi) * 50
        yield
    sprite.center_y = start_y

    # Pause for 2 seconds, then destroy the sprite
    yield from ctx.wait(2)
    sprite.remove_from_sprite_lists()


class Game(arcade.Window):

    def __init__(self, width: int = 800,  height: int = 600):
        super().__init__(width=width, height=height)
        # Create a SpriteList to hold and draw the sprites
        self.sprites = arcade.SpriteList()

        # Create a CoroutineManager to tick the coroutine
        self.manager = game_coro.CoroutineManager()

        # Create the sprite we'll animate and add it to the SpriteList
        self.sprite = arcade.SpriteSolidColor(20, 20, arcade.color.WHITE)
        self.sprite.position = (self.width // 2, self.height // 2)
        self.sprites.append(self.sprite)

        # Create the coroutine with the sprite
        self.coroutine = self.manager.start(animation_coroutine(self.manager.ctx, self.sprite))

    def on_update(self, delta_time: float):
        # Tick all coroutines by delta_time
        self.manager.update(delta_time)

    def on_draw(self):
        self.clear()
        self.sprites.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
