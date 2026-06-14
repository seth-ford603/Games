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

    # Randomizes the rooms height, width, and location. Add them to a list we can use
    def create_random_rooms(self):
        # Create room list
        rooms = {}
    
        # Establish path length and number of branches randomly
        main_path_length = random.randint(3, 7)
        branch_count = random.randint(2, 4)
    
        # Create start room and add it to the list
        start_room = self.create_room_at_random_valid_location("start", "start", rooms)
        rooms[start_room.room_id] = start_room
    
        # Create the main path of rooms
        main_path_rooms = self.create_main_path(start_room, main_path_length, rooms)
    
        # If the room list is empty, restart
        if main_path_rooms is None:
            return self.create_random_rooms()
    
        # Create branches
        branches_created = self.create_branches(branch_count, rooms)
    
        # If brannches DNE, restart.
        if branches_created == False:
            return self.create_random_rooms()
    
        # Assign the boss room
        self.assign_boss_room(start_room)
    
        # Return list of rooms
        return rooms
    
    # Create the main dungeon path
    def create_main_path(self, start_room, main_path_length, rooms):
        # Create linkage between rooms
        previous_room = start_room
        main_path_rooms = [start_room]
    
        # For each room between 1 and max number of rooms.
        for room_number in range(1, main_path_length):
            # Create the room ID and room type
            room_id = "room_" + str(room_number)
            room_type = self.get_random_room_type()
    
            # Create the room
            new_room = self.create_room_at_random_valid_location(room_id, room_type, rooms, previous_room)
    
            # If room is empty, return empty room
            if new_room is None:
                return None
    
            # Move linkage forward one
            previous_room.connect(new_room)
            rooms[new_room.room_id] = new_room
    
            # Verify this room does not have connections that intersect with another room
            # Exit and restart if so by returning none
            if self.connection_intersects_room(rooms):
                return None
    
            # Verify this room does not have connections that intersect with another connection
            # Exit and restart if so by returning none
            if self.connection_intersects_connection(previous_room, new_room, rooms):
                return None
    
            # Add the room to the main path
            main_path_rooms.append(new_room)
            # Increment linkage
            previous_room = new_room
    
        # Return main path of rooms
        return main_path_rooms
    
    # Add branches to the main dungeon path
    def create_branches(self, branch_count, rooms):
        # Create counter to track max rooms
        next_room_number = len(rooms)
    
        # For each branch to be created
        for branch_number in range(branch_count):
            # Identify a possible parent list
            possible_parent_rooms = list(rooms.values())
    
            # Select one randomly
            parent_room = random.choice(possible_parent_rooms)
    
            # Create a room id and room type
            room_id = "room_" + str(next_room_number)
            room_type = self.get_random_room_type()
    
            # Add the room to a valid location
            branch_room = self.create_room_at_random_valid_location(room_id, room_type, rooms, parent_room)
    
            # If branch cannot be created, restart by returning false
            if branch_room is None:
                return False
    
            # Create linkage between room and parent. Add it to the list
            parent_room.connect(branch_room)
            rooms[branch_room.room_id] = branch_room
    
            # Verify this room does not have connections that intersect with another room
            # Exit and restart if so by returning false
            if self.connection_intersects_room(rooms):
                return False
    
            # Verify this room does not have connections that intersect with another connection
            # Exit and restart if so by returning false
            if self.connection_intersects_connection(parent_room, branch_room, rooms):
                return False
    
            # Increment number of rooms
            next_room_number += 1
    
        # Signal successful branch creation
        return True

    # Adds a room to the canvas where there is not already a room.
    def create_room_at_random_valid_location(self, room_id, room_type, rooms, parent_room=None):
        # Detect the screen, determine max x and y dependent on screen 
        max_x = (SCREEN_WIDTH - DUNGEON_OFFSET_X) // TILE_SIZE
        max_y = (SCREEN_HEIGHT - DUNGEON_OFFSET_Y) // TILE_SIZE
    
        # Room width and height
        width = random.randint(2, 5)
        height = random.randint(2, 5)
    
        # List of valid locations
        valid_locations = []
    
        # Loop through all possible locations and add it to the list if valid
        for x in range(0, max_x - width + 1):
            for y in range(0, max_y - height + 1):
                # Create random room at random location
                test_room = Room(room_id, room_type, x, y, width, height)
    
                # Verify location is valid
                if self.room_location_is_valid(test_room, rooms):
                    # Verify new room is within valid distance (except start room which will have none as parent)
                    if parent_room is None or self.room_is_valid_distance_from_parent(test_room, parent_room):
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
        # Check for connection overlap
        if self.room_is_clipped(test_room):
            return False
    
        # Check for room overlaps
        for existing_room in rooms.values():
            if self.rooms_overlap(test_room, existing_room):
                return False
    
        # Check for close distances with other rooms
        if self.room_is_minimum_distance_from_all_rooms(test_room, rooms) == False:
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
        # Convert locations to pixels
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
    def connection_intersects_room(self, rooms):
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
    
    # Checks if any connections for a room intersect with another
    def connection_intersects_connection(self, room_a, room_b, rooms):
        # For each room in our rooms list
        for existing_room in rooms.values():
            # For each connection in that room
            for connected_room in existing_room.connections:
    
                # Do not compare the connection against itself
                if existing_room == room_a and connected_room == room_b:
                    continue
    
                if existing_room == room_b and connected_room == room_a:
                    continue
    
                # Ignore connections that share an endpoint
                if existing_room == room_a or existing_room == room_b:
                    continue
    
                if connected_room == room_a or connected_room == room_b:
                    continue
    
                # Check if the lines intersect
                if self.lines_intersect(
                    room_a.center_x,
                    room_a.center_y,
                    room_b.center_x,
                    room_b.center_y,
                    existing_room.center_x,
                    existing_room.center_y,
                    connected_room.center_x,
                    connected_room.center_y
                ):
                    return True
    
        return False
    
    # Compares two lines. They intersect if their endpoints are on opposite sides of a line. 
    # (If a line C-D bisects points A and B then there is an intersection)
    def lines_intersect(self, a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y):
        # Are A and B on opposite sides of line C-D?
        position_1 = self.get_position(c_x, c_y, d_x, d_y, a_x, a_y)
        position_2 = self.get_position(c_x, c_y, d_x, d_y, b_x, b_y)
        # Are C and D on opposite sides of line A-B?
        position_3 = self.get_position(a_x, a_y, b_x, b_y, c_x, c_y)
        position_4 = self.get_position(a_x, a_y, b_x, b_y, d_x, d_y)
    
        # If positions are not the same, then an intersection exists
        if position_1 != position_2 and position_3 != position_4:
            return True
    
        return False
    
    # Gets the position of a point relative to a line.
    # Two points that both return the same value are on the same side of the provided line.
    def get_position(self, line_start_x, line_start_y, line_end_x, line_end_y, point_x, point_y):
        value = (
            (point_y - line_start_y) * (line_end_x - line_start_x)
            - (line_end_y - line_start_y) * (point_x - line_start_x)
        )
    
        if value > 0:
            return 1
    
        if value < 0:
            return -1
    
        return 0
    
    # Returns true if test_room location is with a donut shaped valid area for placement
    # min_distance and max_distance control this valid area
    def room_is_valid_distance_from_parent(self, test_room, parent_room):
        # Set min/max distances
        min_distance = 75
        max_distance = 175
    
        # test_room.center_x returns the center of the test room in tiles
        # We need to convert this to pixels to measure distance in pixels
        test_center_x = DUNGEON_OFFSET_X + test_room.center_x * TILE_SIZE
        test_center_y = DUNGEON_OFFSET_Y + test_room.center_y * TILE_SIZE
    
        parent_center_x = DUNGEON_OFFSET_X + parent_room.center_x * TILE_SIZE
        parent_center_y = DUNGEON_OFFSET_Y + parent_room.center_y * TILE_SIZE
    
        # Find distance with pyth theorem
        # For horiz and vert seperation
        dx = test_center_x - parent_center_x
        dy = test_center_y - parent_center_y
    
        # Square and add together then compare
        distance_squared = dx * dx + dy * dy
    
        # Just square distance values for easier math
        if distance_squared < min_distance * min_distance:
            return False
    
        if distance_squared > max_distance * max_distance:
            return False
    
        return True
    
    # Returns false if test room is too close to any other room by checking room edges
    def room_is_minimum_distance_from_all_rooms(self, test_room, rooms):
        min_distance = 5
    
        for existing_room in rooms.values():
            if self.rooms_are_too_close(test_room, existing_room, min_distance):
                return False
    
        return True
    
    # Returns false if two rooms are too close
    def rooms_are_too_close(self, room_a, room_b, min_distance):
        # Convert sides to pixel locations
        a_left = DUNGEON_OFFSET_X + room_a.x * TILE_SIZE
        a_right = DUNGEON_OFFSET_X + (room_a.x + room_a.width) * TILE_SIZE
        a_top = DUNGEON_OFFSET_Y + room_a.y * TILE_SIZE
        a_bottom = DUNGEON_OFFSET_Y + (room_a.y + room_a.height) * TILE_SIZE
    
        b_left = DUNGEON_OFFSET_X + room_b.x * TILE_SIZE
        b_right = DUNGEON_OFFSET_X + (room_b.x + room_b.width) * TILE_SIZE
        b_top = DUNGEON_OFFSET_Y + room_b.y * TILE_SIZE
        b_bottom = DUNGEON_OFFSET_Y + (room_b.y + room_b.height) * TILE_SIZE
    
        # Compare edge locations
        if a_right + min_distance <= b_left:
            return False
    
        if a_left - min_distance >= b_right:
            return False
    
        if a_bottom + min_distance <= b_top:
            return False
    
        if a_top - min_distance >= b_bottom:
            return False
    
        return True
