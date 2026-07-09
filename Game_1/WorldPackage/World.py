"""
Created on 20260703
Updated on 20260709
@author: Seth Ford
"""

import pygame
from WorldPackage.DungeonEntrance import DungeonEntrance


class World:
    def __init__(self, width, height):
        # World starts at 0,0 and extends to the provided width/height
        self.width = width
        self.height = height

        # The playable world boundary
        self.world_rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height
        )
        
        # A list of all dungeon entrances
        # Might not need this later
        self.dungeon_entrances = [
            DungeonEntrance(
                # x/y loc
                self.world_rect.centerx - 40,
                self.world_rect.centery - 200,
                # Size
                80,
                80
            )
        ]

    def get_rect(self):
        return self.world_rect

    def get_spawn_position(self, character):
        # Spawn character in the center of the world
        spawn_x = self.world_rect.centerx - character.width / 2
        spawn_y = self.world_rect.centery - character.height / 2

        return spawn_x, spawn_y
    
    def get_dungeon_entrances(self):
        return self.dungeon_entrances