"""
Created on 20260608
Updated on 20260710
@author: Seth Ford
"""

import pygame

# DungeonPackage
from DungeonPackage.DungeonFactory import DungeonFactory
from DungeonPackage.DungeonRenderer import DungeonRenderer

# GamePackage
from GamePackage.GameUI import Button
from GamePackage.Camera import Camera

# CharacterPackage
from CharacterPackage.Character import Character

# WorldPackage
from WorldPackage.World import World

# ControllerPackage
from ControllerPackage.WorldController import WorldController
from ControllerPackage.DungeonController import DungeonController

# Main
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT

# Globals
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (180, 255, 180)
BACK_SELECT = 0

def background_selector(screen):
    if BACK_SELECT == 0:
        screen.fill(LIGHT_BLUE)
    else:
        screen.fill(LIGHT_GREEN)

# Abstract class for gamestates
class GameState:
    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

'''
TIGHER ENFORCEMENT
class GameState(ABC):

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass
'''

class MainMenuState(GameState):
    
    def __init__(self, game):
        # Startup
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Main Menu")

        # Create Buttons
        button_width = 250
        button_height = 60
        button_spacing = 20
        num_buttons = 4

        # Vars to help center buttons on screen
        total_height = (button_height * num_buttons) + (button_spacing * (num_buttons-1))
        start_y = (SCREEN_HEIGHT - total_height) // 2
        x = (SCREEN_WIDTH - button_width) // 2

        self.buttons = [
            Button("New Game", x, start_y, button_width, button_height, self.font),
            Button("Load Game", x, start_y + 80, button_width, button_height, self.font),
            Button("Settings", x, start_y + 160, button_width, button_height, self.font),
            Button("Exit Game", x, start_y + 240, button_width, button_height, self.font),
        ]
        
    def handle_events(self, events):
        # Button map
        self.newgame_button =  self.buttons[0] 
        self.loadgame_button = self.buttons[1] 
        self.settings_button = self.buttons[2]   
        self.exit_button =     self.buttons[3]      

        # Parse event queue and handle
        for event in events:
            
            # If New Game button pressed, change to CharacterCreationState
            if self.newgame_button.was_clicked(event):
                self.game.state_manager.change_state(CharacterCreationState(self.game))
            
            # If Load Game button pressed, change to LoadGameState
            if self.loadgame_button.was_clicked(event):
                self.game.state_manager.change_state(LoadGameState(self.game))
            
            # If Settings button pressed, change to SettingsState
            if self.settings_button.was_clicked(event):
                self.game.state_manager.change_state(SettingsState(self.game))
                
            # If Quit button was pressed, quit the game
            if self.exit_button.was_clicked(event):
                self.game.running = False

    def draw(self, screen):
        background_selector(screen)

        for button in self.buttons:
            button.draw(screen)

class SettingsState(GameState):
    
    def __init__(self, game):
        # Startup
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Settings Menu")
        
        # Create Buttons
        button_width = 250
        button_height = 60
        button_spacing = 20
        num_buttons = 3

        # Vars to help center buttons on screen
        total_height = (button_height * num_buttons) + (button_spacing * (num_buttons-1))
        start_y = (SCREEN_HEIGHT - total_height) // 2
        x = (SCREEN_WIDTH - button_width) // 2

        self.buttons = [
            Button("Apply", x, start_y, button_width, button_height, self.font),
            Button("Reset", x, start_y + 80, button_width, button_height, self.font),
            Button("Back", x, start_y + 160, button_width, button_height, self.font),
        ]

    def handle_events(self, events):
        
        global BACK_SELECT
        
        # Button map
        self.apply_button = self.buttons[0]   
        self.reset_button = self.buttons[1]  
        self.back_button =  self.buttons[2]        

        # Parse event queue and handle
        for event in events:
            
            # If Apply button pressed, cycle bg color to simulate actions
            if self.apply_button.was_clicked(event):
                BACK_SELECT = 1 - BACK_SELECT
            
            # If Reset button pressed, cycle bg color to simulate actions
            if self.reset_button.was_clicked(event):
                BACK_SELECT = 1 - BACK_SELECT
                
            # If Back button was pressed, change states to MainMenuState
            if self.back_button.was_clicked(event):
                self.game.state_manager.change_state(MainMenuState(self.game))

    def draw(self, screen):
        background_selector(screen)

        for button in self.buttons:
            button.draw(screen)

