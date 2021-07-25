# Copyright 2020 The MediaPipe Authors.
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

load(
    "//mediapipe/framework/tool:mediapipe_graph.bzl",
    "mediapipe_simple_subgraph",
)

licenses(["notice"])

package(default_visibility = ["//visibility:public"])

mediapipe_simple_subgraph(
    name = "eyes_landmark_cpu",
    graph = "eyes_landmark_cpu.pbtxt",
    register_as = "EyesLandmarkCpu",
    deps = [
        "//mediapipe/calculators/core:clip_vector_size_calculator",
        "//mediapipe/calculators/core:split_vector_calculator",
        "//mediapipe/calculators/image:image_cropping_calculator",
        "//mediapipe/calculators/image:image_properties_calculator",
        "//mediapipe/calculators/image:image_transformation_calculator",
    ],
)

mediapipe_simple_subgraph(
    name = "eyes_detector_left_and_right_cpu",
    graph = "eyes_detector_left_and_right_cpu.pbtxt",
    register_as = "EyesDetectorLeftAndRightCpu",
    deps = [
        ":eyes_landmark_cpu",
        ":eyes_landmark_landmarks_to_roi",
        "//mediapipe/calculators/core:constant_side_packet_calculator",
        "//mediapipe/calculators/core:side_packet_to_stream_calculator",
        "//mediapipe/calculators/image:color_convert_calculator",
        "//mediapipe/calculators/image:image_properties_calculator",
    ],
)

mediapipe_simple_subgraph(
    name = "eyes_landmark_landmarks_to_roi",
    graph = "eyes_landmark_landmarks_to_roi.pbtxt",
    register_as = "EyesLandmarkLandmarksToRoi",
    deps = [
        "//mediapipe/calculators/util:detections_to_rects_calculator",
        "//mediapipe/calculators/util:landmarks_to_detection_calculator",
        "//mediapipe/calculators/util:rect_transformation_calculator",
    ],
)
