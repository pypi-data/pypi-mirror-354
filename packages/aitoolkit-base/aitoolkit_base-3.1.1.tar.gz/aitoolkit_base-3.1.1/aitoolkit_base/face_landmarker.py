from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError
from .utils import ModelManager, VisUtil
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarkerResult
from mediapipe.framework.formats import landmark_pb2
from typing import List, Tuple
import numpy as np

class FaceLandmarker(BaseMediaPipeDetector):
    def __init__(self, num_faces=1, output_face_blendshapes=True, **kwargs):
        self.num_faces = num_faces
        self.output_face_blendshapes = output_face_blendshapes
        super().__init__(**kwargs)

    def _initialize_detector(self):
        try:
            base_options = python.BaseOptions(model_asset_path=ModelManager.get_model_path('face_landmarker.task'))
            options_args = {
                'base_options': base_options,
                'running_mode': self.running_mode,
                'num_faces': self.num_faces,
                'min_face_detection_confidence': self.min_detection_confidence,
                'output_face_blendshapes': self.output_face_blendshapes
            }
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                options_args['result_callback'] = self._save_result
            
            options = vision.FaceLandmarkerOptions(**options_args)
            self.detector = vision.FaceLandmarker.create_from_options(options)
        except Exception as e:
            raise BaseMediaPipeError(f"初始化人脸关键点检测器失败: {e}")

    def _process_result(self, detection_result, image_shape):
        return detection_result

    def draw(self, image: np.ndarray, results: FaceLandmarkerResult) -> np.ndarray:
        if not results or not results.face_landmarks:
            return image
        vis_image = image.copy()
        for face_landmarks in results.face_landmarks:
            # 转换为MediaPipe需要的格式
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                for landmark in face_landmarks
            ])
            vis_image = VisUtil.draw_face_landmarks(vis_image, face_landmarks_proto)
        return vis_image

    def get_landmarks(self, results: FaceLandmarkerResult) -> List[List[Tuple[int, int]]]:
        if not results or not results.face_landmarks:
            return []
        landmarks_list = []
        for face_landmarks in results.face_landmarks:
            landmarks = []
            for landmark in face_landmarks:
                landmarks.append((int(landmark.x * self._latest_frame.shape[1]), int(landmark.y * self._latest_frame.shape[0])))
            landmarks_list.append(landmarks)
        return landmarks_list 