import numpy as np
import pygame as pg
import sys
from figures import *
from drawer import Drawer
import transformations as xforms

from time import time


class Render:
    def __init__(self):
        pg.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1920, 1080
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        Drawer.screen = self.screen

        self.global_origin = np.array((self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, 0, 1), dtype="float64")

        self.transformation_matrix = np.identity(4, dtype="float64")
        self.transformation_matrix[1][1] = -1

        self.figures = []

        self.mouseClicked = {"l": False, "r": False}

        self.timer_duration = 2000
        self.start_time = pg.time.get_ticks()

        self.clock = pg.time.Clock()

        self.create()

    def create(self):
        cube = Cube(size=200)
        cube.color = (255, 215, 0)

        n = 1000
        butterfly = RandonPoints(n)
        butterfly.update_points(ftype="butterfly", r=100)
        butterfly.rotate(axes="X", angle=-45)

        sphere2 = RandonPoints(n)
        sphere2.update_points(ftype="sphere", r=100)
        sphere2.local_origin = np.array((0, 0, 0, 1), dtype="float64")

        sphere3 = RandonPoints(n)
        sphere3.color = np.array((152, 0, 15))
        sphere3.update_points(ftype="sphere", r=500)
        sphere3.rotate(axes="X", angle=27)
        sphere3.local_origin = np.array((3000, 0, 0, 1), dtype="float64")

        xforms.rotate(sphere3.local_origin, axes="Z", angle=216)

        self.figures = [cube, butterfly, sphere2, sphere3]

    def run(self, fps):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.transformation_matrix = np.identity(4, dtype="float64")
                        self.transformation_matrix[1][1] = -1

                elif event.type == pg.MOUSEWHEEL:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    mouse_x -= self.global_origin[0]
                    mouse_y -= self.global_origin[1]

                    self.move(-mouse_x, -mouse_y)
                    if event.y > 0:
                        self.scale(1.25)

                    elif event.y < 0:
                        self.scale(0.75)
                    self.move(mouse_x, mouse_y)

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouseClicked["l"] = True
                    elif event.button == 3:
                        self.mouseClicked["r"] = True

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouseClicked["l"] = False
                    elif event.button == 3:
                        self.mouseClicked["r"] = False

                elif event.type == pg.MOUSEMOTION:
                    if self.mouseClicked["l"]:
                        self.rotate(axes="X", angle=-event.rel[1])
                        self.rotate(axes="Y", angle=event.rel[0])

                    elif self.mouseClicked["r"]:
                        self.move(event.rel[0], event.rel[1])

            self.draw()

            self.figures[1].rotate(axes="X", angle=np.cos(time() * 10))
            self.figures[2].rotate(axes="Z", angle=0.2)
            self.figures[2].rotate(axes="X", angle=0.2)

            self.clock.tick(fps)

    def draw(self):
        for fig in self.figures:
            fig.transform_points()
            for i, p in enumerate(fig.transformed_points):
                fig.transformed_points[i] = self.transformation_matrix.dot(p) + self.global_origin
        Drawer.draw(self.figures, self.clock.get_fps())

    def rotate(self, axes, angle):
        xforms.rotate(self.transformation_matrix, axes, angle)

    def scale(self, size):
        xforms.scale(self.transformation_matrix, size)

    def move(self, dx, dy, dz=0):
        xforms.move(self.transformation_matrix, dx, dy, dz)
