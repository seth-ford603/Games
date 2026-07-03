"""
Created on 20260702
Updated on 20260703
@author: Seth Ford
"""

import pygame


class RoomRenderer:
    def __init__(self, floor_image_path):
        # Load floor tile image once
        self.floor_tile = pygame.image.load(floor_image_path).convert()

        # Resize tile if desired
        self.tile_size = 128
        self.floor_tile = pygame.transform.scale(
            self.floor_tile,
            (self.tile_size, self.tile_size)
        )

        # Room visual settings
        self.room_border_color = (0, 0, 0)
        self.room_border_width = 4

    def draw_room(self, screen, room_rect, camera):
        # Draw floor first
        self.draw_floor(screen, room_rect, camera)

        # Draw room border second
        self.draw_room_border(screen, room_rect, camera)

    def draw_floor(self, screen, room_rect, camera):
        # Only allow floor tiles to draw inside the visible room area
        old_clip = screen.get_clip()
        screen.set_clip(camera.apply_rect(room_rect))

        # Draw the floor across the whole room in world space
        for world_x in range(room_rect.left, room_rect.right, self.tile_size):
            for world_y in range(room_rect.top, room_rect.bottom, self.tile_size):

                tile_rect = pygame.Rect(
                    world_x,
                    world_y,
                    self.tile_size,
                    self.tile_size
                )

                # Convert to screen coordinates
                screen_tile_rect = camera.apply_rect(tile_rect)

                # Draw to screen
                screen.blit(self.floor_tile, screen_tile_rect)

        # Restore normal drawing behavior
        screen.set_clip(old_clip)
    
    def draw_room_border(self, screen, room_rect, camera):
        # Convert room rect from world coordinates to screen coordinates
        screen_room_rect = camera.apply_rect(room_rect)

        # Draw room border
        pygame.draw.rect(
            screen,
            self.room_border_color,
            screen_room_rect,
            self.room_border_width
        )
        
    def draw_doors(self, screen, doors, camera):
        # Draw each door in screen coordinates
        for door in doors:
            door.draw(screen, camera)