"""
Created on 20260710
Updated on 20260710
@author: Seth Ford

Controls gameplay behavior while the character is inside a dungeon.
"""

import pygame

from ControllerPackage.AreaController import AreaController
from DungeonPackage.Door import Door
from DungeonPackage.RoomRenderer import RoomRenderer
from GameConfig import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class DungeonController(AreaController):

    ROOM_SCALE = 14
    ROOM_ENTRY_PADDING = 30

    def __init__(self, dungeon, character, camera):
        super().__init__(character, camera)

        # Dungeon data
        self.dungeon = dungeon

        # Dungeon rendering
        self.room_renderer = RoomRenderer("assets/stone_floor.png")

        # Temporary debug text
        self.font = pygame.font.SysFont(None, 36)

        # Cached playable-room information
        self.current_room_rect = None
        self.current_doors = []

    def enter(self):
        # Build the playable representation of the starting room
        self.refresh_current_room()

        # Spawn the character in the center of the starting room
        self.character.x = (
            self.current_room_rect.centerx - self.character.width / 2
        )
        self.character.y = (
            self.current_room_rect.centery - self.character.height / 2
        )

        # Position the camera around the new spawn
        self.camera.update(
            self.character.get_rect(),
            self.current_room_rect
        )

    def update(self, dt):
        # Keep the character inside the active room
        self.character.keep_inside_rect(self.current_room_rect)

        # Check whether the character entered one of the room's doors
        self.handle_door_collision()

        # A room transition may have changed the active room boundary
        self.character.keep_inside_rect(self.current_room_rect)

        # Follow the character through the active room
        self.camera.update(
            self.character.get_rect(),
            self.current_room_rect
        )

        return None

    def draw(self, screen):
        self.room_renderer.draw_room(
            screen,
            self.current_room_rect,
            self.camera
        )

        self.room_renderer.draw_doors(
            screen,
            self.current_doors,
            self.camera
        )

        current_room = self.dungeon.get_current_room()

        # Temporary debug information
        room_text = self.font.render(
            f"Room: {current_room.room_id}",
            True,
            (255, 255, 255)
        )

        type_text = self.font.render(
            f"Type: {current_room.room_type}",
            True,
            (255, 255, 255)
        )

        screen.blit(room_text, (20, 20))
        screen.blit(type_text, (20, 50))

    def get_boundary_rect(self):
        return self.current_room_rect

    def refresh_current_room(self):
        """
        Rebuild room geometry and doors only when the active room changes.
        """
        current_room = self.dungeon.get_current_room()

        self.current_room_rect = self.create_room_rect(current_room)
        self.current_doors = self.create_doors(
            current_room,
            self.current_room_rect
        )

    def create_room_rect(self, room):
        room_width = room.width * TILE_SIZE * self.ROOM_SCALE
        room_height = room.height * TILE_SIZE * self.ROOM_SCALE

        room_x = (SCREEN_WIDTH - room_width) // 2
        room_y = (SCREEN_HEIGHT - room_height) // 2

        return pygame.Rect(
            room_x,
            room_y,
            room_width,
            room_height
        )

    def create_doors(self, current_room, room_rect):
        doors = []

        for connected_room in current_room.connections:
            doors.append(
                Door(current_room, connected_room, room_rect)
            )

        return doors

    def handle_door_collision(self):
        character_rect = self.character.get_rect()

        for door in self.current_doors:
            if character_rect.colliderect(door.rect):
                self.try_enter_door(door)
                break

    def try_enter_door(self, door):
        moved = self.dungeon.move_to_room(door.target_room)

        if moved:
            self.refresh_current_room()
            self.place_character_after_room_transition(door)

    def place_character_after_room_transition(self, entered_door):
        room_rect = self.current_room_rect
        padding = self.ROOM_ENTRY_PADDING

        center_x = room_rect.centerx - self.character.width / 2
        center_y = room_rect.centery - self.character.height / 2

        # The entered door's direction describes where the destination room
        # was relative to the previous room. Spawn on the opposite side of
        # the new room so the character does not immediately re-enter it.
        if entered_door.direction == "north":
            self.character.x = center_x
            self.character.y = (
                room_rect.bottom - self.character.height - padding
            )

        elif entered_door.direction == "south":
            self.character.x = center_x
            self.character.y = room_rect.top + padding

        elif entered_door.direction == "east":
            self.character.x = room_rect.left + padding
            self.character.y = center_y

        elif entered_door.direction == "west":
            self.character.x = (
                room_rect.right - self.character.width - padding
            )
            self.character.y = center_y

        self.camera.update(
            self.character.get_rect(),
            room_rect
        )