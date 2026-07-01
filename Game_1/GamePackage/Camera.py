# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:57:49 2026

@author: sford
"""

import pygame
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    CAMERA_PADDING = 50
    
    def __init__(self):
        # Top-left position of the camera in world coordinates
        self.x = 0
        self.y = 0

        # Invisible center box where the character can move freely
        self.deadzone = pygame.Rect(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 - 100,
            300,
            200
        )

    # How the camera should reposition if the char reaches the edge of the dead zone.
    def update(self, target_rect, boundary_rect):
        # Convert character position from world position to screen position
        target_screen_x = target_rect.x - self.x
        target_screen_y = target_rect.y - self.y

        # If character moves past left side of deadzone, move camera left
        if target_screen_x < self.deadzone.left:
            self.x = target_rect.x - self.deadzone.left

        # If character moves past right side of deadzone, move camera right
        if target_screen_x + target_rect.width > self.deadzone.right:
            self.x = target_rect.right - self.deadzone.right

        # If character moves past top side of deadzone, move camera up
        if target_screen_y < self.deadzone.top:
            self.y = target_rect.y - self.deadzone.top

        # If character moves past bottom side of deadzone, move camera down
        if target_screen_y + target_rect.height > self.deadzone.bottom:
            self.y = target_rect.bottom - self.deadzone.bottom

        # Do not let the camera show space outside the room
        self.keep_inside_rect(boundary_rect)

    def keep_inside_rect(self, boundary_rect):
        padding = self.CAMERA_PADDING
        
        # Camera cannot move left of the room
        if self.x < boundary_rect.left - padding:
            self.x = boundary_rect.left - padding

        # Camera cannot move above the room
        if self.y < boundary_rect.top - padding:
            self.y = boundary_rect.top - padding

        # Camera cannot move right past the room
        if self.x + SCREEN_WIDTH > boundary_rect.right + padding:
            self.x = boundary_rect.right + padding - SCREEN_WIDTH

        # Camera cannot move below the room
        if self.y + SCREEN_HEIGHT > boundary_rect.bottom + padding:
            self.y = boundary_rect.bottom + padding - SCREEN_HEIGHT

    def apply_rect(self, rect):
        # Convert a world rect into a screen rect
        return pygame.Rect(
            rect.x - self.x,
            rect.y - self.y,
            rect.width,
            rect.height
        )