class CharacterCreationState(GameState):
    
    def __init__(self, game):
        # Startup
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Character Creation Menu")
        
        # Create Buttons
        button_width = 250
        button_height = 60
        button_spacing = 20
        num_buttons = 3

        # Vars to help center buttons on screen
        total_height = (button_height * num_buttons) + (button_spacing * (num_buttons-1))
        start_y = (SCREEN_HEIGHT - total_height) // 2
        x = (SCREEN_WIDTH - button_width) // 2

        self.buttons = [
            Button("Start Game", x, start_y, button_width, button_height, self.font),
            Button("Reset", x, start_y + 80, button_width, button_height, self.font),
            Button("Back", x, start_y + 160, button_width, button_height, self.font),
        ]

    def handle_events(self, events):
        
        global BACK_SELECT
        
        # Button map
        self.start_button = self.buttons[0]   
        self.reset_button = self.buttons[1]  
        self.back_button =  self.buttons[2]        

        # Parse event queue and handle
        for event in events:
            
            # If start button pressed, navigate to execution state with:
            # Dungeon and charater created in center of the start room
            if self.start_button.was_clicked(event):
                '''# Create dungeon and identify start room
                dungeon = DungeonFactory().create_dungeon()'''
            
                # Create the starting world
                world = World(WORLD_WIDTH, WORLD_HEIGHT)
            
                # Create a new character
                character = Character(0, 0)
            
                # Change states to execution state
                self.game.state_manager.change_state(
                    ExecutionState(self.game, world, character)
                )
            
            # If Reset button pressed, cycle bg color to simulate actions
            if self.reset_button.was_clicked(event):
                BACK_SELECT = 1 - BACK_SELECT
                
            # If Back button was pressed, change states to MainMenuState
            if self.back_button.was_clicked(event):
                self.game.state_manager.change_state(MainMenuState(self.game))

    def draw(self, screen):
        background_selector(screen)

        for button in self.buttons:
            button.draw(screen)


class LoadGameState(GameState):
    
    def __init__(self, game):
        # Startup
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Load Game Menu")
        
        # Create Buttons
        button_width = 250
        button_height = 60
        button_spacing = 20
        num_buttons = 3

        # Vars to help center buttons on screen
        total_height = (button_height * num_buttons) + (button_spacing * (num_buttons-1))
        start_y = (SCREEN_HEIGHT - total_height) // 2
        x = (SCREEN_WIDTH - button_width) // 2

        self.buttons = [
            Button("Load Game", x, start_y, button_width, button_height, self.font),
            Button("Delete", x, start_y + 80, button_width, button_height, self.font),
            Button("Back", x, start_y + 160, button_width, button_height, self.font),
        ]

    def handle_events(self, events):
        
        global BACK_SELECT
        
        # Button map
        self.load_button =   self.buttons[0]   
        self.delete_button = self.buttons[1]  
        self.back_button =   self.buttons[2]        

        # Parse event queue and handle
        for event in events:
            
            # If load game button pressed, navigate to execution state
            if self.load_button.was_clicked(event):
                BACK_SELECT = 1 - BACK_SELECT
            
            # If Reset button pressed, cycle bg color to simulate actions
            if self.delete_button.was_clicked(event):
                BACK_SELECT = 1 - BACK_SELECT
                
            # If Back button was pressed, change states to MainMenuState
            if self.back_button.was_clicked(event):
                self.game.state_manager.change_state(MainMenuState(self.game))

    def draw(self, screen):
        background_selector(screen)

        for button in self.buttons:
            button.draw(screen)

