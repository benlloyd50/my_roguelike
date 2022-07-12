"""
An external tool for creating map prefabs for my_roguelike
Majority of prefabs are taken from the Zorbus Vault
Allows customization of said prefabs and exports them to json to be used in the game
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

WIDTH, HEIGHT = 80, 90 # Window width and height in tiles.

loader = PrefabLoader()

def run_console(loader: PrefabLoader):
    tileset = tcod.tileset.load_tilesheet(
        "assets/tilesets/zara_graphic.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    gamemap = loader.room_to_ndarray()
    font_scale = 1
    with tcod.context.new_terminal(
        rows=HEIGHT * font_scale,
        columns=WIDTH * font_scale,
        tileset=tileset,
        title="Prefab Editor",
    ) as context:
        console = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:
            console.clear()
            #Render under here
            draw_boxes(console)
            console.print(0, HEIGHT - 2, "Current tool: k")
            x_offset = int((WIDTH - loader.room_width) / 2)
            console.rgb[x_offset : x_offset + loader.room_width, 1 : 1 + loader.room_height] = gamemap['sprite']
            #Render above here
            context.present(console)

            for event in tcod.event.wait():
                context.convert_event(event)
                print(event)
                if event.type == "QUIT":
                    raise SystemExit()
                elif isinstance(event, tcod.event.MouseButtonDown):
                    if event.button == tcod.event.BUTTON_LEFT:
                        x = event.tile.x - x_offset
                        y = event.tile.y - 1
                        if validate_tile(x, y):
                            gamemap[x, y]['sprite']['ch'] = ord("k")
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym == tcod.event.K_ESCAPE:
                        raise SystemExit()
                    if event.sym == tcod.event.KeySym.j: #Down
                        loader.change_room_index(-1)
                        gamemap = loader.room_to_ndarray()
                    if event.sym == tcod.event.KeySym.k: #Up
                        loader.change_room_index(1)
                        gamemap = loader.room_to_ndarray()

def validate_tile(x: int, y: int) -> bool:
    return 0 <= x < loader.room_width and 0 <= y < loader.room_height

def draw_boxes(console: tcod.Console) -> None:
    console.draw_frame(
        x=5,
        y=0,
        width=WIDTH - 10,
        height=66,
    )
    console.print_box(
        x=0,
        y=0,
        width=WIDTH,
        height=1,
        alignment=tcod.CENTER,
        string=f" {loader.room_type} : {loader.room_index} / {loader.len_dict_list_for(loader.room_type)} ",
    )

def main() -> None:
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
