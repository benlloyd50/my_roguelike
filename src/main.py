import tcod
import numpy as np # type: ignore

from gamemap import GameMap, water
from entity import Entity
from typing import List

#Constants
WIDTH, HEIGHT = 90, 51  # Console width and height in tiles.
MAP_WIDTH, MAP_HEIGHT = 90, 40 #11 rows for ui down the bottom

MOVECOMMANDS = {
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.d: (1, 0),
}


def main() -> None:
    # Load the font, a 32 by 8 tile font with libtcod's CP437 character layout.
    tileset = tcod.tileset.load_tilesheet(
        "assets/Taffer_huge.png", 16, 16, tcod.tileset.CHARMAP_CP437,
    )

    player = Entity(0, 0, chr(0x263A), tcod.yellow, render_priority=0) 
    bard = Entity(10, 3, 'B', tcod.azure, render_priority=1)

    entities = [player, bard] 

    gamemap = GameMap(MAP_WIDTH, MAP_HEIGHT)

    # Create a window based on this console and tileset.
    with tcod.context.new_terminal(
        WIDTH,
        HEIGHT,
        tileset=tileset,
        title="MyRL",
        vsync=True,
    ) as context:
        root_console = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:  # Main loop, runs until SystemExit is raised.
            root_console.clear() #wipes the console to just black space
            render(entities, root_console, gamemap)
            context.present(root_console)  # Show the console.

            # This event loop will wait until at least one event is processed before exiting.
            # For a non-blocking event loop replace `tcod.event.wait` with `tcod.event.get`.
            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                #print(event)  # Print event names and attributes.
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym in MOVECOMMANDS:
                        player.x += MOVECOMMANDS[event.sym][0]
                        player.y += MOVECOMMANDS[event.sym][1]
                    elif event.sym is tcod.event.KeySym.ESCAPE:
                        raise SystemExit()
        # The window will be closed after the above with-block exits.


def render(entities: List[Entity], console: tcod.Console, gamemap: GameMap):
    #render some sort of map
    #somehow is not the same size??
    gamemap.render(console=console) 
    
    entities = sorted(entities, reverse=True)   #sorts entity by render priority, lowest first
    #probably need to move this sort somewhere else or get a better way to print
    for e in entities:
        #allows bg to be none, so we could take the color of the tile instead
        console.print(e.x, e.y, e.char, fg=e.color)


if __name__ == "__main__":
    main()

