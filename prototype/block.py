import math
import pygame
from color import *


class Block:
    """
    This class allows us to simply create and manage blocks.
    """
    ID = 0
    def __init__(self, mass, x, vx, FPS, APP_HEIGHT, color = WHITE):
        self.id = Block.ID
        Block.ID += 1

        self.mass = mass
        self.size = self.compute_size()

        self.distance_traveled = 0
        self.x = x
        self.y = APP_HEIGHT - self.size
        self.vx = vx
        self.dt = 1 / FPS
        
        self.color = color
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))
        self.img = pygame.Surface((self.size, self.size))
        self.img.fill(self.color)

    def compute_size(self):
        size = 10 + math.log(self.mass) * 2
        return size

    def move(self, time_speed_modifier):
        self.x += self.vx * self.dt * time_speed_modifier
        self.distance_traveled += abs(self.vx * self.dt * time_speed_modifier)
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

    def collide(self, block):
        if self.x <= block.x <= self.x + self.size or self.x <= block.x + block.size <= self.x + self.size:
            return True
        return False