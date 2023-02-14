#-*- coding: utf-8 -*-

import numpy as np


def get_ABCD_free_space(dx=1e-3):

    ret = np.array([
        [1, dx],
        [0, 1]
    ])

    return ret


class Ray():

    def __init__(self, r0, theta0):

        self.r0 = r0
        self.theta0 = theta0

        self.rs = [self.r0]
        self.thetas = [self.theta0]

    def propagate_add(self, M):

        v = np.array([self.rs[-1], self.thetas[-1]])
        v = np.dot(M, v)

        self.rs.append(v[0])
        self.thetas.append(v[1])

    def propagate_change(self, M):

        v = np.array([self.rs[-1], self.thetas[-1]])
        v = np.dot(M, v)

        self.rs[-1] = v[0]
        self.thetas[-1] = v[1]

    def clear(self):

        self.rs = [self.r0]
        self.thetas = [self.theta0]


class Rays():

    def __init__(self):

        self._rays = []

    def add_ray(self, ray):

        self._rays.append(ray)

    def propagate(self, geometry, lenses=[], dx=1e-3):

        xMax = geometry['X range']

        xs = np.arange(0, xMax, step=1e-3)

        M_free_space = get_ABCD_free_space(dx)

        for ray in self._rays:
            ray.clear()
            for i, x in enumerate(xs):
                # Propagation
                # Lenses
                for lens in lenses:
                    if lens.validate_position(x, dx):
                        ray.propagate_change(lens.get_ABCD())
                # Free space
                ray.propagate_add(M_free_space)

        # Intensity
        ys_list = [np.array(ray.rs[:-1]) for ray in self._rays]

        return xs, ys_list


class Lens():

    def __init__(self, name, f=50, position=10):

        self._name = name
        self.f = f
        self.position = position

        self._ABCD = np.array([
            [1, 0],
            [-1/self.f, 1]
        ])

    def get_ABCD(self):

        return self._ABCD

    def validate_position(self, x, dx):

        xMin = self.position - 0.5*dx
        xMax = self.position + 0.5*dx

        if x >= xMin and x < xMax:
            return True
        else:
            return False