class ExecutionState(GameState):

    def __init__(self, game, world, character):
        # Startup
        self.game = game
        pygame.display.set_caption("Execution State")

        # Shared gameplay objects
        self.character = character
        self.camera = Camera()

        # Begin gameplay in the world
        self.active_controller = WorldController(
            world,
            self.character,
            self.camera
        )
        self.active_controller.enter()

    def handle_events(self, events):

        # Parse event queue and handle
        for event in events:

            # If ESC pressed, push GameMenuState on top of execution state
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.state_manager.push_state(GameMenuState(self.game))

            # If X is pressed while in a dungeon, generate a new dungeon
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                if isinstance(self.active_controller, DungeonController):
                    self.enter_new_dungeon()

            # If M is pressed while in a dungeon, show the dungeon map
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if isinstance(self.active_controller, DungeonController):
                    self.game.state_manager.push_state(
                        MapState(
                            self.game,
                            self.active_controller.dungeon
                        )
                    )

    def update(self, dt):
        self.handle_character_movement(dt)

        # Let the active controller perform area-specific gameplay
        requested_transition = self.active_controller.update(dt)

        # ExecutionState remains responsible for switching controllers
        if requested_transition == "dungeon":
            self.enter_new_dungeon()

    def draw(self, screen):
        background_selector(screen)

        # Draw the current world or dungeon
        self.active_controller.draw(screen)

        # The character remains shared across all controllers
        self.character.draw(screen, self.camera)

    def handle_character_movement(self, dt):
        # Control character with WASD
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.character.move_up(dt)

        if keys[pygame.K_s]:
            self.character.move_down(dt)

        if keys[pygame.K_a]:
            self.character.move_left(dt)

        if keys[pygame.K_d]:
            self.character.move_right(dt)

    def enter_new_dungeon(self):
        # Generate the dungeon data
        dungeon = DungeonFactory().create_dungeon()

        # Replace the active controller
        self.active_controller = DungeonController(
            dungeon,
            self.character,
            self.camera
        )

        # Let the new controller prepare its room, character, and camera
        self.active_controller.enter()
class GameMenuState(GameState):
    
    def __init__(self, game):
        # Startup
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("In Game Menu")
        
        # Create Buttons
        button_width = 250
        button_height = 60
        button_spacing = 20
        num_buttons = 3

        # Vars to help center buttons on screen
        total_height = (button_height * num_buttons) + (button_spacing * (num_buttons-1))
        start_y = (SCREEN_HEIGHT - total_height) // 2
        x = (SCREEN_WIDTH - button_width) // 2

        self.buttons = [
            Button("Resume", x, start_y, button_width, button_height, self.font),
            Button("Main Menu", x, start_y + 80, button_width, button_height, self.font),
            Button("Quit Game", x, start_y + 160, button_width, button_height, self.font),
        ]

    def handle_events(self, events):
        
        global BACK_SELECT
        
        # Button map
        self.resume_button =   self.buttons[0]   
        self.mainmenu_button = self.buttons[1]  
        self.quit_button =     self.buttons[2]        

        # Parse event queue and handle
        for event in events:
            
            # If resume button pressed, pop this state and return to execution state
            if self.resume_button.was_clicked(event):
                pygame.display.set_caption("Execution State")
                self.game.state_manager.pop_state()
            
            # If Main Menu button pressed, go to the main menu
            if self.mainmenu_button.was_clicked(event):
                self.game.state_manager.change_state(MainMenuState(self.game))
                
            # If Quit button was pressed, close game
            if self.quit_button.was_clicked(event):
                self.game.running = False
            
            # If ESC pressed, return to game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.set_caption("Execution State")
                self.game.state_manager.pop_state()

    def draw(self, screen):
        background_selector(screen)

        for button in self.buttons:
            button.draw(screen)

class MapState(GameState):
    
    def __init__(self, game, dungeon):
        # Startup
        self.game = game
        self.dungeon = dungeon
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Map State")

        self.dungeon_renderer = DungeonRenderer(self.game.screen)
        
    def handle_events(self, events):
        
        # Parse event queue and handle
        for event in events:
            # IF key pressed is ESC, pop MenuState off from state stack and return to game
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_m):
                pygame.display.set_caption("Execution State")
                self.game.state_manager.pop_state()

    def draw(self, screen):
        # Clear Screen
        background_selector(screen)
        
        # Retrieve current room
        current_room = self.dungeon.get_current_room()
    
        # Draw the dungeon
        self.dungeon_renderer.draw_connections(self.dungeon)
        self.dungeon_renderer.draw_rooms(self.dungeon, current_room)

