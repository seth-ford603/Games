# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:04:04 2026

@author: sford
"""

from DungeonGenerator import DungeonGenerator


class DungeonFactory:
    def create_dungeon(self, game_context=None):
        generator = DungeonGenerator()

        if game_context is None:
            return generator.generate()

        return generator.generate(game_context.dungeon_theme)