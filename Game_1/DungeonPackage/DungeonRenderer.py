# -*- coding: utf-8 -*-
"""
Created on 20260609
Updated on 20260619
@author: Seth Ford
"""

import pygame
from GameConfig import TILE_SIZE, DUNGEON_OFFSET_X, DUNGEON_OFFSET_Y

class DungeonRenderer:
    # Startup
    def __init__(self, screen):
        self.screen = screen
        
        # Font support
        self.font = pygame.font.SysFont(None, 20)
        self.text_color = (255, 255, 255)
        
        # Scalars/offsets
        self.tile_size = TILE_SIZE
        self.offset_x = DUNGEON_OFFSET_X
        self.offset_y = DUNGEON_OFFSET_Y

        self.room_color = (80, 80, 80)
        self.current_room_color = (120, 160, 255)
        self.connection_color = (36, 36, 36)
        self.border_color = (255, 255, 255)

    def draw(self, dungeon):
        self.draw_connections(dungeon)
        self.draw_rooms(dungeon)

    def draw_rooms(self, dungeon, cur_room):
        current_room = cur_room

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
            
            # Draw roomtype
            # Render: creates a small surface with text 
            #   room.room_type: the text
            #   anti-aliasing True:smoothed false: more blocky
            #   text color
            text_surface = self.font.render(room.room_type, True, self.text_color)
            
            # This creates a rectangle around the text image.
            text_rect = text_surface.get_rect(center=rect.center)
            
            # Draw it to the screen
            # text_surface: text image
            # text_rect : the location defined by a rect
            self.screen.blit(text_surface, text_rect)

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