"""
Created on 20260703
Updated on 20260703
@author: Seth Ford
"""

import pygame


class WorldRenderer:
    def __init__(self, grass_image_path):
        # Load grass tile once
        self.grass_tile = pygame.image.load(grass_image_path).convert()

        # Scale the tile
        self.tile_size = 128
        self.grass_tile = pygame.transform.scale(
            self.grass_tile,
            (self.tile_size, self.tile_size)
        )

    def draw_world(self, screen, world_rect, camera):
        # Draw grass across the whole world in world space
        for world_x in range(world_rect.left, world_rect.right, self.tile_size):
            for world_y in range(world_rect.top, world_rect.bottom, self.tile_size):

                tile_rect = pygame.Rect(
                    world_x,
                    world_y,
                    self.tile_size,
                    self.tile_size
                )

                # Convert world position to screen position
                screen_tile_rect = camera.apply_rect(tile_rect)

                # Draw grass tile
                screen.blit(self.grass_tile, screen_tile_rect)