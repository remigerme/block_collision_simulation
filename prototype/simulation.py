import pygame
from block import Block
from wall import Wall
from color import *


class Simulation:
    def __init__(self, settings):
        # basic properties
        self.APP_WIDTH = settings["window"]["width"]
        self.APP_HEIGHT = settings["window"]["height"]
        self.FPS = settings["window"]["fps"]

        # physical objects
        self.wall_size = (settings["walls"]["width"], settings["walls"]["height"])
        self.walls = [
                    Wall((0, self.APP_HEIGHT - self.wall_size[1]), self.wall_size),
                    Wall((self.APP_WIDTH - self.wall_size[0], self.APP_HEIGHT - self.wall_size[1]), self.wall_size)
                    ]
        self.blocks = []
        for block in settings["blocks"]:
            self.blocks.append(Block(block["mass"], block["x"], block["vx"], self.FPS, self.APP_HEIGHT, block["color"].upper()))

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
        self.text_info = self.font.render("Esc:quit, space:paused, i:info, u/o:walls, l/r arrows:time speed", False, WHITE)

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
                    if event.key == pygame.K_LEFT:
                        if 0.01 < self.time_speed_modifier <= 0.10:
                            self.time_speed_modifier = round(self.time_speed_modifier - 0.01, 3)
                        elif self.time_speed_modifier > 0.10:
                            self.time_speed_modifier = round(self.time_speed_modifier - 0.10, 3)
                    if event.key == pygame.K_RIGHT:
                        if self.time_speed_modifier < 0.10:
                            self.time_speed_modifier = round(self.time_speed_modifier + 0.01, 3)
                        else:
                            self.time_speed_modifier = round(self.time_speed_modifier + 0.10, 3)

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
            collide = False
            for wall in self.walls:
                if wall.status:
                    if wall.collide(block):
                        collisions += 1
                        collide = True
                        block.vx *= -1
            for other_block in self.blocks:
                a = block
                b = other_block # see in a future update
                id_collision = (min(a.id, b.id), max(a.id, b.id))
                # due to some technical limits, we need to check if the collision is realistic
                # if we don't check, right after the blocks collide they will collide infinitely
                collision_possible = False
                if (a.x <= b.x and a.vx > b.vx) or (a.x >= b.x and a.vx < b.vx) : # in the three possible collision types (-> -> / -> <- / <- <-) the left block velocity is bigger than right's one
                    collision_possible = True
                if a != b and id_collision not in checked_collisions and a.collide(b) and collision_possible:
                    collisions += 1
                    collide = True
                    self.set_new_velocity(a, b)
                    checked_collisions.append(id_collision)
                elif id_collision in checked_collisions:
                    collide = True
            if not collide: # if the blocks collide during this frame, we don't move it
                a.move(self.time_speed_modifier)
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
            text_time_speed_modifier = self.font.render("Time speed modifier : {}".format(round(self.time_speed_modifier, 3)), False, WHITE)
            text_collision = self.font.render("Collisions counter : {}".format(self.collisions_counter), False, WHITE)
            text_time = self.font.render("Time : {}s".format(round(self.simulation_time, 2)), False, WHITE)
            self.app.blit(text_time_speed_modifier, (20, 40))
            self.app.blit(text_collision, (20, 70))
            self.app.blit(text_time, (20, 100))
            for i, block in enumerate(self.blocks):
                text_block = self.font.render("Block #{} : {}m and {}m/s".format(i + 1, int(block.x),round(block.vx, 2)), False, block.color)
                self.app.blit(text_block, (20, 100 + 30 * (i + 1)))