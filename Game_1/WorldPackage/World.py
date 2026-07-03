"""
Created on 20260703
Updated on 20260703
@author: Seth Ford
"""

import pygame


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

    def get_rect(self):
        return self.world_rect

    def get_spawn_position(self, character):
        # Spawn character in the center of the world
        spawn_x = self.world_rect.centerx - character.width / 2
        spawn_y = self.world_rect.centery - character.height / 2

        return spawn_x, spawn_y