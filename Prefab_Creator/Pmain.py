from __future__ import annotations

from Ploader import PrefabLoader
from Pprefab import Prefab
from Pinput_handler import InputHandler

import numpy as np
import sys
import tcod

WIDTH = 90
HEIGHT = 90


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        path="assets/tilesets/zara_graphic.png",
        rows=16,
        columns=16,
        charmap=tcod.tileset.CHARMAP_CP437,
    )

    # Initialize prefab
    room_index = int(sys.argv[1])
    room_name = sys.argv[2]
    loader = PrefabLoader()
    gamemap = loader.room_to_ndarray(room_index) 
    prefab = Prefab(gamemap=gamemap, name=room_name, source_pts=[], tags=[])
    handler = InputHandler(prefab)

    with tcod.context.new_terminal(
        columns=WIDTH,
        rows=HEIGHT,
        tileset=tileset,
        title="Prefab Creator",
    ) as context:
        console = tcod.Console(width=WIDTH, height=HEIGHT, order="F")
        while True:
            handler.render(console)
            context.present(console)
            
            for event in tcod.event.wait():
                context.convert_event(event)
                print(event)
                handler.handle_event(event)



if __name__ == "__main__":
    main()