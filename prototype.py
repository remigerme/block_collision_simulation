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


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Wall:
    """
    This class allows us to create walls, with which blocks will interact.
    """
    def __init__(self, pos, size):
        self.status = True
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
    def __init__(self, mass, x, vx, APP_HEIGHT = 300, color = WHITE, FPS = 60):
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

    def move(self, time_speed_modifier = 1):
        self.x += self.vx * self.dt * time_speed_modifier
        self.distance_traveled += abs(self.vx * self.dt)
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

    def collide(self, block):
        if self.x <= block.x <= self.x + self.size or self.x <= block.x + block.size <= self.x + self.size:
            return True
        return False


class Simulation:
    def __init__(self):
        # basic properties
        self.APP_WIDTH = 700 # default value, can change
        self.APP_HEIGHT = 300 # default value, can change
        self.FPS = 60 # default value, can change

        # physical objects
        self.wall_size = (10, 50) # can maybe change, don't know for the moment
        self.walls = [
                    Wall((0, self.APP_HEIGHT - self.wall_size[1]), self.wall_size),
                    Wall((self.APP_WIDTH - self.wall_size[0], self.APP_HEIGHT - self.wall_size[1]), self.wall_size)
                    ]
        self.blocks = [
                    Block(1, 100, 0, self.APP_HEIGHT, FPS = self.FPS), # can change all parameters ofc
                    Block(100, 200, -30, self.APP_HEIGHT, color = GREEN, FPS = self.FPS)
                    ]

        # more information
        self.simulation_time = 0
        self.time_speed_modifier = 1 # default value, can change
        self.collisions_counter = 0
        self.more_info_status = True

    def run(self):
        pygame.init()
        self.app = pygame.display.set_mode((self.APP_WIDTH, self.APP_HEIGHT))
        clock = pygame.time.Clock()

        self.bg = pygame.Surface((self.APP_WIDTH, self.APP_HEIGHT))
        self.bg.fill(BLACK)
        
        self.font = pygame.font.SysFont("dejavusans", 20)
        self.text_info = self.font.render("Escape : quit, space : paused, i : info, u / o : left/right walls", False, WHITE)

        self.is_paused = False
        self.is_running = True
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    quit() # for now, but it could launch an output screen for example
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        pygame.quit()
                        quit() # look above
                    if event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused
                    if event.key == pygame.K_i:
                        self.more_info_status = not self.more_info_status
                    if event.key == pygame.K_u:
                        self.walls[0].status = not self.walls[0].status
                    if event.key == pygame.K_o:
                        self.walls[1].status = not self.walls[1].status

            if not self.is_paused:
                self.simulation_time += 1 / self.FPS * self.time_speed_modifier
                self.collisions_counter += self.evolve()
                self.draw()
                clock.tick(self.FPS)
                pygame.display.update()

    def evolve(self):
        collisions = 0
        checked_collisions = []
        for block in self.blocks:
            block.move(self.time_speed_modifier)
            for wall in self.walls:
                if wall.status:
                    if wall.collide(block):
                        collisions += 1
                        block.vx *= -1
            for other_block in self.blocks:
                a = block
                b = other_block
                id_collision = (min(a.id, b.id), max(a.id, b.id))
                # due to some technical limits, we need to check if the collision is realistic
                # if we don't check, right after the blocks collide they will collide infinitely
                # if you don't understand just don't care, but keep in mind it's necessary to check
                collision_possible = False
                if (a.x <= b.x and a.vx > b.vx) or (a.x >= b.x and a.vx < b.vx) : # in the three possible collision types (-> -> / -> <- / <- <-) the left block velocity is bigger than right's one
                    collision_possible = True
                if a != b and id_collision not in checked_collisions and a.collide(b) and collision_possible:
                    collisions += 1
                    self.set_new_velocity(a, b)
                    checked_collisions.append(id_collision)
        return collisions

    def set_new_velocity(self, a, b):
        """
        This is the most important function of the prototype, this is here that we use dynamics.
        If you want to see the proof of these formulas, check the readme.
        """
        m = a.mass
        M = b.mass
        v_ra0 = a.vx
        v_rb0 = b.vx
        v_b0 = v_rb0 - v_ra0
        v_ra1 = 2 * M / (M + m) * v_b0 + v_ra0
        v_rb1 = (1 - 2 * m / (M + m)) * v_b0 + v_ra0
        a.vx = v_ra1
        b.vx = v_rb1

    def draw(self):
        self.app.blit(self.bg, (0, 0))
        for wall in self.walls:
            if wall.status:
                self.app.blit(wall.img, wall.rect)
        for block in self.blocks:
            self.app.blit(block.img, block.rect)
        self.app.blit(self.text_info, (20, 10))
        if self.more_info_status:
            text_collision = self.font.render("Collisions counter : {}".format(self.collisions_counter), False, WHITE)
            text_time = self.font.render("Time : {}s".format(round(self.simulation_time, 2)), False, WHITE)
            self.app.blit(text_collision, (20, 40))
            self.app.blit(text_time, (20, 70))
            for i, block in enumerate(self.blocks):
                text_block = self.font.render("Block #{} : {}m and {}m/s".format(i + 1, int(block.x),round(block.vx, 2)), False, block.color)
                self.app.blit(text_block, (20, 70 + 30 * (i + 1)))


def main():
    Simulation().run()

if __name__ == "__main__":
    main()