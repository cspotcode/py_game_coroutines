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

    #Disappear
    ctx.reset()
    # For the next 3 seconds, slowly disappear
    while ctx.local_time < 3:
        delta_time = yield
        sprite.alpha -= delta_time*12
        yield
    sprite.alpha = 0

    # Pause for 2 seconds, then reappear
    yield from ctx.wait(2)
    ctx.reset()
    # For the next 3 seconds, slowly reappear
    while ctx.local_time < 3:
        delta_time = yield
        sprite.alpha -= delta_time*12
        yield
    sprite.alpha = 128

    # Pause for 2 seconds, then destroy the sprite
    yield from ctx.wait(2)
    sprite.remove_from_sprite_lists()

sprite = arcade.SpriteSolidColor(20, 20, arcade.color.WHITE)
sprite.position = (50, 300)

manager = game_coro.CoroutineManager()

coroutine = manager.start(animation_coroutine(manager.ctx, sprite))

class Game(arcade.Window):
    def on_update(self, delta_time):
        manager.update(delta_time)
    def on_draw(self):
        self.clear(arcade.color.BLACK)
        sprite.draw()

game = Game()
game.run()