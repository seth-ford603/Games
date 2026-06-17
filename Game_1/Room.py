# -*- coding: utf-8 -*-
"""
Created on:  20260609   
Last Update: 20260617 

@author: sford
"""

from GameConfig import DUNGEON_OFFSET_Y, DUNGEON_OFFSET_X, TILE_SIZE

class Room:
    # x, y represent the top-left coordinate of the room
    # width and height are measured in dungeon units
    def __init__(self, room_id, room_type, x, y, width, height):
        self.room_id = room_id
        self.room_type = room_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.connections = []

    # Connects a room to another
    def connect(self, other_room):
        if other_room not in self.connections:
            self.connections.append(other_room)
    
        if self not in other_room.connections:
            other_room.connections.append(self)
        
    # Rooms are drawn from center to center so these functions make measurment easier
    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2
    
    # Return the pixel locations of each side
    @property
    def left_side_px(self):
        return DUNGEON_OFFSET_X + self.x * TILE_SIZE
    
    @property
    def right_side_px(self):
        return DUNGEON_OFFSET_X + (self.x + self.width) * TILE_SIZE
    
    @property
    def top_side_px(self):
        return DUNGEON_OFFSET_Y + self.y * TILE_SIZE
    
    @property
    def bottom_side_px(self):
        return DUNGEON_OFFSET_Y + (self.y + self.height) * TILE_SIZE
    
    # Return the pixel locations of each room's X and Y coord
    @property
    def x_px(self):
        return DUNGEON_OFFSET_X + self.center_x * TILE_SIZE
    
    @property
    def y_px(self):
        return DUNGEON_OFFSET_Y + self.center_y * TILE_SIZE
    