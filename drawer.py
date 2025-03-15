import pygame as pg
from random import randint, uniform

r, g, b = 66, 99, 77


class Drawer:
    screen = None

    @staticmethod
    def draw(figures, fps):
        pg.display.set_caption(f"fps: {fps}")
        Drawer.screen.fill((0, 0, 0))

        for fig in figures:
            if fig.type == "figure":
                for p in fig.transformed_points:
                    pg.draw.circle(Drawer.screen,
                                   # (102, 43, 45),
                                   (randint(0, 255), randint(0, 255), randint(0, 255)),
                                   (p[0], p[1]), 1.7)

            elif fig.type == "cube":
                pg.draw.lines(Drawer.screen, fig.color, True,
                              [(fig.transformed_points[i][0],
                                fig.transformed_points[i][1]) for i in range(4)])

                pg.draw.lines(Drawer.screen, fig.color, True,
                              [(fig.transformed_points[i][0],
                                fig.transformed_points[i][1]) for i in range(4, 8)])

                for i in range(4):
                    pg.draw.line(Drawer.screen, fig.color,
                                 (fig.transformed_points[i][0], fig.transformed_points[i][1]),
                                 (fig.transformed_points[i + 4][0], fig.transformed_points[i + 4][1])
                                 )

            elif fig.type == "point":
                pg.draw.circle(Drawer.screen, fig.color, fig.transformed_points[0][:2], fig.radius)

        pg.display.flip()
