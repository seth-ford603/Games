# -*- coding: utf-8 -*-
"""
Created on 20260710
Updated on 20260710
@author: Seth Ford

Base controller for playable game areas.

"""


class AreaController:
    """
    Defines the common behavior ExecutionState expects from every playable area controller.
    """
    def __init__(self, character, camera):
        self.character = character
        self.camera = camera

    def enter(self):
        """
        Prepare the area when it becomes the active controller.

        Concrete controllers should position the character and update
        the camera for their area.
        """
        pass

    def update(self, dt):
        """
        Update area-specific gameplay.

        Return a transition name such as "dungeon" when ExecutionState
        should switch controllers. Return None when no transition occurs.
        """
        return None

    def draw(self, screen):
        """Draw the area, excluding the character."""
        pass

    def get_boundary_rect(self):
        """Return the rectangle that bounds the active playable area."""
        raise NotImplementedError