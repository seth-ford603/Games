# ControllerPackage

## Purpose

The `ControllerPackage` contains the gameplay controllers responsible for coordinating player interaction within each playable area. 
Controllers sit between `ExecutionState` and the underlying game objects, keeping area-specific gameplay logic separate from game-state management.

## Responsibilities

* Manage area-specific gameplay updates
* Coordinate rendering for the active area
* Handle player spawning and boundaries
* Process area interactions (doors, dungeon entrances, etc.)
* Request transitions between gameplay areas

## Classes
### `AreaController`
Abstract base class defining the common interface shared by all gameplay controllers.

### `WorldController`
Controls gameplay while the player is exploring the world.

Unique Responsibilities include:
* World updates
* World rendering
* Dungeon entrance detection

### `DungeonController`
Controls gameplay while the player is inside a dungeon.

Responsibilities include:
* Room management
* Door creation and collision
* Room transitions
* Dungeon rendering
