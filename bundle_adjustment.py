from reader import Reader
import numpy as np
import matplotlib.pyplot as plt

# given rotation vec represents rotation in lie algebra, we can apply
# rodrigues formula and transform it to lie group.
def calculate_rotation_by_rodrigues_formula(rotation_vecs, points_in_3d):
    rot_vec_norms = np.linalg.norm(rotation_vecs, axis=1)[:, np.newaxis] # calculated the norm of 
    # each row
    # np.newaxis function is used to add one more dimension to the existing data. 
    # This way we will have N*1 matrix.
    
    rotation_vecs_unit = rotation_vecs / rot_vec_norms
    cos_theta = np.cos(rotation_vecs_unit)
    sin_theta = np.sin(rotation_vecs_unit)

    return 1 + rot_vec_norms*sin_theta + rot_vec_norms * rot_vec_norms * (1 - cos_theta)

def world_to_pixel_coordinates(camera_params, points_in_3d):
    num_observations = camera_params.shape[0]
    rotation = camera_params[:, 0:3]
    translation = camera_params[:, 3:6]

    rot = calculate_rotation_by_rodrigues_formula(rotation, points_in_3d)
    translated_rotated_points = np.cross(points_in_3d, rot) + translation

    # 3d points projected in 2d.
    radial_undistort_2d = -1 * np.divide(translated_rotated_points[:, 0:2], (translated_rotated_points[:, 2])[:, np.newaxis]) 

    undistorted_norm = np.linalg.norm(radial_undistort_2d)
    norm_square = undistorted_norm * undistorted_norm
    f = camera_params[:, 6]
    k1 = camera_params[:, 7]
    k2 = camera_params[:, 8]
    return (1 + k1 * norm_square + k2 * norm_square * norm_square)[:, np.newaxis] * f[:, np.newaxis] * radial_undistort_2d


def projection(camera_params, camera_indices, projections_2d, point_indices, points_in_3d):
    pixel_coordinates = world_to_pixel_coordinates(camera_params[camera_indices], points_in_3d[point_indices])
    err = (pixel_coordinates - projections_2d).ravel()
    return err


if __name__ == "__main__":
    BASE_URL = "http://grail.cs.washington.edu/projects/bal/data/ladybug/"
    FILE_NAME = "problem-49-7776-pre.txt.bz2"
    reader = Reader(BASE_URL, FILE_NAME)
    camera_indices, point_indices, camera_params, projections_2d, points_in_3d = reader.readDataset()
    proj_err = projection(camera_params, camera_indices, projections_2d, point_indices, points_in_3d)
    plt.plot(proj_err)
    plt.show()
    
