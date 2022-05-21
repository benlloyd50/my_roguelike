import tcod
import time
import pickle
import lzma
import sys

from os import listdir
from os.path import exists, dirname, abspath 

from mapgenerator import generate_worldmap
from entity import Actor
from engine import Engine

#Constants
WIDTH, HEIGHT = 91, 51  # Console width and height in tiles.
MAP_WIDTH, MAP_HEIGHT = 500, 500 #screen uses 90 x 41, however map is larger
#will fit a 256 diameter circle with padding


def save_game(engine: Engine, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(engine, Engine):
        engine.save_as(filename)
        print("Game saved.")


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    engine._loadname = filename
    print(engine._loadname)
    return engine


def view_save_files():
    DIRECTORY = dirname(abspath(__file__))
    #Preview saves folder
    save_files = listdir(DIRECTORY + "/../saves/")
    for idx, sf in enumerate(save_files):
        name = sf.split(sep='.')[0]
        print(f"{idx + 1}) " + name)

    filename = str(input("Enter a save file name or press [ENTER]: "))
    if filename == "":
        return "" 

    return str(DIRECTORY + "/../saves/" +filename + ".sav")


def main() -> None:
    DIRECTORY = dirname(abspath(__file__))

    # Load the font, a 32 by 8 tile font with libtcod's CP437 character layout.
    tileset = tcod.tileset.load_tilesheet(
        #This is a bit odd since i have to go up a level, may move folders
        DIRECTORY + "/../assets/zara_graphic.png", 16, 16, tcod.tileset.CHARMAP_CP437,
    )
    font_scale = 2 #makes console bigger and thus increase the size of the ascii chars

    if sys.argv[1] == "qs": #Quickstart
        print("Starting new game")

        player = Actor(char=chr(0x263A), color=tcod.yellow, name="Adventurer")
        # bard = Entity(255, 250, 'B', tcod.azure, render_priority=1)

        engine = Engine(player)
        engine.game_map = generate_worldmap(engine, MAP_WIDTH, MAP_HEIGHT, int(time.time()))
        engine.game_map.move_camera_to_player(player.x, player.x)
    else:
        #TODO: Integrate into game console
        filename = view_save_files()

        if exists(path=filename):
            print("Engine loaded successfully")
            engine = load_game(filename=filename)
        else:
            print("Starting new game")

            player = Actor(char=chr(0x263A), color=tcod.yellow, name="Adventurer")
            # bard = Entity(255, 250, 'B', tcod.azure, render_priority=1)

            engine = Engine(player)
            engine.game_map = generate_worldmap(engine, MAP_WIDTH, MAP_HEIGHT, int(time.time()))
            engine.game_map.move_camera_to_player(player.x, player.x)

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
            frame += 1
            engine.render(console=root_console, context=context)
            engine.state_handler.handle_events()
            print(f"{frame = } finished")
        # The window will be closed after the above with-block exits.

if __name__ == "__main__":
    main()
