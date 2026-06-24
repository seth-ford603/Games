# -*- coding: utf-8 -*-
"""
Created on 20260624
Updated on 20260624
@author: Seth Ford
"""

import pygame


class Door:
    # Startup
    def __init__(self, current_room, target_room, room_rect):
        self.current_room = current_room
        self.target_room = target_room

        self.width = 40
        self.height = 40
        self.color = (150, 90, 50)

        self.direction = self.get_direction()
        self.rect = self.create_rect(room_rect)

    # Determine direction of the connection by comparing x/y values
    def get_direction(self):
        dx = self.target_room.center_x - self.current_room.center_x
        dy = self.target_room.center_y - self.current_room.center_y

        if abs(dx) > abs(dy):
            if dx > 0:
                return "east"
            else:
                return "west"

        if dy > 0:
            return "south"
        else:
            return "north"

    # Place the door based on the determined direction
    def create_rect(self, room_rect):

        SCALAR = 30        

        # Determine relative position of target room
        dx = self.target_room.center_x - self.current_room.center_x
        dy = self.target_room.center_y - self.current_room.center_y
    
        # North wall
        if self.direction == "north":
    
            # Door center X = room center X shifted toward the connected room
            door_center_x = room_rect.centerx + (dx * SCALAR)
    
            # Prevent door from leaving the wall
            door_center_x = max(room_rect.left  + self.width // 2, door_center_x)
            door_center_x = min(room_rect.right - self.width // 2, door_center_x)
    
            return pygame.Rect(
                # Door X = calculated center position minus half width
                door_center_x - self.width // 2,
                # Door Y = top wall minus half height
                room_rect.top - self.height // 2,
                # Door Width
                self.width,
                # Door Height
                self.height
            )
    
        # South wall
        if self.direction == "south":
    
            # Door center X = room center X shifted toward the connected room
            door_center_x = room_rect.centerx + (dx * SCALAR)
    
            # Prevent door from leaving the wall
            door_center_x = max(room_rect.left  + self.width // 2, door_center_x)
            door_center_x = min(room_rect.right - self.width // 2, door_center_x)
    
            return pygame.Rect(
                # Door X = calculated center position minus half width
                door_center_x - self.width // 2,
                # Door Y = bottom wall minus half height
                room_rect.bottom - self.height // 2,
                # Door Width
                self.width,
                # Door Height
                self.height
            )
    
        # East wall
        if self.direction == "east":
    
            # Door center Y = room center Y shifted toward connected room
            door_center_y = room_rect.centery + (dy * SCALAR)
    
            # Prevent door from leaving wall
            door_center_y = max(room_rect.top    + self.height // 2, door_center_y)
            door_center_y = min(room_rect.bottom - self.height // 2, door_center_y)
    
            return pygame.Rect(
                # Door X = right wall minus half width
                room_rect.right - self.width // 2,
                # Door Y = calculated center position minus half height
                door_center_y - self.height // 2,
                # Door Width
                self.width,
                # Door Height
                self.height
            )
    
        # West wall
        if self.direction == "west":
    
            # Door center Y = room center Y shifted toward connected room
            door_center_y = room_rect.centery + (dy * SCALAR)
    
            # Prevent door from leaving wall
            door_center_y = max(room_rect.top + self.height // 2, door_center_y)
            door_center_y = min(room_rect.bottom - self.height // 2, door_center_y)
    
            return pygame.Rect(
                # Door X = left wall minus half width
                room_rect.left - self.width // 2,
                # Door Y = calculated center position minus half height
                door_center_y - self.height // 2,
                # Door Width
                self.width,
                # Door Height
                self.height
            )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)