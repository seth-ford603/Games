# DungeonPackage

`DungeonPackage` contains the dungeon generation, dungeon data model, room model, and rendering logic for the game.

The package is split into five main files:

- `Room.py` defines individual rooms, including their ID, type, position, size, and connected rooms. Rooms connect to each other bidirectionally.
- 'Door.py' defines a door within a room. A door is an immovable object that lets a user navigate from one room to another using a connection by simply touching it with their character.
- `Dungeon.py` stores the full room collection, tracks the start room/current room, and controls movement between connected rooms.
- `DungeonFactory.py` acts as the entry point for dungeon creation. It creates a `DungeonGenerator` and returns a generated dungeon.
- `DungeonGenerator.py` builds a random dungeon by creating a start room, generating a main path, adding branch rooms, validating spacing/intersections, and assigning a boss room.
- `DungeonRenderer.py` draws the dungeon using Pygame, including room rectangles, room labels, room connections, and a highlight for the current room.

Overall, the package separates dungeon logic from the main game loop. The game asks the factory for a dungeon, the generator builds the dungeon structure, the `Dungeon` object stores and manages that structure, and the renderer displays it on screen.
