"""
IntroMenu controls the setup of a new game and loading previously saved games
"""
from __future__ import annotations

import lzma
import pickle
import time
from os import listdir
from os.path import abspath, dirname, exists
from typing import Optional

import tcod

import colors
import state_handlers
from camera import Camera
from engine import Engine
from entity import Actor
from mapgenerator import generate_worldmap

MAP_WIDTH, MAP_HEIGHT = 500, 500 #screen uses 90 x 41, however map is larger
background_image = tcod.image.load(dirname(abspath(__file__)) + "/../assets/images/menu_background.png")[:, :, :3]

def setup_game() -> Engine:
    """Returns an engine set to the default new game settings"""
    player = Actor(char=chr(0x263A), color=tcod.yellow, name="Adventurer")
    # bard = Entity(255, 250, 'B', tcod.azure, render_priority=1)

    engine = Engine(player)
    engine.game_map = generate_worldmap(engine, MAP_WIDTH, MAP_HEIGHT, int(time.time()))

    engine.camera = Camera(81, 31)
    engine.camera.center_on_position(player.x, player.y)

    return engine

def check_saves() -> Optional[Engine]:
    filename = view_save_files()

    if exists(path=filename):
        print("Engine loaded successfully")
        engine = load_game(filename=filename)
        return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    engine.loadname = filename
    print(engine.loadname)
    return engine


def view_save_files():
    directory = dirname(abspath(__file__))
    #Preview saves folder
    save_files = listdir(directory + "/../saves/")
    for idx, save in enumerate(save_files):
        name = save.split(sep='.')[0]
        print(f"{idx + 1}) " + name)

    filename = str(input("Enter a save file name or press [ENTER]: "))
    if filename == "":
        return ""

    return str(directory + "/../saves/" +filename + ".sav")

class MainMenuStateHandler(state_handlers.BaseStateHandler):
    def on_render(self, console: tcod.Console) -> None:
        #Load bg image
        console.draw_semigraphics(background_image, 0, 0)

        #Show menu options
        console.print(
            console.width // 2,
            console.height - 2,
            "By Benjamin Lloyd",
            fg=colors.light_green,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Start a game", "[L] Load a game", "[0] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colors.yellow,
                bg=colors.light_blue,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[state_handlers.BaseStateHandler]:
        if event.sym in (tcod.event.K_0, tcod.event.K_ESCAPE):
            raise SystemExit()
        if event.sym == tcod.event.K_l:
            view_save_files()
        elif event.sym == tcod.event.K_n:
            return state_handlers.MainGameStateHandler(setup_game())
        return None
