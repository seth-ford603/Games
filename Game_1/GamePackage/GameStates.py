"""
Created on 20260608
Updated on 20260702
@author: Seth Ford
"""

import pygame
# DungeonPackage
from DungeonPackage.DungeonFactory import DungeonFactory
from DungeonPackage.DungeonRenderer import DungeonRenderer
from DungeonPackage.Door import Door
from DungeonPackage.RoomRenderer import RoomRenderer
# GamePackage
from GamePackage.GameUI import Button
from GamePackage.Camera import Camera
# CharacterPackage
from CharacterPackage.Character import Character
# Main
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

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
                # Create dungeon and identify start room
                dungeon = DungeonFactory().create_dungeon()
            
                # Create a new character
                character = Character(0, 0)
            
                # Change states to execution state
                self.game.state_manager.change_state(
                    ExecutionState(self.game, dungeon, character)
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
    
    def __init__(self, game, dungeon, character):        
        # Startup
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Execution State")
        
        # Dungeon Init
        self.dungeon = dungeon
        self.dungeon_renderer = DungeonRenderer(self.game.screen)
        self.room_renderer = RoomRenderer("assets/stone_floor.png")
        self.room_border_color = (0, 0, 0)
        
        # Char Init
        self.character = character
        
        # Camera Init
        self.camera = Camera()
        
        # Get start room and its area
        current_room = self.dungeon.get_current_room()
        room_rect = self.get_current_room_rect(current_room)
        
        # Spawn character in center of room
        self.character.x = room_rect.centerx - self.character.width / 2
        self.character.y = room_rect.centery - self.character.height / 2
        
        # Center camera on character at start
        self.camera.update(self.character.get_rect(), room_rect)
        
    def handle_events(self, events):
        
        # Parse event queue and handle
        for event in events:
            # IF key pressed is ESC, push GameMenuState on top of execution state
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.state_manager.push_state(GameMenuState(self.game))
            
            # IF key pressed is X, generate a dungeon
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                self.dungeon = DungeonFactory().create_dungeon()
            
            # If key pressed is M, show the dungeon map
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.game.state_manager.push_state(MapState(self.game, self.dungeon))

    def update(self, dt):
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
    
        # Ensure char stays within walls of room
        current_room = self.dungeon.get_current_room()
        room_rect = self.get_current_room_rect(current_room)
        self.character.keep_inside_rect(room_rect)
        
        # Update camera after character movement
        self.camera.update(self.character.get_rect(), room_rect)
    
    # Get the room dimensions
    # Scale it up for ExecutionState since we are looking at it close up
    # Also center it on the screen
    def get_current_room_rect(self, room):
        room_scale = 14
    
        room_width = room.width * TILE_SIZE * room_scale
        room_height = room.height * TILE_SIZE * room_scale
    
        room_x = (SCREEN_WIDTH - room_width) // 2
        room_y = (SCREEN_HEIGHT - room_height) // 2
    
        return pygame.Rect(
            room_x,
            room_y,
            room_width,
            room_height
        )
    
    # Create/return a list of door objects for the current room.
    # Append the current room_rect for future placment
    def create_doors_for_current_room(self, current_room, room_rect):
        doors = []
    
        for connected_room in current_room.connections:
            door = Door(current_room, connected_room, room_rect)
            doors.append(door)
    
        return doors
    
    # Place the character at a specific position in a room based on the door they entered
    def place_character_after_room_transition(self, entered_door):
        # Get the new room after movement
        current_room = self.dungeon.get_current_room()
        room_rect = self.get_current_room_rect(current_room)
    
        # Distance from the wall after entering the new room
        padding = 30
    
        # Center character horizontally/vertically as needed
        center_x = room_rect.centerx - self.character.width / 2
        center_y = room_rect.centery - self.character.height / 2
    
        # If player exited through a north door,
        # they should appear near the south side of the new room
        if entered_door.direction == "north":
            self.character.x = center_x
            self.character.y = room_rect.bottom - self.character.height - padding
    
        # If player exited through a south door,
        # they should appear near the north side of the new room
        elif entered_door.direction == "south":
            self.character.x = center_x
            self.character.y = room_rect.top + padding
    
        # If player exited through an east door,
        # they should appear near the west side of the new room
        elif entered_door.direction == "east":
            self.character.x = room_rect.left + padding
            self.character.y = center_y
    
        # If player exited through a west door,
        # they should appear near the east side of the new room
        elif entered_door.direction == "west":
            self.character.x = room_rect.right - self.character.width - padding
            self.character.y = center_y
    
        # Move camera to match the character's new position in the new room
        self.camera.update(self.character.get_rect(), room_rect)
    
    # Transitions rooms if a connection is detected
    # The door provided may/may not have a connection attribute defined (future flex)
    def try_enter_door(self, door):
        # Try to move to the room connected to this door
        moved = self.dungeon.move_to_room(door.target_room)
    
        # If the move succeeded, reposition the character
        if moved:
            self.place_character_after_room_transition(door)
    
    def draw(self, screen):
        # Clear screen
        background_selector(screen)
    
        # Get current room and its space(rect)
        current_room = self.dungeon.get_current_room()
        room_rect = self.get_current_room_rect(current_room)
    
        # Draw the room floor
        self.room_renderer.draw_floor(screen, room_rect, self.camera)
        
        # Draw the current room border
        screen_room_rect = self.camera.apply_rect(room_rect)
        pygame.draw.rect(screen, self.room_border_color, screen_room_rect, 4)
    
        # Create doors
        doors = self.create_doors_for_current_room(current_room, room_rect)
        # Draw the doors
        for door in doors:
            door.draw(screen, self.camera)
            
            # If character touches a door, move to the connected room
            # If char tocuhes door rect...
            if self.character.get_rect().colliderect(door.rect):
                # ...attempt to open door
                self.try_enter_door(door)
                # Dont process other doors in loop...break
                break
        
        # Create surface to write room id to screen
        room_text = self.font.render(
            f"Room: {current_room.room_id}",
            True,
            (255, 255, 255)
        )
        # Create surface to write room type to screen
        type_text = self.font.render(
            f"Type: {current_room.room_type}",
            True,
            (255, 255, 255)
        )
        # Write room and type to screen
        screen.blit(room_text, (20, 20))
        screen.blit(type_text, (20, 50))
    
        # Draw the character
        self.character.draw(screen, self.camera)


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

