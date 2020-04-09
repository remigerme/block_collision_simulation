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


APP_WIDTH = 700
APP_HEIGHT = 300

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
	ID = 0
	def __init__(self, mass, x, vx):
		self.id = Block.ID
		Block.ID += 1
		self.mass = mass
		self.size = self.compute_size()
		self.x = x
		self.y = APP_HEIGHT - self.size
		self.vx = vx
		self.dt = 0.1 * (60 / FPS)
		self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))
		self.img = pygame.Surface((self.size, self.size))
		self.img.fill(WHITE)

	def compute_size(self):
		size = 10 + math.log(self.mass) * 2
		return size

	def move(self):
		self.x += self.vx * self.dt
		self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

	def collide(self, block):
		if self.x <= block.x <= self.x + self.size or self.x <= block.x + block.size <= self.x + self.size:
			return True
		return False


def draw(app, bg, walls, blocks):
	app.blit(bg, (0, 0))
	for wall in walls:
		app.blit(wall.img, wall.rect)
	for block in blocks:
		app.blit(block.img, block.rect)


def main():
	pygame.init()
	app = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
	clock = pygame.time.Clock()
	bg = pygame.Surface((APP_WIDTH, APP_HEIGHT))
	bg.fill(BLACK)
	walls = []
	blocks = []
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
		draw(app, bg, walls, blocks)
		clock.tick(FPS)
		pygame.display.update()


if __name__ == "__main__":
	main()