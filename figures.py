from random import randint, randrange, uniform
import numpy as np
import transformations as xforms


class Figure:
    def __init__(self, color=np.array((255, 255, 255))):
        self.type = "figure"
        self.color = color
        self.local_origin = np.array([0, 0, 0, 1], dtype="float64")
        self.transformation_matrix = np.identity(4, dtype="float64")
        self.raw_points = []
        self.transformed_points = []

    def transform_points(self):
        self.transformed_points = [p.dot(self.transformation_matrix) + self.local_origin for p in self.raw_points]

    def rotate(self, axes, angle):
        xforms.rotate(self.transformation_matrix, axes, angle)

    def scale(self, size):
        xforms.scale(self.transformation_matrix, size)

    def move(self, dx, dy, dz=0):
        xforms.move(self.transformation_matrix, dx, dy, dz)


class Cube(Figure):
    def __init__(self, size):
        super().__init__()
        self.type = "cube"
        hsize = size / 2
        self.raw_points = [np.array((hsize, hsize, hsize, 1), dtype="float64"),
                           np.array((hsize, -hsize, hsize, 1), dtype="float64"),
                           np.array((-hsize, -hsize, hsize, 1), dtype="float64"),
                           np.array((-hsize, hsize, hsize, 1), dtype="float64"),
                           np.array((hsize, hsize, -hsize, 1), dtype="float64"),
                           np.array((hsize, -hsize, -hsize, 1), dtype="float64"),
                           np.array((-hsize, -hsize, -hsize, 1), dtype="float64"),
                           np.array((-hsize, hsize, -hsize, 1), dtype="float64"),
                           ]


class RandonPoints(Figure):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.raw_points = [np.array((randint(-100, 100), randint(-100, 100), randint(-100, 100), 1), dtype="float64")
                           for _ in range(self.number)]

    def update_points(self, ftype=None, r=100):

        if ftype == "ball":
            self.raw_points = [np.array((randint(-r, r), randint(-r, r), randint(-r, r), 1), dtype="float64") for _ in
                               range(self.number)]

            i = 0
            while i < len(self.raw_points):
                if np.linalg.norm(self.raw_points[i]) > r:
                    self.raw_points.pop(i)
                else:
                    i += 1

        elif ftype == "sphere":
            self.raw_points = [np.array((r * np.sin(theta := np.deg2rad(randrange(0, 179, 1)))
                                         * np.cos(phi := np.deg2rad(randrange(0, 359, 9))),
                                         r * np.sin(theta) * np.sin(phi),
                                         r * np.cos(theta), 1), dtype="float64") for _ in range(self.number)]

        elif ftype == "butterfly":
            self.raw_points = [np.array((
                25 * np.sin(t := (uniform(0, 12))) * (k := (np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12) ** 5)),
                25 * np.cos(t) * k, 0, 1),
                dtype="float64") for _ in range(self.number)]

        else:
            self.raw_points = [np.array((randint(-r, r), randint(-r, r), randint(-r, r), 1), dtype="float64") for _ in
                               range(self.number)]


class Point(Figure):
    def __init__(self, x, y, z, r, color):
        super().__init__(color)

        self.type = "point"
        self.raw_points = [np.array((x, y, z, 1), dtype="float64")]
        self.radius = r
