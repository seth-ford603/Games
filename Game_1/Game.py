# -*- coding: utf-8 -*-
"""
Created on 20260608
Updated on 20260619
@author: Seth Ford
"""
import sys
import pygame
# GamePackage
from GamePackage.GameStates import MainMenuState
# Main
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT

FPS = 60

# Middle man between Game and States
# Can act as global behavior for states as well
class StateManager:
    # On startup
    def __init__(self, game):
        self.game = game
        self.current_state = MainMenuState(game)

    # Change state
    def change_state(self, new_state):
        self.current_state = new_state
    
    # Event handler for all states
    def handle_events(self, events):
        self.current_state.handle_events(events)

    # Update for all states
    def update(self, dt):
        self.current_state.update(dt)

    # Draw for all states
    def draw(self, screen):
        self.current_state.draw(screen)
    
    # SAVING STATE METHODS
    def push_state(self, new_state):
        new_state.previous_state = self.current_state
        self.current_state = new_state

    def pop_state(self):
        self.current_state = self.current_state.previous_state

    
class Game:
    def __init__(self):
        # Initialize
        pygame.init()

        # Game objects
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Connect state manager
        self.state_manager = StateManager(self)

    def run(self):
        while self.running:
            # self.clock.tick(60) Prevent game from running faster than FPS frames per second - should be 60
            # Divide by 1000 to get dt (delta time: time since last frame)
            # Need this as a scalar for movement
            dt = self.clock.tick(FPS) / 1000.0
            
            # Retrieve all pending events (inputs) and store them in 'events'
            events = pygame.event.get()

            # Parse 'events' for events and act on them
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Pass the events to the state event handler
            self.state_manager.handle_events(events)
            # Execute game logic
            self.state_manager.update(dt)
            # Draw the state to the screen
            self.state_manager.draw(self.screen)

            # Display our hidden canvas to the screen
            pygame.display.flip()

        # Quit
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Create game object
    game = Game()
    # Run the game
    game.run()