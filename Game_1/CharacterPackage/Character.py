# -*- coding: utf-8 -*-
"""
Created on 20260623
Updated on 20260623
@author: Seth Ford
"""


import pygame


class Character:
    def __init__(self, x, y):

        # Initialization
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 200
        self.color = (0, 255, 0)

    # Character control
    def move_up(self, dt):
        self.y -= self.speed * dt

    def move_down(self, dt):
        self.y += self.speed * dt

    def move_left(self, dt):
        self.x -= self.speed * dt

    def move_right(self, dt):
        self.x += self.speed * dt

    # Returns a pygame.Rect object representing the character's current position and size on the screen.
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # Prevents the character from moving beyond the walls of a room.
    # If the character attempts to leave the provided boundary rectangle, its position is corrected so that it remains
    # completely inside the room.
    def keep_inside_rect(self, boundary_rect):
        character_rect = self.get_rect()

        if character_rect.left < boundary_rect.left:
            self.x = boundary_rect.left

        if character_rect.right > boundary_rect.right:
            self.x = boundary_rect.right - self.width

        if character_rect.top < boundary_rect.top:
            self.y = boundary_rect.top

        if character_rect.bottom > boundary_rect.bottom:
            self.y = boundary_rect.bottom - self.height

    # Draw the character to the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())