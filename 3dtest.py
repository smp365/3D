import pyrender
import numpy as np
import trimesh
import imageio

# Load the 3D model
loaded = trimesh.load('table2.obj')

# Create a scene
scene = pyrender.Scene()

# Check if the loaded object is a scene (i.e., contains multiple meshes)
if isinstance(loaded, trimesh.Scene):
    # Add each mesh in the scene to the pyrender scene
    for mesh in loaded.geometry.values():
        scene.add(pyrender.Mesh.from_trimesh(mesh))
else:
    # Add the single mesh to the pyrender scene
    scene.add(pyrender.Mesh.from_trimesh(loaded))

# Set the camera parameters
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)

# Define the rotation angles (in radians)
rotation_angle_x = -45* np.pi / 180  # -45 degrees
rotation_angle_y = 45* np.pi / 180  # 45 degrees
rotation_angle_z = 0* np.pi / 180  # 45 degrees

# Create the rotation matrices
rotation_matrix_x = np.array([
    [1, 0, 0, 0],
    [0, np.cos(rotation_angle_x), -np.sin(rotation_angle_x), 0],
    [0, np.sin(rotation_angle_x), np.cos(rotation_angle_x), 0],
    [0, 0, 0, 1]
])

rotation_matrix_y = np.array([
    [np.cos(rotation_angle_y), 0, np.sin(rotation_angle_y), 0],
    [0, 1, 0, 0],
    [-np.sin(rotation_angle_y), 0, np.cos(rotation_angle_y), 0],
    [0, 0, 0, 1]
])

rotation_matrix_z = np.array([
    [np.cos(rotation_angle_y), 0, np.sin(rotation_angle_y), 0],
    [0, 1, 0, 0],
    [-np.sin(rotation_angle_y), 0, np.cos(rotation_angle_y), 0],
    [0, 0, 0, 1]
])

print("x", rotation_matrix_x)
print("y", rotation_matrix_y)
print("y dot x", np.dot(rotation_matrix_y, rotation_matrix_x))
print("x dot y",np.dot(rotation_matrix_x, rotation_matrix_y))

# Combine the rotation matrices
#rotation_matrix = np.dot(rotation_matrix_y, rotation_matrix_x)
rotation_matrix = np.dot(rotation_matrix_x, rotation_matrix_y)
#rotation_matrix = rotation_matrix_y.dot(rotation_matrix_x)

# Create the translation matrix
translation_matrix = np.array([
    [1, 0, 0, 2],
    [0, 1, 0, 2],
    [0, 0, 1, 2],
    [0, 0, 0, 1]
])

# Combine the rotation and translation matrices
transformation_matrix = np.dot(translation_matrix, rotation_matrix)

'''
s = np.sqrt(2)/2
camera_pose = np.array([
    [0.0, -s,   s,   0.3],
    [1.0,  0.0, 0.0, 0.0],
    [0.0,  s,   s,   0.35],
    [0.0,  0.0, 0.0, 1.0],
])

# x rotation 45 degree, x move 5, y 15, z 15
camera_pose = np.array([
    [1.0,  0.0, 0.0, 5.0],
    [0.0,  s,   s,   15.0],
    [0.0,  -s,  s,   15.0],
    [0.0,  0.0, 0.0, 1.0],
])
'''

camera_pose = transformation_matrix

scene.add(camera, pose=camera_pose)

# Render the scene
renderer = pyrender.OffscreenRenderer(640, 480)
color, depth = renderer.render(scene)

# Save the rendered image
imageio.imwrite('table_yr45xr-45_x2y2z2.png', color)
