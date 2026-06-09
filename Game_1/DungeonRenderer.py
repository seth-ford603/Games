# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:18:08 2026

@author: sford
"""

import pygame


class DungeonRenderer:
    # Startup
    def __init__(self, screen):
        self.screen = screen
        
        # Scalars/offsets
        self.tile_size = 40
        self.offset_x = 100
        self.offset_y = 100

        self.room_color = (80, 80, 80)
        self.current_room_color = (120, 160, 255)
        self.connection_color = (200, 200, 200)
        self.border_color = (255, 255, 255)

    def draw(self, dungeon):
        self.draw_connections(dungeon)
        self.draw_rooms(dungeon)

    def draw_rooms(self, dungeon):
        current_room = dungeon.get_current_room()

        # Loop through each room in the dungeon
        for room in dungeon.rooms.values():
            rect = self.get_room_rect(room)

            # Highlight current room
            if room == current_room:
                color = self.current_room_color
            else:
                color = self.room_color
            
            # Draw the squares with their borders
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.border_color, rect, 2)

    def draw_connections(self, dungeon):
        # Empty set to remember which connections have already been drawn
        drawn_connections = set()

        # Loop through every room value in the dungeon
        for room in dungeon.rooms.values():
            start_pos = self.get_room_center(room)

            # Loop through each room connected to this one
            for connected_room in room.connections:
                # Create key of connection and sort it so that we dont have to check for order
                connection_key = tuple(sorted([room.room_id, connected_room.room_id]))

                # Check if the connection has already been drawn
                if connection_key not in drawn_connections:
                    end_pos = self.get_room_center(connected_room)
                    
                    # Draw the line
                    pygame.draw.line(self.screen, self.connection_color, start_pos, end_pos, 3)

                    # Add connection to list of already drawn
                    drawn_connections.add(connection_key)

    def get_room_rect(self, room):
        screen_x = self.offset_x + room.x * self.tile_size
        screen_y = self.offset_y + room.y * self.tile_size
        screen_width = room.width * self.tile_size
        screen_height = room.height * self.tile_size

        return pygame.Rect(screen_x, screen_y, screen_width, screen_height)

    def get_room_center(self, room):
        rect = self.get_room_rect(room)
        return rect.center