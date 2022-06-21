"""
Generates a gamemap object with a set of configurable options
- Perlin Noise
- Cellular Automata (Coming Soonish)
- Prefabs
"""
from __future__ import annotations
import random

import tcod
import tile_types
from numpy import select, ogrid, sqrt
from tcod.noise import Noise
from gamemap import GameMap
from typing import TYPE_CHECKING
from tools import prefab_loader

if TYPE_CHECKING:
    from engine import Engine

def generate_worldmap(engine: Engine, width: int, height: int, seed: int) -> GameMap:
    """Creates the map """
    player = engine.player
    world = GameMap(engine, width, height, entities=[player]) #starts the map as just water tiles

    noise = Noise(
        dimensions = 2,
        hurst = .6, 
        lacunarity = 3.0,
        octaves = 5.0,
        seed = seed, 
    )
    samples = noise[tcod.noise.grid(shape=(width, height), scale=.1, origin=(0,0))]
    #Bound the samples array from 0 <-> 1
    samples = (samples + 1.0) * .5

    #Determines a tile for the .world map by value of parallel noise value
    for x in range(width):
        for y in range(height):
            noise_height = samples[y, x]

            if noise_height >= .45:
                world.tiles[x][y] = tile_types.grass
            elif noise_height >= .3:
                world.tiles[x][y] = tile_types.sand
            else:
                world.tiles[x][y] = tile_types.water

    #Create a circle bool array that masks the island to leave a circle shaped land
    circle_mask = create_circular_mask(height, width, radius=128)
    world.tiles = select(
        condlist=[circle_mask],
        choicelist=[world.tiles],
        default=tile_types.water,
    )

    #I want to iterate every tile and check neighbors for water tiles,
    #if atleast 3 then turn the tile to sand

    world = place_prefabs(world)

    place_player_on_walkable(world, player)
    return world

def place_player_on_walkable(world, player):
    x = 256
    y = 256
    isPlaced = False
    while not isPlaced:
        if not world.tiles[x, y]['walkable']:
            chance = random.random()
            if chance >= .5:
                x += 1
            else:
                y += 1
        else:
            player.place(x, y, world) 
            isPlaced = True
    return world

def create_circular_mask(h, w, center=None, radius=None):
    """Generates a circular mask"""
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = ogrid[:w, :h]
    dist_from_center = sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def cellular_automata_pass(gamemap: GameMap) -> GameMap:
    #DO some cellular stuff here
    return gamemap

def place_prefabs(gamemap: GameMap) -> GameMap:
    prefabs = prefab_loader.load_prefabs()
    loc_x = 230
    loc_y = 256
    for y, row in enumerate(prefabs[439]):
        for x, letter in enumerate(row):
            chance_to_place = random.random()
            if letter == ' ':
                continue
            elif letter == '#':
                if chance_to_place < .05:
                    continue
                gamemap.tiles[x + loc_x][y + loc_y] = tile_types.brown_wall
            elif letter == '.':
                continue

    return gamemap