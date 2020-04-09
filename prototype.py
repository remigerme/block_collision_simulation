"""
First prototype of the project.
We have one or two blocs :
	- that are square (no matter their shape in this prototype)
	- whose the mass, the initial velocity and position are given (no acceleration)
	- moving along the same and unique horizontal axis
	- there is no loss of energy when blocks collide together or with a wall
	- there can be friction with the ground only (not air)

We can :
	- activate / desactivate the side walls
	- make the two blocs collide each other, and know what their velocity and position will be
	- obviously count the number of collisions between the blocks, if only the left side wall is enabled
"""


import math
import pygame

FPS = 240 # it will compute 240 times per second the position of the blocks

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Wall:
	"""
	This class allows us to create walls, with which blocks will interact.
	"""
	def __init__(self, pos, size):
		self.x = pos[0]
		self.y = pos[1]
		self.thickness = size[0]
		self.height = size[1]
		self.rect = pygame.Rect((self.x, self.y), (self.thickness, self.height))
		self.img = pygame.Surface((self.thickness, self.height))
		self.img.fill(WHITE)

	def collide(self, block):
		# as we have only one horizontal axis, we don't matter of the vertical axis
		if block.vx > 0:
			if self.x <= block.x + block.size <= self.x + self.thickness:
				return True
		else:
			if self.x <= block.x <= self.x + self.thickness
				return True
		return False


class Block:
	"""
	This class allows us to simply create and manage blocks.
	"""
	def __init__(self):
		print("Block created !")


def main():
	pass


if __name__ == "__main__":
	main()