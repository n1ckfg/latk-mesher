import numpy as np
import trimesh
from shapely.geometry import Polygon
import latk

la = latk.Latk("test.latk")
la_layer = la.layers[0]

sweep_size=0.015
sweep_polygon_points = np.array([[-sweep_size, -sweep_size], [sweep_size, -sweep_size], [sweep_size, sweep_size], [-sweep_size, sweep_size]])
sweep_polygon = Polygon(sweep_polygon_points)

for i, la_frame in enumerate(la_layer.frames):
	mesh = trimesh.base.Trimesh()
	
	for la_stroke in la_frame.strokes:
		points = []
		
		for la_point in la_stroke.points:
			co = la_point.co
			points.append([co[0], co[2], co[1]])
		
		points = np.array(points)

		stroke_mesh = trimesh.creation.sweep_polygon(sweep_polygon, path=points, cap_ends=True)
		
		vertices = np.concatenate((mesh.vertices, stroke_mesh.vertices))
		faces = np.concatenate((mesh.faces, stroke_mesh.faces + len(mesh.vertices)))
		mesh = trimesh.Trimesh(vertices, faces)

	mesh.export("test" + str(i) + ".ply")
