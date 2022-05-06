"""
Generates a gamemap object with a set of configurable options
"""
import tcod
import tile_types
import random
from tcod.noise import Noise
from gamemap import GameMap
from typing import List 
from entity import Entity


def generate_worldmap(width: int, height: int, entities: List[Entity], seed: int) -> GameMap:
    """Creates the map """
    world = GameMap(width, height, entities) #starts the map as just water tiles

    noise = Noise(
        dimensions = 2,
        hurst = .6, 
        lacunarity = 3.0,
        octaves = 5.0,
        seed = seed, 
    )
    samples = noise[tcod.noise.grid(shape=(width, height), scale=.1, origin=(0,0))]
    # #Bound the samples array from 0 <-> 1
    samples = (samples + 1.0) * .5

    # #Determines a tile for the world map by value of parallel noise value
    for x in range(width):
        for y in range(height):
            noise_height = samples[y, x]

            if noise_height >= .45:
                world.tiles[x][y] = tile_types.grass
            elif noise_height >= .3:
                world.tiles[x][y] = tile_types.sand
            else:
                world.tiles[x][y] = tile_types.water

    return world

def bres_circle(world: GameMap, xc: int, yc: int, radius: int):
    x = 0
    y = radius
    d = 3 - 2 * radius
    world = draw_circle(world, xc, yc, x, y)
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        draw_circle(world, xc, yc, x, y)

    return world


def draw_circle(world: GameMap, xc: int, yc: int, x: int, y: int):
    chance = random.random() 
    #Given a chance can create sort of ruins
    if chance > .9 : world.tiles[xc+x, yc+y] = tile_types.brown_wall 
    if chance > .85 : world.tiles[xc-x, yc+y] = tile_types.brown_wall
    if chance > .8 : world.tiles[xc+x, yc-y] = tile_types.brown_wall
    if chance > .75 : world.tiles[xc-x, yc-y] = tile_types.brown_wall
    if chance > .7 : world.tiles[xc+y, yc+x] = tile_types.brown_wall
    if chance > .65 : world.tiles[xc-y, yc+x] = tile_types.brown_wall
    if chance > .3 : world.tiles[xc+y, yc-x] = tile_types.brown_wall
    if chance > .25 : world.tiles[xc-y, yc-x] = tile_types.brown_wall
    return world