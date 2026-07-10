"""
Created on 20260710
Updated on 20260710
@author: Seth Ford

Controls gameplay behavior while the character is in the world.
"""

import pygame

from ControllerPackage.AreaController import AreaController
from WorldPackage.WorldRenderer import WorldRenderer


class WorldController(AreaController):

    def __init__(self, world, character, camera):
        super().__init__(character, camera)

        # World data
        self.world = world

        # World rendering
        self.world_renderer = WorldRenderer("assets/grassy_area.png")

        # Temporary debug text
        self.font = pygame.font.SysFont(None, 36)

    def enter(self):
        # Spawn the character in the center of the world
        spawn_x, spawn_y = self.world.get_spawn_position(self.character)
        self.character.x = spawn_x
        self.character.y = spawn_y

        # Position the camera around the new spawn
        self.camera.update(
            self.character.get_rect(),
            self.get_boundary_rect()
        )

    def update(self, dt):
        world_rect = self.get_boundary_rect()

        # Keep the character inside the world
        self.character.keep_inside_rect(world_rect)

        # Check whether the character touched a dungeon entrance
        for entrance in self.world.get_dungeon_entrances():
            if entrance.is_touched_by(self.character):
                return "dungeon"

        # Follow the character through the world
        self.camera.update(
            self.character.get_rect(),
            world_rect
        )

        return None

    def draw(self, screen):
        world_rect = self.get_boundary_rect()

        self.world_renderer.draw_world(
            screen,
            world_rect,
            self.camera
        )

        self.world_renderer.draw_dungeon_entrances(
            screen,
            self.world.get_dungeon_entrances(),
            self.camera
        )

        # Temporary debug information
        world_text = self.font.render(
            "Area: World",
            True,
            (255, 255, 255)
        )

        position_text = self.font.render(
            f"X: {int(self.character.x)} Y: {int(self.character.y)}",
            True,
            (255, 255, 255)
        )

        screen.blit(world_text, (20, 20))
        screen.blit(position_text, (20, 50))

    def get_boundary_rect(self):
        return self.world.get_rect()