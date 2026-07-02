"""
Created on 20260702
Updated on 20260702
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