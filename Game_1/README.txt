DUNGEONGAME Architecture Summary

The game currently uses a Python/Pygame state-machine architecture. The main program owns the game window, clock, main loop, and StateManager. The StateManager controls which state is currently active and forwards events, updates, and draw calls to that state.

Core Runtime Flow:
1. Game initializes Pygame, creates the screen, clock, and StateManager.
2. The main loop collects Pygame events every frame.
3. Window close events set game.running to False.
4. Events are passed to the StateManager.
5. The active state handles input, updates, and draws itself.
6. pygame.display.flip() presents the completed frame.

Main Classes:
- Game: owns the window, clock, running flag, and main loop.
- StateManager: owns the current state and handles state transitions.
- GameState: base class/interface for all game states.
- Button: reusable UI component for rendering and click detection.

Implemented States:
- MainMenuState
  - Buttons: New Game, Load Game, Settings, Exit Game
  - Routes to CharacterCreationState, LoadGameState, SettingsState, or exits the game.

- SettingsState
  - Buttons: Apply, Reset, Back
  - Apply/Reset currently toggle the background color as temporary test behavior.
  - Back returns to MainMenuState.

- CharacterCreationState
  - Buttons: Start Game, Reset, Back
  - Start Game enters ExecutionState.
  - Reset toggles the background color as temporary test behavior.
  - Back returns to MainMenuState.

- LoadGameState
  - Buttons: Load Game, Delete, Back
  - Load Game enters ExecutionState.
  - Delete toggles the background color as temporary test behavior.
  - Back returns to MainMenuState.

- ExecutionState
  - Main gameplay state.
  - No buttons currently.
  - Pressing Esc pushes GameMenuState on top of ExecutionState instead of replacing it.

- GameMenuState
  - Buttons: Resume, Main Menu, Quit Game
  - Resume pops GameMenuState and returns to the same ExecutionState instance.
  - Main Menu replaces the current state with MainMenuState.
  - Quit Game stops the program.

State Transition Design:
- change_state(new_state): replaces the current state.
- push_state(new_state): temporarily places a new state over the current one.
- pop_state(): returns to the previous state.

This allows ExecutionState to be paused and resumed without being recreated.

UI Design:
- Buttons are centralized in GameUI.py.
- Each state creates its own buttons but reuses the shared Button class for consistent drawing and click behavior.

Temporary Test Behavior:
- BACK_SELECT is a global flag used to toggle between light blue and light green backgrounds.
- background_selector(screen) fills the screen based on the current BACK_SELECT value.