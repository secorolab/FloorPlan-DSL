import numpy as np


def get_intersection(a1, a2, b1, b2):
    # method source: https://stackoverflow.com/a/42727584

    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return float("inf"), float("inf")
    return x / z, y / z


def get_angle_between_vectors(v1, v2):
    # Adapted from https://stackoverflow.com/a/13849249
    u1 = _get_unit_vector(v1)
    u2 = _get_unit_vector(v2)

    sign = 1
    if u1[1] < 0:
        sign = -1
    return sign * np.arccos(np.dot(u1, u2))


def _get_unit_vector(vector):
    # Inputs need to be transformed to unit vectors so we can use np.arccos
    return vector / np.linalg.norm(vector)
