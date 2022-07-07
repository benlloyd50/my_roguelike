from json import dump, load
from typing import Dict, List, Tuple
from extensions import is_null_or_space
from tcod.console import rgb_graphic
import numpy as np

# PickNewRoom = 1
# NavigateOrJson = 2
# JsonCreation = 3
# Reset = 4

class PrefabLoader:
    room_type: str
    room_index: int

    def __init__(self):
        self.prefab_collection = self.load_prefabs()

    def len_dict_list_for(self, key: str) -> int:
        return len(self.prefab_collection[key]) - 1

    @property
    def room_selected(self) -> list:
        return self.prefab_collection[self.room_type][self.room_index]

    @property
    def room_height(self) -> int:
        return len(self.room_selected)

    @property
    def room_width(self) -> int:
        return len(max(self.room_selected, key=len))

    @property
    def room_types(self) -> str:
        return self.prefab_collection.keys()

    def room_to_ndarray(self) -> np.ndarray:
        room_list = [list(line) for line in self.room_selected]
        room_tiles = np.full((self.room_width, self.room_height), fill_value=np.array((ord(' '), (255, 255, 255), (0, 0, 0)), dtype=rgb_graphic), order="F")
        # room_tiles = np.full((self.room_width, self.room_height), fill_value=tile_types.remove_me, order="F")
        for y, row in enumerate(room_list):
            for x, col in enumerate(row):
                if room_list[y][x] == '#':
                    room_tiles[x, y] = np.array((ord('#'), (255, 255, 255), (0, 0, 0)), dtype=rgb_graphic)
                    # room_tiles[x, y] = tile_types.gray_wall
                elif room_list[y][x] == '.':
                    room_tiles[x, y] = np.array((ord('.'), (105, 105, 105), (0, 0, 0)), dtype=rgb_graphic)
                    # room_tiles[x, y] = tile_types.gray_floor

        return room_tiles

    def char_to_tile(self, char: str) -> np.ndarray:
        return np.array((ord(char), (255, 255, 255), (0, 0, 0)), dtype=rgb_graphic)

    def load_prefabs(self) -> Dict:
        all_rooms = {} 
        with open("assets/zorbus_vaults/Zorbus_Vaults.txt") as f:
            current_room = [] 
            current_list = []
            current_list_name = ""
            for line in f.readlines():
                if line[0] == '?':
                    if len(current_list) > 0:
                        all_rooms[current_list_name] = current_list
                    current_list = []
                    current_list_name = line.lstrip('?').rstrip('\n')
                if line.isspace():
                    if len(current_room) > 1:
                        current_room = self.remove_space(current_room)
                        current_list.append(current_room)
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

    def get_tags(self) -> List:
        tags = input("Enter tag(s) for the level with spaces:")
        if is_null_or_space(tags):
            return self.get_tags()
        return tags.split()

    def get_sourcepoints(self) -> Tuple:
        points = input("Enter source pts as \"xy\":")
        if is_null_or_space(points):
            return self.get_sourcepoints()
        points_tuple = tuple((ord(raw[0]) - 65, int(raw[1:])) for raw in points.split())
        return points_tuple 

    def print_room(room: list) -> None:
        print("y x", end="")
        longest = len(max(room, key=len))
        for i in range(65, longest + 65, 1):
            print(chr(i), end="")
        print("")
        for j, line in enumerate(room):
            print(f"{j:02d} {line}")

# def clear():
#    # for windows
#     if name == 'nt':
#         _ = system('cls')
#    # for mac and linux
#     else:
#         _ = system('clear')
#
# room_index = int(input(f"Enter a room index (max:{max_room_length})"))
# while True:
#     print_room(loaded_rooms[room_type][room_index])
#     print("Would you like to create a json of the selected room?")
#     choice = input(f"J-Json, Go Up-U, Go Down-D, Increment-I={incrementer}").lower()

#     match choice:
#         case "j":
#             create_dungeon(loaded_rooms[room_type][room_index])
#         case "u":
#             room_index += incrementer 
#             clamp(room_index, 0, max_room_length)
#         case "d":
#             room_index -= incrementer 
#             clamp(room_index, 0, max_room_length)
#         case "i":
#             incrementer = input("How fast would you like to scroll up or down >")
#     clear()     
