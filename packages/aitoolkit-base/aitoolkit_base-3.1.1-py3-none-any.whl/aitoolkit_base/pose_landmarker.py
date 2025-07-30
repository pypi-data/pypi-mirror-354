from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError
from .utils import ModelManager, VisUtil
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult
from mediapipe.framework.formats import landmark_pb2
from typing import List, Tuple
import numpy as np

class PoseLandmarker(BaseMediaPipeDetector):
    def __init__(self, num_poses=1, **kwargs):
        self.num_poses = num_poses
        super().__init__(**kwargs)

    def _initialize_detector(self):
        try:
            base_options = python.BaseOptions(model_asset_path=ModelManager.get_model_path('pose_landmarker.task'))
            options_args = {
                'base_options': base_options,
                'running_mode': self.running_mode,
                'num_poses': self.num_poses,
                'min_pose_detection_confidence': self.min_detection_confidence,
            }
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                options_args['result_callback'] = self._save_result
            
            options = vision.PoseLandmarkerOptions(**options_args)
            self.detector = vision.PoseLandmarker.create_from_options(options)
        except Exception as e:
            raise BaseMediaPipeError(f"初始化姿态检测器失败: {e}")

    def _process_result(self, detection_result, image_shape):
        return detection_result

    def draw(self, image: np.ndarray, results: PoseLandmarkerResult) -> np.ndarray:
        if not results or not results.pose_landmarks:
            return image
        vis_image = image.copy()
        for pose_landmarks in results.pose_landmarks:
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                for landmark in pose_landmarks
            ])
            vis_image = VisUtil.draw_pose_landmarks(vis_image, pose_landmarks_proto)
        return vis_image

    def get_landmarks(self, results: PoseLandmarkerResult) -> List[List[Tuple[int, int]]]:
        if not results or not results.pose_landmarks:
            return []
        landmarks_list = []
        if self._latest_frame is None:
            return []
        h, w, _ = self._latest_frame.shape
        for pose_landmarks in results.pose_landmarks:
            landmarks = []
            for landmark in pose_landmarks:
                landmarks.append((int(landmark.x * w), int(landmark.y * h)))
            landmarks_list.append(landmarks)
        return landmarks_list