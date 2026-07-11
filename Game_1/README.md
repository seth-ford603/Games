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
* Room-to-room dungeon navigation
* Dead-zone camera
* Area Management System

## Architecture Overview

The project is built using Python and Pygame with a state-machine driven architecture.

### Core Components

| package           | Responsibility                                                    |
| ----------------  | ----------------------------------------------------------------  |
| CharacterPackage  | All components related to characters                              |
| ControllerPackage | All components related to in game event handling                  |
| DungeonPackage    | All components related to dungeon creation                        |
| GamePackage       | All components related to game control like states and interfaces |
| WorldPackage      | All components related to the world outside the dungeon           |

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
