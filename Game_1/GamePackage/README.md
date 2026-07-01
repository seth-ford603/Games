# GamePackage
## Purpose
The GamePackage contains the core runtime architecture for DUNGEONGAME. It is responsible for application startup, game-state management, user interface components, and the main execution loop.

This package serves as the central coordinator for the game and provides the framework that other packages operate within.

## Components
### Game

The Game class serves as the entry point for the application.

### StateManager

Manages all game states and state transitions.

Responsibilities include:

* Routing events to the active state
* Updating the active state
* Drawing the active state
* Managing the state stack

Supported operations:

```python
change_state(new_state)
push_state(new_state)
pop_state()
```

### GameState

Abstract base class used by all game states.

Required methods:

```python
handle_events(events)
update(dt)
draw(screen)
```

All game states inherit from this interface.

### Button

Reusable user interface component used throughout the application.

Provides:

* Button rendering
* Mouse click detection
* Consistent UI behavior across states

### Camera

Responsible for controlling the player's view of the current room.
The camera operates independently of the character and determines which portion of the room is visible on screen.

Key Concepts:
* World Coordinates – The true location of game objects within a room.
* Screen Coordinates – Where those objects are drawn on the player's display.
* Dead-Zone – An invisible rectangle surrounding the player. The camera remains stationary while the player moves inside this area. Once the player reaches an edge, the camera follows until the player is once again inside the dead-zone.

---

## Implemented States

### MainMenuState

Primary application menu.

### CharacterCreationState

Handles character creation and game initialization.

### LoadGameState

Handles save-game loading functionality.

### SettingsState

Provides game configuration options.

### ExecutionState

Primary gameplay state.

### GameMenuState

Pause/menu overlay displayed during gameplay.

### MapState

Dungeon map overlay displayed during gameplay.

---

## State Architecture

The package utilizes a stack-based state machine.

### State Replacement

Used when transitioning between unrelated screens.

Example:

```text
MainMenuState
    ↓
CharacterCreationState
    ↓
ExecutionState
```

### State Overlay

Used when temporarily displaying a state over another state.

Example:

```text
ExecutionState
    ↓
MapState
    ↓
ExecutionState
```

This allows gameplay states to remain active and resume without recreation.

---

## Design Goals

* Clear separation of responsibilities
* Reusable UI components
* Maintainable state-driven architecture
* Support for layered game states
* Easy integration of future gameplay systems
* Minimal coupling between packages

```
```
