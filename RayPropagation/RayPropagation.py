#-*- coding: utf-8 -*-

import numpy as np


def get_ABCD_free_space(dx=1e-4):

    ret = np.array([
        [1, dx],
        [0, 1]
    ])

    return ret

def find_imaging_planes(xs, lenses, dx=1e-4, B_threshold=1e-5):

    # Propagation
    M = np.identity(2)
    ret = []
    for i, x in enumerate(xs):
        # Propagation
        # Lenses
        for lens in lenses:
            if lens.validate_position(x, dx):
                M = np.dot(M, lens.get_ABCD())
        # Free space
        M = np.dot(M, get_ABCD_free_space(dx))

        if np.abs(M[0,1]) < B_threshold:
            ret.append({
                'x': x,
                'A': M[0,0],
                'B': M[0,1],
                'C': M[1,0],
                'D': M[1,1]
            })

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

    def propagate(self, geometry, lenses=[], dx=1e-4):

        xMax = geometry['X range']

        xs = np.arange(0, xMax, step=dx)

        M_free_space = get_ABCD_free_space(dx)

        for ray in self._rays:
            ray.clear()
            for i, x in enumerate(xs):
                # Propagation
                # Lenses
                for lens in lenses:
                    if lens.validate_position(x, dx):
                        ray.propagate_change(lens.get_ABCD())
                        if not lens.validate_aperture(ray.rs[-1]):
                            ray.rs[-1] = np.nan
                # Free space
                ray.propagate_add(M_free_space)

        # Intensity
        ys_list = [np.array(ray.rs[:-1]) for ray in self._rays]

        return xs, ys_list


class Lens():

    def __init__(self, name, f=50, position=10, aperture=25.4):

        self._name = name
        self.f = f
        self.position = position
        self.aperture = aperture

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

    def validate_aperture(self, r):

        if r < -0.5*self.aperture or r > 0.5*self.aperture:
            return False
        else:
            return True