# -*- coding: utf-8 -*-
"""
Created on 20260609
Updated on 20260619
@author: Seth Ford
"""

from DungeonPackage.DungeonGenerator import DungeonGenerator


class DungeonFactory:
    def create_dungeon(self, game_context=None):
        generator = DungeonGenerator()

        if game_context is None:
            return generator.generate()

        return generator.generate(game_context.dungeon_theme)