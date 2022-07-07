"""
An app made in tcod to generate prefabs for my game. 
There are based on zorbus maps but are highly customizable.
Simple controls and complex outputs, furnish levels with details.
Export to json, interact closely with the game
"""
import tcod
import tcod.event
import sys
from prefab_loader import PrefabLoader

#Constants
NUM_KEYS = {
    tcod.event.KeySym.N1: 1,
    tcod.event.KeySym.N2: 2,
    tcod.event.KeySym.N3: 3,
    tcod.event.KeySym.N4: 4,
    tcod.event.KeySym.N5: 5,
    tcod.event.KeySym.N6: 6,
    tcod.event.KeySym.N7: 7,
    tcod.event.KeySym.N8: 8,
    tcod.event.KeySym.N9: 9,
    tcod.event.KeySym.N0: 0,
}

# WIDTH, HEIGHT = 100, 60 # Window width and height in tiles.

def run_console(loader: PrefabLoader):
    WIDTH = loader.room_width
    HEIGHT = loader.room_height

    tileset = tcod.tileset.load_tilesheet(
        "assets/tilesets/zara_graphic.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    font_scale = 2
    with tcod.context.new_terminal(
        rows=HEIGHT * font_scale,
        columns=WIDTH * font_scale,
        tileset=tileset,
        title=f"{loader.room_type} : {loader.room_index} / {loader.len_dict_list_for(loader.room_type)}",
    ) as context:
        console = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:
            console.clear()
            #Render under here
            console.rgb[:,:] = loader.room_to_ndarray()
            #Render above here
            context.present(console)

            for event in tcod.event.wait():
                context.convert_event(event)
                print(event)
                if event.type == "QUIT":
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyboardEvent):
                    if event.sym == tcod.event.K_ESCAPE:
                        raise SystemExit()

def main() -> None:
    loader = PrefabLoader()
    if len(sys.argv) > 1:
        room_type = sys.argv[1]
        room_index = int(sys.argv[2])
    else:
        room_type = input(f"Enter a room type{loader.prefab_collection.keys()}:")
        room_index = int(input(f"Enter a room number {loader.len_dict_list_for(room_type)}:"))

    loader.room_type = room_type
    loader.room_index = room_index
    run_console(loader)

if __name__ == "__main__":
    main()
