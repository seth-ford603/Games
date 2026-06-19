# -*- coding: utf-8 -*-
"""
Created on 20260609
Updated on 20260619
@author: Seth Ford
"""

class Dungeon:
    # Startup
    def __init__(self, rooms, start_room_id):
        self.rooms = rooms
        self.start_room_id = start_room_id
        self.current_room_id = start_room_id

    # Obvio
    def get_current_room(self):
        return self.rooms[self.current_room_id]

    # Obvio
    def get_start_room(self):
        return self.rooms[self.start_room_id]

    # Obvio
    def move_to_room(self, destination_room):
        current_room = self.get_current_room()
    
        if destination_room in current_room.connections:
            self.current_room_id = destination_room.room_id
            return True
    
        return False