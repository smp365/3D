import numpy as np
import open3d as o3d
# import imageio # has problem on my Mac

# Assuming depth_image is a 2D numpy array containing your depth map image
# depth_image = imageio.imread('14_dining table_isolated_object_depth_map.pfm')
from read_pfm import read_pfm
depth_image = read_pfm('14_dining table_isolated_object_depth_map.pfm')

# Scale the depth values to represent real-world distances
max_real_world_distance = 10  # meters
scaling_factor = max_real_world_distance / np.max(depth_image)
depth = depth_image * scaling_factor

# Assuming depth is a 2D numpy array containing your depth map
# fx, fy are the focal lengths and cx, cy are the optical centers

height, width = depth.shape
fx, fy = 525.0, 525.0  # example values
cx, cy = width / 2, height / 2  # example values

# Create x, y coordinates
x = np.linspace(0, width - 1, width)
y = np.linspace(0, height - 1, height)
x, y = np.meshgrid(x, y)

# Normalize x, y coordinates
x_norm = (x - cx) / fx
y_norm = (y - cy) / fy

# Create 3D points
xyz = np.zeros((height, width, 3), dtype=np.float32)
xyz[..., 0] = x_norm * depth
xyz[..., 1] = y_norm * depth
xyz[..., 2] = depth

# Convert to point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz.reshape(-1, 3))

# Visualize point cloud
#o3d.visualization.draw_geometries([pcd])

# Save point cloud to a file
o3d.io.write_point_cloud('point_cloud.ply', pcd)
