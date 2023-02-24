import numpy as np
import trimesh
from shapely.geometry import Polygon

points = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])

sweep_size=0.05

sweep_polygon_points = np.array([[-sweep_size, -sweep_size], [sweep_size, -sweep_size], [sweep_size, sweep_size], [-sweep_size, sweep_size]])

sweep_polygon = Polygon(sweep_polygon_points)

mesh = trimesh.creation.sweep_polygon(sweep_polygon, path=points, cap_ends=True)

mesh.show()