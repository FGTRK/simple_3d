import numpy as np

"""
tensor maybe vector or matrix 
"""


def rotate(tensor, axes, angle):
    angle = np.deg2rad(angle)
    rotation_matrix = None

    if axes == "X":
        rotation_matrix = np.array([[1, 0, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle), 0],
                                    [0, np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 0, 1]], dtype="float64")

    elif axes == "Y":
        rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle), 0],
                                    [0, 1, 0, 0],
                                    [-np.sin(angle), 0, np.cos(angle), 0],
                                    [0, 0, 0, 1]], dtype="float64")

    elif axes == "Z":
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                                    [np.sin(angle), np.cos(angle), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], dtype="float64")

    np.dot(rotation_matrix, tensor, out=tensor)


def scale(tensor, size):
    scaling_matrix = np.array([[size, 0, 0, 0],
                               [0, size, 0, 0],
                               [0, 0, size, 0],
                               [0, 0, 0, 1]], dtype="float64")

    np.dot(scaling_matrix, tensor, out=tensor)


def move(tensor, dx, dy, dz):
    movement_matrix = np.array([[1, 0, 0, dx],
                                [0, 1, 0, dy],
                                [0, 0, 1, dz],
                                [0, 0, 0, 1]], dtype="float64")
    np.dot(movement_matrix, tensor, out=tensor)
