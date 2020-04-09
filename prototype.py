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
GREEN = (0, 255, 0)


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
            if self.x <= block.x <= self.x + self.thickness:
                return True
        return False


class Block:
    """
    This class allows us to simply create and manage blocks.
    """
    ID = 0
    def __init__(self, mass, x, vx, color = WHITE):
        self.id = Block.ID
        Block.ID += 1
        self.mass = mass
        self.size = self.compute_size()
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

    def move(self):
        self.x += self.vx * self.dt
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

    def collide(self, block):
        if self.x <= block.x <= self.x + self.size or self.x <= block.x + block.size <= self.x + self.size:
            return True
        return False


def evolve(walls, blocks):
    collisions = 0
    checked_collisions = []
    for block in blocks:
        block.move()
        for wall in walls:
            if wall.collide(block):
                collisions += 1
                block.vx = -block.vx
    return collisions


def draw(app, bg, walls, blocks, more_info, myfont):
    app.blit(bg, (0, 0))
    for wall in walls:
        app.blit(wall.img, wall.rect)
    for block in blocks:
        app.blit(block.img, block.rect)
    app.blit(more_info["text_info"], (20, 10))
    if more_info["status"]:
        text_collision = myfont.render("Collision counter : {}".format(more_info["collision_counter"]), False, WHITE)
        text_time = myfont.render("Time : {}s".format(round(more_info["simulation_time"], 2)), False, WHITE)
        app.blit(text_collision, (20, 40))
        app.blit(text_time, (20, 70))
        for i, block in enumerate(blocks):
            text_block = myfont.render("Block #{} : {}m and {}m/s".format(i + 1, int(block.x),int(block.vx)), False, block.color)
            app.blit(text_block, (20, 70 + 30 * (i + 1)))


def main():
    pygame.init()
    pygame.font.init()

    myfont = pygame.font.SysFont("dejavusans", 20)
    text_info = myfont.render("Press escape to quit, space to pause and i for more information", False, WHITE)

    app = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    clock = pygame.time.Clock()
    bg = pygame.Surface((APP_WIDTH, APP_HEIGHT))
    bg.fill(BLACK)
    default_wall_width = 10
    default_wall_height = 50
    walls = [Wall((0, APP_HEIGHT - default_wall_height), (default_wall_width, default_wall_height)),
            Wall((APP_WIDTH - default_wall_width, APP_HEIGHT - default_wall_height), (default_wall_width, default_wall_height))]
    blocks = [Block(10, 600, -100)]

    simulation_time = 0
    collision_counter = 0
    more_info = {
                "status": True,
                "simulation_time": simulation_time,
                "collision_counter":collision_counter,
                "text_info": text_info
                }
    paused = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_i:
                    more_info["status"] = not more_info["status"]

        if not paused:
            simulation_time += 1 / FPS
            collision_counter += evolve(walls, blocks)
            more_info["simulation_time"] = simulation_time
            more_info["collision_counter"] = collision_counter
            draw(app, bg, walls, blocks, more_info, myfont)
            clock.tick(FPS)
            pygame.display.update()


if __name__ == "__main__":
    main()