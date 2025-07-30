import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.detections import Detection
import cv2
import numpy as np
from .utils import ModelManager, VisUtil
import time
import pathlib
from typing import List, Tuple
from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError
import threading


class FaceDetectorError(BaseMediaPipeError):
    """人脸检测错误"""
    pass

class FaceDetector(BaseMediaPipeDetector):
    def __init__(self, min_suppression_threshold=0.5, **kwargs):
        self.min_suppression_threshold = min_suppression_threshold
        super().__init__(**kwargs)

    def _initialize_detector(self):
        try:
            base_options = python.BaseOptions(model_asset_path=ModelManager.get_model_path("face_detector.tflite"))
            options_args = {
                'base_options': base_options,
                'running_mode': self.running_mode,
                'min_detection_confidence': self.min_detection_confidence,
                'min_suppression_threshold': self.min_suppression_threshold
            }
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                options_args['result_callback'] = self._save_result
            
            options = vision.FaceDetectorOptions(**options_args)
            self.detector = vision.FaceDetector.create_from_options(options)
        except Exception as e:
            raise BaseMediaPipeError(f"初始化人脸检测器失败: {e}")

    def _process_result(self, detection_result, image_shape):
        return detection_result.detections if detection_result else []

    def draw(self, image: np.ndarray, results: List[Detection]) -> np.ndarray:
        if not results:
            return image
        vis_image = image.copy()
        for detection in results:
            vis_image = VisUtil.draw_bounding_box(vis_image, detection.bounding_box)
        return vis_image

    def get_bboxes(self, results: List[Detection]) -> List[Tuple[int, int, int, int]]:
        if not results:
            return []
        return [(d.bounding_box.origin_x, d.bounding_box.origin_y, d.bounding_box.origin_x + d.bounding_box.width, d.bounding_box.origin_y + d.bounding_box.height) for d in results]

    def run(self, frame: np.ndarray = None) -> List[Detection]:
        """
        运行检测
        Args:
            frame: 输入帧
        Returns:
            检测结果列表，每个元素为 mediapipe.tasks.python.components.containers.detection.Detection 对象
        """
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    # 如果是图片模式，并且传入了新的帧，则更新内部状态
                    self._process_input_source(frame)
                return self._process_result(self._latest_result, self._latest_frame.shape)
            
            else:  # 实时流模式
                if frame is None:
                    raise ValueError("实时流模式下必须传入frame参数")
                
                # 实时流模式下，异步检测结果由回调函数处理
                # 这里只负责触发异步检测
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                self.detector.detect_async(mp_image, time.time_ns() // 1_000_000)
                
                # 返回最新的结果
                with self._result_lock:
                    return self._process_result(self._latest_result, frame.shape)
                
        except Exception as e:
            raise FaceDetectorError(f"运行检测失败: {str(e)}")

    def get_fps(self):
        """获取当前FPS - 已弃用，请使用camera模块的get_fps方法"""
        raise NotImplementedError("请使用camera模块的get_fps方法获取帧率")
        
    def close(self):
        """释放资源"""
        if hasattr(self, 'detector'):
            self.detector.close()
    

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

