import pygame
from color import *


class Wall:
    """
    This class allows us to create walls, with which blocks will interact.
    """
    def __init__(self, pos, size, color = colors["white"]):
        self.status = True
        self.x = pos[0]
        self.y = pos[1]
        self.thickness = size[0]
        self.height = size[1]
        self.color = color
        self.rect = pygame.Rect((self.x, self.y), (self.thickness, self.height))
        self.img = pygame.Surface((self.thickness, self.height))
        self.img.fill(self.color)

    def collide(self, block):
        # as we have only one horizontal axis, we don't matter of the vertical axis
        if block.vx > 0:
            if self.x <= block.x + block.size <= self.x + self.thickness:
                return True
        else:
            if self.x <= block.x <= self.x + self.thickness:
                return True
        return False