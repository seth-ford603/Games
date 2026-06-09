# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:03:37 2026

@author: sford
"""

from Room import Room
from Dungeon import Dungeon


class DungeonGenerator:
    def generate(self, theme="standard"):
        rooms = {}

        # Room Consturctor needs: self, room_id, room_type, x, y
        start_room = Room("start", "start", 0, 0, 4, 4)
        combat_room = Room("combat_1", "combat", 4, 0, 3, 3)
        treasure_room = Room("treasure_1", "treasure", 7, 0, 2, 2)
        boss_room = Room("boss", "boss", 9, 0, 5, 5)

        # Connect rooms
        start_room.connect(combat_room)
        combat_room.connect(treasure_room)
        treasure_room.connect(boss_room)

        # Create a lookup table of every room in the dungeon.
        rooms[start_room.room_id] = start_room
        rooms[combat_room.room_id] = combat_room
        rooms[treasure_room.room_id] = treasure_room
        rooms[boss_room.room_id] = boss_room

        return Dungeon(rooms, start_room.room_id)