# Copyright 2021 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""MediaPipe Face Geometry."""

from typing import NamedTuple, Union, Tuple
import math

import numpy as np

from mediapipe.modules.face_geometry.protos import environment_pb2
from mediapipe.modules.face_geometry.protos import face_geometry_pb2
# pylint: disable=unused-import
from mediapipe.modules.face_geometry import geometry_pipeline_calculator_pb2
# pylint: enable=unused-import
from mediapipe.python.solution_base import SolutionBase

FACE_GEOMETRY_FROM_LANDMARKS_GRAPH_FILE_PATH = 'mediapipe/modules/face_geometry/face_geometry_from_landmarks_cpu' \
                                               '.binarypb'
FACE_GEOMETRY_FROM_DETECTION_GRAPH_FILE_PATH = 'mediapipe/modules/face_geometry/face_geometry_from_detection_cpu' \
                                               '.binarypb'

def expand_transformation_matrix(
        face_geometry: face_geometry_pb2.FaceGeometry) -> Union[None, Tuple[np.ndarray, np.ndarray]]:
    if not face_geometry:
        return None

    pose_transform_matrix = face_geometry.pose_transform_matrix

    rotation_matrix = np.zeros((3, 3))
    translation_vector = np.zeros((3, 1))

    rotation_matrix[0, 0] = pose_transform_matrix.packed_data[0]
    rotation_matrix[1, 0] = pose_transform_matrix.packed_data[1]
    rotation_matrix[2, 0] = pose_transform_matrix.packed_data[2]

    rotation_matrix[0, 1] = pose_transform_matrix.packed_data[4]
    rotation_matrix[1, 1] = pose_transform_matrix.packed_data[5]
    rotation_matrix[2, 1] = pose_transform_matrix.packed_data[6]

    rotation_matrix[0, 2] = pose_transform_matrix.packed_data[8]
    rotation_matrix[1, 2] = pose_transform_matrix.packed_data[9]
    rotation_matrix[2, 2] = pose_transform_matrix.packed_data[10]

    translation_vector[0, 0] = pose_transform_matrix.packed_data[12]
    translation_vector[1, 0] = pose_transform_matrix.packed_data[13]
    translation_vector[2, 0] = pose_transform_matrix.packed_data[14]

    return rotation_matrix, translation_vector


def get_euler_angles(face_geometry: face_geometry_pb2.FaceGeometry) -> Union[None, np.ndarray]:
    if not face_geometry:
        return None

    rotation_matrix, translation_vector = expand_transformation_matrix(face_geometry)

    def rotation_matrix_to_euler_angles(rot):

        sy = math.sqrt(rot[0, 0] * rot[0, 0] + rot[1, 0] * rot[1, 0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(rot[2, 1], rot[2, 2])
            y = math.atan2(-rot[2, 0], sy)
            z = math.atan2(rot[1, 0], rot[0, 0])
        else:
            x = math.atan2(-rot[1, 2], rot[1, 1])
            y = math.atan2(-rot[2, 0], sy)
            z = 0

        # Angle given here is inverted compared to ML Kit, so we multiply by -1
        return np.array([-math.degrees(x), -math.degrees(y), -math.degrees(z)])

    return rotation_matrix_to_euler_angles(rotation_matrix)


class FaceGeometry(SolutionBase):
    def __init__(self,
                 num_faces=1,
                 from_detection=False,
                 env_origin_point_location="TOP_LEFT_CORNER",
                 env_perspective_camera_vertical_fov_degrees=63.0,  # 63 degrees
                 env_perspective_camera_near=1.0,  # 1cm
                 env_perspective_camera_far=10000.0,  # 100m
                 ):

        binary_graph_path = (FACE_GEOMETRY_FROM_LANDMARKS_GRAPH_FILE_PATH if not from_detection
                             else FACE_GEOMETRY_FROM_DETECTION_GRAPH_FILE_PATH)

        outputs = (['multi_face_landmarks', 'multi_face_geometry'] if not from_detection
                   else ['multi_face_landmarks', 'detections'])

        environment = environment_pb2.Environment(
            origin_point_location=env_origin_point_location,
            perspective_camera={
                "vertical_fov_degrees": env_perspective_camera_vertical_fov_degrees,
                "near": env_perspective_camera_near,
                "far": env_perspective_camera_far,
            })

        super().__init__(
            binary_graph_path=binary_graph_path,
            side_inputs={
                "environment": environment,
                "num_faces": num_faces
            },
            outputs=outputs)

    def process(self, image: np.ndarray) -> NamedTuple:

        return super().process(input_data={'image': image})
