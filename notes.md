# Ideas

## :white_check_mark:Version Releases
### Working on Version 0.1
- [ ] NPCs and components
    - Capable of performing actions
    - Flexible for monsters, townspeople, quest givers
- [ ] Town generation
    - *See world generation and prefab creation*
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

## World Generation
- See *prefab creation* for more on specifically that
- Town Generation
    - Consists of
        1. Townhouses
        2. Fields
        3. A river/body of water nearby
        4. Walls
        5. Special houses for important people (like mayors or craftsmen)
        6. A townsquare(s)
        7. Shops
    - Made by connecting prefabs in a meaningful way
        1. A townsquare may connect all houses together to shops
        2. Farms closer to townhouses and water
        3. Shops near townsquare
        4. Few special house to keep them special
        5. Craftsmen live near their shops or have a *quick* path
- Less focused on npcs filling the town and simply laying down a town in pleasing patterns

## Prefab Creation
### Prefab Editor (The goal)
- Gets the shape of the room from the zorbusvaults.txt file
- Can pick points or rectangular zones for
    - Entity spawning (items, npcs, enemies)
        - could be chance based 25% for tile to be monster or just 100% for necessary spawns
        - may be specific entity or choose from a list
        - types of entities that could be spawned
    - Possible connection points
    - what tile type to use for each letter in shape

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

