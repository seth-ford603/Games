# -*- coding: utf-8 -*-
"""
Created on 20260709
Updated on 20260709
@author: Seth Ford
"""

import pygame


class DungeonEntrance:
    def __init__(self, x, y, width, height):
        # Entrance position and size in world coordinates
        self.rect = pygame.Rect(x, y, width, height)

        # Temporary visual settings
        self.color = (160, 150, 130)
        self.border_color = (0, 0, 0)
        self.border_width = 3

    def is_touched_by(self, character):
        # Collision uses world coordinates
        return self.rect.colliderect(character.get_rect())

    def draw(self, screen, camera):
        # Convert entrance rect from world coordinates to screen coordinates
        screen_rect = camera.apply_rect(self.rect)

        # Draw entrance
        pygame.draw.rect(screen, self.color, screen_rect)
        pygame.draw.rect(screen, self.border_color, screen_rect, self.border_width)