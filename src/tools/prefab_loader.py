from typing import List
import numpy as np


def load_prefabs() -> List:
    all_rooms = [] 
    with open("assets/zorbus_vaults/Zorbus_Vaults.txt") as f:
        current_room = np.empty(0, dtype=str, order='F') 
        for line in f.readlines():
            if line.isspace():
                if len(current_room) > 1:
                    current_room = remove_space(current_room)
                    all_rooms.append(current_room)
                    current_room = np.empty(0, dtype=str, order='F') 
                else:
                    current_room = np.empty(0, dtype=str, order='F') 
            else:
                current_room = np.append(current_room, line.rstrip())

    return all_rooms

def remove_space(room: np.ndarray) -> np.ndarray:
    min_spaces =  1000
    for line in room:
        curr_spaces = 0
        for letter in line:
            if letter == ' ':
                curr_spaces += 1
            else:
                break
        min_spaces = curr_spaces if curr_spaces < min_spaces and curr_spaces > 0 else min_spaces
    
    return [line[min_spaces:] for line in room]
