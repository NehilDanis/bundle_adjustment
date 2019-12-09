import bz2
import os
import urllib.request
import numpy as np

class Reader:
    def __init__(self, base_url_tmp: str, file_name_tmp: str):
        self.url = base_url_tmp + file_name_tmp
        self.file_name = file_name_tmp

        # if the file is not already downloaded, it will be retrieved from the url.
        if not os.path.isfile(self.file_name):
            urllib.request.urlretrieve(self.url, self.file_name)

    def readDataset(self):
        '''
            The data format in the dataset is shown below;

            <num_cameras> <num_points> <num_observations>

            <camera_index_1> <point_index_1> <x_1> <y_1>
            ...
            <camera_index_num_observations> <point_index_num_observations> <x_num_observations> <y_num_observations>

            <camera_1>
            ...
            <camera_num_cameras>

            <point_1>
            ...
            <point_num_points>

        '''
        with bz2.open(self.file_name, 'rt') as bz_file:
            # The same 3D point is observed by different cameras multiple times.
            num_cameras, num_3d_points, num_observation = map(int, bz_file.readline().split())
            
            # Here the order of the indices shows which camera used to observe
            # which point at a particular time moment.
            camera_indices =np.empty(num_observation, dtype=int)
            point_indices =np.empty(num_observation, dtype=int)
            projections_2d = np.empty((num_observation, 2))
            

            for i in range(num_observation):
                curr_camera_idx, curr_3d_point_idx, projected_x, projected_y = bz_file.readline().split()
                camera_indices[i] = int(curr_camera_idx)
                point_indices[i] = int(curr_3d_point_idx)
                projections_2d[i] = [float(projected_x), float(projected_y)]

            '''
            Each camera has 9 parameters.
            First 3 shows the rotation vector in lie algebra, so we can show the
            3x3 rotation matrix by 3x1 vector.

            The next 3 elements are for translation.

            The next one is the focal length.

            The last two parameters are the radial distortion.
            '''
            camera_params = np.empty(num_cameras * 9)
            for i in range(num_cameras * 9): 
                camera_params[i] = float(bz_file.readline())

            camera_params = camera_params.reshape((num_cameras, 9)) # The shape of camera parameters matrix is num_cameras x 9
            # 9 shows the parameters per camera.


            points_in_3d = np.empty(num_3d_points)
            for i in range(num_3d_points):
                points_in_3d[i] = float(bz_file.readline())

        return camera_indices, point_indices, camera_params, points_in_3d


