# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:19:59 2026

@author: sford
"""

import pygame

BUTTON_COLOR = (240, 240, 240)
BUTTON_BORDER = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

class Button:
    def __init__(self, text, x, y, width, height, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        pygame.draw.rect(screen, BUTTON_BORDER, self.rect, 2)

        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def was_clicked(self, event):
        return (
            # Check that it was clicked
            event.type == pygame.MOUSEBUTTONDOWN
            # AND that it was the left mouse button
            and event.button == 1
            # AND mouse is inside the range of the ractangle
            and self.rect.collidepoint(event.pos)
        )