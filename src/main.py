"""
Main is the driver and where certain pre loading options will be loaded
such as font and scale.
"""
import tcod

from os.path import dirname, abspath 

import state_handlers
from intromenu import MainMenuStateHandler 

#Constants
WIDTH, HEIGHT = 91, 51  # Console width and height in tiles.

def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "assets/tilesets/zara_graphic.png", 
        16, 16, 
        tcod.tileset.CHARMAP_CP437,
    )
    font_scale = 1 
    frame = 0

    state: state_handlers.BaseStateHandler = MainMenuStateHandler()

    with tcod.context.new_terminal(
        WIDTH * font_scale,
        HEIGHT * font_scale,
        tileset=tileset,
        title="MyRL",
        vsync=True,
    ) as context:
        root_console = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:  
            frame += 1
            root_console.clear()
            state.on_render(console=root_console)
            context.present(root_console)

            for event in tcod.event.wait():
                context.convert_event(event)
                state = state.handle_events(event)
            #print(f"{frame = } finished")

if __name__ == "__main__":
    main()
