# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:03:37 2026

@author: sford
"""

from Room import Room
from Dungeon import Dungeon
import random
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, DUNGEON_OFFSET_X, DUNGEON_OFFSET_Y


class DungeonGenerator:
    # Returns a Dungeon object
    def generate(self, theme="standard"):
        # Loop until a dungeon is returned without overlapping rooms
        rooms = self.create_random_rooms()
        return Dungeon(rooms, "start")

    # Randomizes the rooms height, width, and location
    def create_random_rooms(self):
        rooms = {}
        
        num_rooms = random.randint(3, 7)
        
        # Create rooms
        start_room = self.create_room_at_random_valid_location("start", "start", rooms)
        rooms[start_room.room_id] = start_room
        
        # Set previous room for linear connection loop
        previous_room = start_room
        
        # Loop through room creation
        for room_number in range(1, num_rooms):
            # Create room id
            room_id = "room_" + str(room_number)
            room_type = self.get_random_room_type()
    
            # Create the room, but at a valid location
            new_room = self.create_room_at_random_valid_location(room_id, room_type, rooms)
    
            # Restart if we've entered a state that is impossible to add a room
            if new_room is None:
                return self.create_random_rooms()
    
            # Connect rooms linearly
            previous_room.connect(new_room)
    
            # Add room to list
            rooms[new_room.room_id] = new_room
            
            # Restart if we've entered a state that has a connection overlap a room
            if self.has_connection_intersections(rooms):
                return self.create_random_rooms()
            
            # Rest prev room for next loop iteration
            previous_room = new_room
    
        # Assign boss room
        self.assign_boss_room(start_room)
    
        return rooms

    def create_room_at_random_valid_location(self, room_id, room_type, rooms):
        # Detect the screen, determine max x and y dependent on screen 
        max_x = (SCREEN_WIDTH - DUNGEON_OFFSET_X) // TILE_SIZE
        max_y = (SCREEN_HEIGHT - DUNGEON_OFFSET_Y) // TILE_SIZE
    
        # Random widths and heights
        width = random.randint(1, 5)
        height = random.randint(1, 5)
    
        # List of valid locations
        valid_locations = []
    
        # Loop through all possible locations and add it to the list if valid
        for x in range(0, max_x - width + 1):
            for y in range(0, max_y - height + 1):
                test_room = Room(room_id, room_type, x, y, width, height)
    
                if self.room_location_is_valid(test_room, rooms):
                    valid_locations.append((x, y))
    
        # Exit if there are no valid locs
        if len(valid_locations) == 0:
            return None
    
        # Randomley select one of the locations from the list of valids
        selected_x, selected_y = random.choice(valid_locations)
    
        # Return that room
        return Room(room_id, room_type, selected_x, selected_y, width, height)
    
    # Returns true if a rooms location is valid
    def room_location_is_valid(self, test_room, rooms):
        if self.room_is_clipped(test_room):
            return False
    
        for existing_room in rooms.values():
            if self.rooms_overlap(test_room, existing_room):
                return False
    
        return True

    # Returns a random room type
    def get_random_room_type(self):
        room_types = ["combat", "treasure"]
        return random.choice(room_types)

    # Returns false if two rects are overlapping
    def rooms_overlap(self, room_a, room_b):
        # Define the edges of both rectangles
        a_left = room_a.x
        a_right = room_a.x + room_a.width
        a_top = room_a.y
        a_bottom = room_a.y + room_a.height

        b_left = room_b.x
        b_right = room_b.x + room_b.width
        b_top = room_b.y
        b_bottom = room_b.y + room_b.height

        # Check if opposite edges are overlapping
        if a_right <= b_left:
            return False

        if a_left >= b_right:
            return False

        if a_bottom <= b_top:
            return False

        if a_top >= b_bottom:
            return False

        return True
    
    # Returns false if two rects overlaps with screen edge
    def room_is_clipped(self, room):
        screen_x = DUNGEON_OFFSET_X + room.x * TILE_SIZE
        screen_y = DUNGEON_OFFSET_Y + room.y * TILE_SIZE
        screen_width = room.width * TILE_SIZE
        screen_height = room.height * TILE_SIZE
    
        room_left = screen_x
        room_right = screen_x + screen_width
        room_top = screen_y
        room_bottom = screen_y + screen_height
    
        if room_left < 0:
            return True
    
        if room_top < 0:
            return True
    
        if room_right > SCREEN_WIDTH:
            return True
    
        if room_bottom > SCREEN_HEIGHT:
            return True
    
        return False
    
    # Returns a list that contains rooms that are farthest from the start room
    def get_farthest_rooms(self, start_room):
        distances = {} # To store distances from start
        queue = [(start_room, 0)] # Stores (room, distance)
        visited = set() # Track rooms we have already processed
    
        # Continue while items exist in queue
        while queue:
            # Get first pair from queue
            current_room, distance = queue.pop(0)
    
            # Skip if pairing exists in visited
            if current_room in visited:
                continue
    
            # Add the pairing to visited
            visited.add(current_room)
            # Store current distance from start
            distances[current_room] = distance
    
            # For each connection to the current room
            for connected_room in current_room.connections:
                # If the connection has not been visited
                if connected_room not in visited:
                    # Add it to the queue and add 1 to distance since the room is 1 step away
                    queue.append((connected_room, distance + 1))
                    
        # At this point, distances contains a list of rooms and their distance from start
        
        # Find the max value in the distance list
        max_distance = max(distances.values())
    
        # Create a list to store farthest rooms
        farthest_rooms = []
    
        # For each room in distance
        for room, distance in distances.items():
            # If room = max distance
            if distance == max_distance:
                # Append to farthest_rooms list
                farthest_rooms.append(room)
    
        return farthest_rooms
    
    # Assigns a room to be a boss room
    def assign_boss_room(self, start_room):
        farthest_rooms = self.get_farthest_rooms(start_room)
        boss_room = random.choice(farthest_rooms)
        boss_room.room_type = "boss"

    # Checks if there are any room intersections with a connection
    def has_connection_intersections(self, rooms):
        checked_connections = set()
    
        for room in rooms.values():
            for connected_room in room.connections:
                connection_key = tuple(sorted([room.room_id, connected_room.room_id]))
    
                if connection_key in checked_connections:
                    continue
    
                if self.connection_intersects_other_room(room, connected_room, rooms):
                    return True
    
                checked_connections.add(connection_key)
    
        return False

    # Checks a single connection for intersections
    def connection_intersects_other_room(self, room_a, room_b, rooms):
        start_x = room_a.center_x
        start_y = room_a.center_y
        
        end_x = room_b.center_x
        end_y = room_b.center_y
    
        for room in rooms.values():
            if room == room_a or room == room_b:
                continue
    
            if self.line_passes_through_room(start_x, start_y, end_x, end_y, room):
                return True
    
        return False
    
    # Returns true if a line passes through a room
    def line_passes_through_room(self, start_x, start_y, end_x, end_y, room):
        sample_count = 100
    
        for i in range(sample_count + 1):
            progress = i / sample_count
    
            point_x = start_x + (end_x - start_x) * progress
            point_y = start_y + (end_y - start_y) * progress
    
            if self.point_inside_room(point_x, point_y, room):
                return True
    
        return False
    
    # Returns true if a point is inside a room
    def point_inside_room(self, point_x, point_y, room):
        room_left = room.x
        room_right = room.x + room.width
        room_top = room.y
        room_bottom = room.y + room.height
    
        if point_x >= room_left and point_x <= room_right:
            if point_y >= room_top and point_y <= room_bottom:
                return True
    
        return False
