from reader import Reader
import numpy as np


def perspective_projection(camera_params, points_in_3d):
    num_observations = camera_params.shape[0]
    rotation = camera_params[:, 0:3]
    translation = camera_params[:, 3:6]
    f = camera_params[:, 6]
    k1 = camera_params[:, 7]
    k2 = camera_params[:, 8]
    
    pass


def projection(camera_params, camera_indices, projections_2d, point_indices, points_in_3d):
    perspective_projection(camera_params[camera_indices], points_in_3d[point_indices])
    


if __name__ == "__main__":
    BASE_URL = "http://grail.cs.washington.edu/projects/bal/data/ladybug/"
    FILE_NAME = "problem-49-7776-pre.txt.bz2"
    reader = Reader(BASE_URL, FILE_NAME)
    camera_indices, point_indices, camera_params, projections_2d, points_in_3d = reader.readDataset()
    projection(camera_params, camera_indices, projections_2d, point_indices, points_in_3d)
    
