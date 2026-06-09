# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:02:58 2026

@author: sford
"""

class Room:
    # x, y represent the top-left coordinate of the room
    # width and height are measured in dungeon units
    def __init__(self, room_id, room_type, x, y, height, width):
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
        return self.x + self.width // 2

    @property
    def center_y(self):
        return self.y + self.height // 2