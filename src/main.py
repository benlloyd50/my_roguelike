import tcod
import numpy as np # type: ignore
import time

from mapgenerator import generate_worldmap 
from entity import Entity
from engine import Engine

#Constants
WIDTH, HEIGHT = 90, 51  # Console width and height in tiles.
MAP_WIDTH, MAP_HEIGHT = 90, 40 #11 rows for ui down the bottom


def main() -> None:
    # Load the font, a 32 by 8 tile font with libtcod's CP437 character layout.
    tileset = tcod.tileset.load_tilesheet(
        "assets/zara_graphic.png", 16, 16, tcod.tileset.CHARMAP_CP437,
    )
    font_scale = 2 #makes console bigger and thus increase the size of the ascii chars

    player = Entity(0, 0, chr(0x263A), tcod.yellow, render_priority=0) 
    bard = Entity(10, 3, 'B', tcod.azure, render_priority=1)

    entities = {player, bard} 
    game_map = generate_worldmap(MAP_WIDTH, MAP_HEIGHT, entities, int(time.time()))
    engine = Engine(entities=entities, game_map=game_map, player=player)

    frame = 0
    # Create a window based on this console and tileset.
    with tcod.context.new_terminal(
        WIDTH * font_scale,
        HEIGHT * font_scale,
        tileset=tileset,
        title="MyRL",
        vsync=True,
    ) as context:
        root_console = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:  # Main loop, runs until SystemExit is raised.
            #would be wise to limit frames somehow, so an anim that lasts 20 frames is visible for a bit
            frame += 1
            engine.render(console=root_console, context=context)
            #events are grabbed as they happen and will not hold up the loop so render can be called
            events = tcod.event.get()
            engine.handle_events(events=events, context=context)
            print(f"{frame = } finished")
        # The window will be closed after the above with-block exits.

if __name__ == "__main__":
    main()

