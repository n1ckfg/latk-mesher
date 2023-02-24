import latk
import trimesh
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def create_tube(line, radius=0.1, segments=16):
    points = line.vertices
    distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
    cumulative_distances = np.concatenate([[0], np.cumsum(distances)])
    num_points = len(points)
    
    radii = np.full(num_points, radius)
    
    faces = []
    for i in range(num_points - 1):
        start_index = i * segments
        end_index = (i + 1) * segments
        for j in range(segments):
            p1 = start_index + j
            p2 = start_index + ((j + 1) % segments)
            p3 = end_index + j
            p4 = end_index + ((j + 1) % segments)
            faces.append([p1, p2, p3])
            faces.append([p2, p4, p3])
    
    vertices = []
    for i in range(num_points):
        for j in range(segments):
            theta = 2 * np.pi * j / segments
            r = radii[i]
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = cumulative_distances[i]
            vertices.append([x, y, z])
    
    tube = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    x_axis = np.array([1, 0, 0])
    direction = np.diff(points, axis=0)[0]
    angle = np.arccos(np.dot(direction, x_axis) / np.linalg.norm(direction))
    axis = np.cross(direction, x_axis)
    tube.apply_transform(trimesh.transformations.rotation_matrix(angle, axis))
    
    return tube

def test_tube():
    line1 = trimesh.load_path(np.array([[0, 0, 0], [1, 0, 0], [2, 1, 0]]))
    line2 = trimesh.load_path(np.array([[0, 0, 0], [0, 1, 0], [0, 2, 1]]))
    tube1 = create_tube(line1)
    tube2 = create_tube(line2)
    return tube1, tube2
    