# WorldPackage
## Overview

The `WorldPackage` is responsible for representing and rendering the game's world. 
It provides the first playable area the player enters after character creation and serves as the foundation for future towns, routes, points of interest, and dungeon entrances.

## Components
### World
Represents the playable world and defines its boundaries. It is responsible for storing the world dimensions and providing helper methods such as the player's initial spawn position.

### WorldRenderer
Responsible for rendering the world. 
The renderer tiles the `grassy_area.png` texture across the entire world and draws it relative to the camera, allowing the player to freely explore a world much larger than the game window.

### DungeonEntrance
Responsible for detecting when the user enters the dungeon. 
Just a colored rect that can draw itself to the screen and detect collisions.
