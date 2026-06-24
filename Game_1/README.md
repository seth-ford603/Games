Contact seth.ford@comcast.net with any questions.

# DUNGEONGAME
## Current Status

DUNGEONGAME is currently in the core systems prototyping phase. The focus is on validating the underlying game architecture before implementing gameplay systems such as combat, progression, inventory management, and world navigation.

### Completed Systems

* State machine architecture
* Menu and UI framework
* Procedural dungeon generation
* Dungeon rendering
* Room connectivity validation
* Character entity framework
* Character spawning within dungeons
* In-game map overlay
* State stack navigation (push/pop states)

## Architecture Overview

The project is built using Python and Pygame with a state-machine driven architecture.

### Core Components

| Component        | Responsibility                                           |
| ---------------- | -------------------------------------------------------- |
| Game             | Owns the main loop, window, clock, and runtime lifecycle |
| StateManager     | Controls state transitions and state stack operations    |
| GameState        | Base class for all game states                           |
| Button           | Shared UI component for menus and interactions           |
| DungeonFactory   | Creates dungeon instances                                |
| DungeonGenerator | Procedurally generates dungeon layouts                   |
| Dungeon          | Stores rooms, connections, and current location          |
| Room             | Represents individual dungeon nodes                      |
| DungeonRenderer  | Handles dungeon visualization                            |
| Character        | Represents the player's in-game character                |

## State Management

The game uses two forms of state transitions:

### State Replacement

```text
change_state(new_state)
```

Replaces the active state entirely.

Example:

```text
Main Menu → Character Creation → Execution State
```

### State Stack

```text
push_state(new_state)
pop_state()
```

Temporarily places a state on top of another state.

Example:

```text
Execution State
    ↓
Map State
    ↓
Execution State
```

This allows gameplay states to be paused and resumed without recreation.

## Technology

* Python
* Pygame
* Object-Oriented Design
* State Machine Architecture
* Procedural Content Generation

```
```
