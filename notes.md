# Ideas

## :white_check_mark:Version Releases
- Working on Version 0.1
- [ ] NPCs and components
    - Capable of performing actions
    - Flexible for monsters, townspeople, quest givers
- [ ] Config files
    - Map size
    - Console size
    - Font
    - Pallette

## Tilesets
- Different tilesets for different environment
    1. Overworld
    2. Caves
    3. ???
- Really need to pick and stick with a tileset which should have:
    1. Small (8x8)
    2. Some graphics (player, frequent *objects*)
    3. Good with 1 color with some shading
    4. Utilize only lower/upper case to make room for sprites
    5. CP437 font page
- Ablity to switch tilesets on demand
    1. Support most DF fonts and make menu setting that lets you switch tilesets

## Prefab Creation
- A way to generate/create prefabs
    1. Need to find way to load in the zorbus maps
    2. Zorbus, load in a few and try to place them on the map if they get placed have a chance to not put a wall to let player in
- A way to place prefabs into map
    1. Place rooms, keep track of entry points, place based off those points and whether or not there is space
    2. However, we have an overworld so it's less important everything connects, we can also place randomly on the map
        - Generate source points on map from perlin noise

## Animations
- Since seeing cogmind's animations, I am very much interested in following suit and incorporating them into the game
- However, I will not I have a decent size list of ideas of what the animations would be and what they could do
- An approach worth taking may be based on a "fire and forget" or having a event driven animation machine that waits for an action to occur and plays the animation
- Also a fair point may be that cool effects can be created outside of animation and in more *hacky* ways

### Animation Ideas
1. Bard plays a music note by his sprite
2. Sprite may flicker between two characters

## :clipboard:Unorganized Notes
- Daily Challenges?
    - What factors are changed
- Character Builds?
    - Stats for different skills
    - Start with a couple
    - Train up your other skills
- Disappearing roofs on building

