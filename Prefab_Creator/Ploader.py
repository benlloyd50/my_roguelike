"""
Backend for the Prefab Creator
"""
from json import dump, load

import numpy as np

import Ptile_types as tile_types


class PrefabLoader:
    def __init__(self):
        self.prefab_collection = self.load_zorbus_prefabs()    #len = 1336 + 1

    def room_to_ndarray(self, index: int) -> np.ndarray:
        room_list = [list(line) for line in self.prefab_collection[index]]
        height = len(room_list)
        width = len(max(room_list, key=len))
        room_tiles = np.full((width, height), fill_value=tile_types.remove_me, order="F")

        for y, row in enumerate(room_list):
            for x, col in enumerate(row):
                if room_list[y][x] == '#':
                    room_tiles[x, y] = tile_types.gray_wall
                elif room_list[y][x] == '.':
                    room_tiles[x, y] = tile_types.gray_floor

        return room_tiles

    def load_zorbus_prefabs(self) -> list:
        with open("assets/zorbus_vaults/Zorbus_Vaults.txt") as f:
            current_room = [] 
            all_rooms = []
            for line in f.readlines():
                if line.isspace():
                    if len(current_room) > 1:
                        current_room = self.remove_space(current_room)
                        all_rooms.append(current_room)
                        current_room = [] 
                    else:
                        current_room = [] 
                else:
                    current_room.append(line.rstrip())

        return all_rooms

    def remove_space(self, room: list) -> list:
        min_spaces = 1000
        for line in room:
            curr_spaces = 0
            for letter in line:
                if letter == ' ':
                    curr_spaces += 1
                else:
                    break
            min_spaces = curr_spaces if curr_spaces < min_spaces and curr_spaces > 0 else min_spaces

        return [line[min_spaces:] for line in room]

    def create_dungeon_json(name: str, room_layout: list, tags: list, srcpts: list):
        dungeon_map = {
            "name": name, 
            "layout": room_layout,
            "tags": tags,
            "srcpts": srcpts,
        }
        with open(file=f"assets/prefabs/{name}.json", mode='w') as f:
            dump(obj=dungeon_map, indent=4, fp=f)

    def load_existing_copy(name: str) -> dict:
        try:
            with open(file=f"assets/prefabs/{name}.json") as f:
                return load(f)
        except:
            return {}

    # def create_dungeon(room_layout: list):
    #     d_name = input("Enter a name for the level:")
    #     existing = load_existing_copy(d_name)
    #     if existing:
    #         print(f"Current dtags are {existing['tags']}")
    #     d_tags = get_tags()

    #     if existing:
    #         print(f"Current srcpts are {existing['srcpts']}")
    #     d_srcpts = get_sourcepoints()

    #     if existing:
    #         d_tags = d_tags + existing['tags']
    #         d_srcpts = d_srcpts + tuple(existing['srcpts'])

    #     create_dungeon_json(
    #         d_name, 
    #         room_layout, 
    #         d_tags,
    #         d_srcpts
    #     )