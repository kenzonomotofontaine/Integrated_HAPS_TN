import numpy as np
import scipy.stats

from parameters import Parameters

class Points_Circle_Mesh:
    def __init__(self) -> None:
        self.radius = np.array([Parameters.Mesh_sample*i for i in range(int(Parameters.Mesh_rad/Parameters.Mesh_sample)+1)])
        self.pts_per_circle = np.array([6*i for i in range(len(self.radius))])
        self.pts_per_circle[0] = 1
        self.Nb_points = np.sum(self.pts_per_circle)

    def generate_points(self, rad, num_points):
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        x = rad * np.cos(angles)
        y = rad * np.sin(angles)
        return list(zip(x, y))

    def get_mesh_points(self):
        mesh_points = []
        for rad, num_points in zip(self.radius, self.pts_per_circle):
            circle_points = self.generate_points(rad, num_points)
            mesh_points.extend(circle_points)
        return np.array(mesh_points)


class Points_Square_Mesh:
    def __init__(self) -> None:
        self.rad = Parameters.Mesh_rad
        self.sample = Parameters.Mesh_sample

    def get_mesh_points(self):
        x = np.linspace(-self.rad, self.rad, int(self.rad/self.sample)*2+1)
        y = np.linspace(-self.rad, self.rad, int(self.rad/self.sample)*2+1)
        return np.array([[x[i], y[j]] for j in range(len(y)) for i in range(len(x))])


class Station_Circle_Mesh:
    def __init__(self) -> None:
        self.radius = np.array([12.5, 37.5, 62.5, 87.5])
        self.pts_per_circle = np.array([2, 7, 9, 14])
        self.Nb_points = np.sum(self.pts_per_circle)

    def generate_tbs(self, rad, num_points):
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        x = rad * np.cos(angles)
        y = rad * np.sin(angles)
        h = 0.05*np.ones(num_points)
        return list(zip(x, y, h))
    
    def get_mesh_stations(self):
        mesh_tbs = []
        for rad, num_points in zip(self.radius, self.pts_per_circle):
            circle_tbs = self.generate_tbs(rad, num_points)
            mesh_tbs.extend(circle_tbs)
        return np.array(mesh_tbs)
    
class Station_Circle_Mesh_Poisson:
    def __init__(self) -> None:
        self.radius = np.array([12.5, 37.5, 62.5, 87.5])
        self.pts_per_circle = np.array([2, 7, 9, 14])
        self.Nb_points = np.sum(self.pts_per_circle)

    def generate_tbs(self, rad, num_points):
        angles = 2*np.pi*scipy.stats.uniform.rvs(0,1,((num_points,1)))
        x = rad * np.cos(angles)
        y = rad * np.sin(angles)
        h = 0.03*scipy.stats.uniform.rvs(0,1,((num_points,1))) + 0.03
        return list(zip(x, y, h))
    
    def get_mesh_stations(self):
        mesh_tbs = []
        for rad, num_points in zip(self.radius, self.pts_per_circle):
            circle_tbs = self.generate_tbs(rad, num_points)
            mesh_tbs.extend(circle_tbs)
        return np.array(mesh_tbs)
    
