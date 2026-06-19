# -*- coding: utf-8 -*-
"""
Created on 20260609
Updated on 20260619
@author: Seth Ford
"""

import random
# DungeonPackage
from DungeonPackage.Room import Room
from DungeonPackage.Dungeon import Dungeon
# Main
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, DUNGEON_OFFSET_X, DUNGEON_OFFSET_Y


class DungeonGenerator:
    
    VALID_DONUT_MIN_DIST = 75
    VALID_DONUT_MAX_DIST = 175
    
    MIN_VALID_DISTANCE_ALL_ROOMS = 5
    
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
            # Exit and restart if so by returning false
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

        # Check if opposite edges are overlapping
        if room_a.right_side_px <= room_b.left_side_px:
            return False

        if room_a.left_side_px >= room_b.right_side_px:
            return False

        if room_a.bottom_side_px <= room_b.top_side_px:
            return False

        if room_a.top_side_px >= room_b.bottom_side_px:
            return False

        return True
    
    # Returns false if two rects overlaps with screen edge
    def room_is_clipped(self, room):
        # Compare room edges to see if they exceed the window dimensions
        if room.left_side_px < 0:
            return True
    
        if room.top_side_px < 0:
            return True
    
        if room.right_side_px > SCREEN_WIDTH:
            return True
    
        if room.bottom_side_px > SCREEN_HEIGHT:
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
        start_x = room_a.x_px
        start_y = room_a.y_px
        
        end_x = room_b.x_px
        end_y = room_b.y_px
    
        for room in rooms.values():
            if room == room_a or room == room_b:
                continue
    
            if self.line_passes_through_room(start_x, start_y, end_x, end_y, room):
                return True
    
        return False
    
    # Returns true if a line passes through a room
    def line_passes_through_room(self, start_x, start_y, end_x, end_y, room):
        sample_count = 100
    
        # Check 100 points on the line and see if any of them are inside a room
        for i in range(sample_count + 1):
            progress = i / sample_count
    
            point_x = start_x + (end_x - start_x) * progress
            point_y = start_y + (end_y - start_y) * progress
    
            if self.point_inside_room(point_x, point_y, room):
                return True
    
        return False
    
    # Returns true if a point is inside a room
    def point_inside_room(self, point_x, point_y, room):
        # Check the location of the point relative to the rooms walls
        if point_x >= room.left_side_px and point_x <= room.right_side_px:
            if point_y >= room.top_side_px and point_y <= room.bottom_side_px:
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
                    room_a.x_px,
                    room_a.y_px,
                    room_b.x_px,
                    room_b.y_px,
                    existing_room.x_px,
                    existing_room.y_px,
                    connected_room.x_px,
                    connected_room.y_px
                ):
                    return True
    
        return False
    
    # Compares two lines. They intersect if their endpoints are on opposite sides of the line we are checking for intersection. 
    # (If a line C-D bisects points A and B then there is an intersection)
    def lines_intersect(self, a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y):
        # Are A and B on opposite sides of line C-D?
        # Are C and D on opposite sides of line A-B?
        
        # Start by getting position of each
        # Point A relative to line CD
        position_a = self.get_position(c_x, c_y, d_x, d_y, a_x, a_y)
        # Point B relative to line CD
        position_b = self.get_position(c_x, c_y, d_x, d_y, b_x, b_y)
        # Point C relative to line AB
        position_c = self.get_position(a_x, a_y, b_x, b_y, c_x, c_y)
        # Point D relative to line AB
        position_d = self.get_position(a_x, a_y, b_x, b_y, d_x, d_y)
    
        # If positions are not the same, then an intersection exists
        if position_a != position_b and position_c != position_d:
            return True
    
        return False
    
    # Gets the position of a point relative to a line.
    # Two points that both return the same value are on the same side of the provided line.
    # This uses 2D cross product math
    def get_position(self, line_start_x, line_start_y, line_end_x, line_end_y, point_x, point_y):
        # Line A = (line_start_x, line_start_y)
        # Line B = (line_end_x, line_end_y)
        # Test Point P = (point_x, point_y)
        
        # Vector AB
        AB_x = line_end_x - line_start_x
        AB_y = line_end_y - line_start_y
        
        # Vector AP
        AP_x = point_x - line_start_x
        AP_y = point_y - line_start_y
        
        # Find the 2D cross product
        value = AP_y * AB_x - AB_y * AP_x
    
        # If the cross product is pos, then dot is on pos side of line
        if value > 0:
            return 1
    
        # If the cross product is neg, then dot is on neg side of line
        if value < 0:
            return -1
    
        # If the cross product is 0, then dot is directly on the line
        return 0
    
    # Returns true if test_room location is with a donut shaped valid area for placement
    # min_distance and max_distance control this valid area
    def room_is_valid_distance_from_parent(self, test_room, parent_room):
        # Retrieve min/max distances from class constants
        min_distance = self.VALID_DONUT_MIN_DIST
        max_distance = self.VALID_DONUT_MAX_DIST
    
        # Find distance with pyth theorem
        # For horiz and vert seperation
        dx = test_room.x_px - parent_room.x_px
        dy = test_room.y_px - parent_room.y_px
    
        # Square and add together then compare
        distance_squared = (dx * dx) + (dy * dy)
    
        # Just square distance values for easier math
        if distance_squared < (min_distance * min_distance):
            return False
    
        if distance_squared > (max_distance * max_distance):
            return False
    
        return True
    
    # Returns false if test room is too close to any other room by checking room edges
    def room_is_minimum_distance_from_all_rooms(self, test_room, rooms):
        # Retrieve min distance from class contants
        min_distance = self.MIN_VALID_DISTANCE_ALL_ROOMS
    
        # For each room in our room list...
        for existing_room in rooms.values():
            # ...if the rooms are too close return false
            if self.rooms_are_too_close(test_room, existing_room, min_distance):
                return False
        # ...otherwise return true
        return True
    
    # Returns false if two rooms are too close
    def rooms_are_too_close(self, room_a, room_b, min_distance):
       
        # Compare edge locations
        # If left edge is farther left than other right edge, they overlap, repeat logic
        if (room_a.right_side_px) + min_distance <= (room_b.left_side_px):
            return False
    
        if (room_a.left_side_px) - min_distance >= (room_b.right_side_px):
            return False
    
        if (room_a.bottom_side_px) + min_distance <= (room_b.top_side_px):
            return False
    
        if (room_a.top_side_px) - min_distance >= (room_b.bottom_side_px):
            return False
        
        return True
    