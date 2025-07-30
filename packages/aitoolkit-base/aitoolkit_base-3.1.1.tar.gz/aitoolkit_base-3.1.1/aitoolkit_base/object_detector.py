import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.detections import Detection
import cv2
import numpy as np
from .utils import ModelManager, VisUtil
from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError
from typing import List, Tuple, Dict, Any
import time

class ObjectDetectionError(BaseMediaPipeError):
    """目标检测错误"""
    pass

class ObjectDetector(BaseMediaPipeDetector):
    def __init__(self, max_results=5, score_threshold=0.5, **kwargs):
        self.max_results = max_results
        self.score_threshold = score_threshold
        super().__init__(**kwargs)

    def _initialize_detector(self):
        try:
            base_options = python.BaseOptions(model_asset_path=ModelManager.get_model_path("object_detector.tflite"))
            options_args = {
                'base_options': base_options,
                'running_mode': self.running_mode,
                'max_results': self.max_results,
                'score_threshold': self.score_threshold
            }
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                options_args['result_callback'] = self._save_result
            
            options = vision.ObjectDetectorOptions(**options_args)
            self.detector = vision.ObjectDetector.create_from_options(options)
        except Exception as e:
            raise BaseMediaPipeError(f"初始化物体检测器失败: {e}")

    def _process_result(self, detection_result, image_shape):
        return detection_result.detections if detection_result else []

    def run(self, frame: np.ndarray = None) -> List[Detection]:
        """
        运行检测
        Args:
            frame: 输入帧
        Returns:
            检测结果列表
        """
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    self._process_input_source(frame)
                return self._process_result(self._latest_result, self._latest_frame.shape)
            else:
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
            raise ObjectDetectionError(f"运行检测失败: {str(e)}")

    def draw(self, image: np.ndarray, results: List[Detection]) -> np.ndarray:
        """
        在图像上绘制物体检测结果
        Args:
            image: 原始图像
            results: run() 方法返回的检测结果
        Returns:
            绘制了检测框的图像
        """
        if not results:
            return image
        
        vis_image = image.copy()
        
        for detection in results:
            bbox = detection.bounding_box
            category = detection.categories[0]
            label = f"{category.category_name} ({category.score:.2f})"
            vis_image = VisUtil.draw_bounding_box(vis_image, bbox, label)
            
        return vis_image

    def get_objects(self, results: List[Detection]) -> List[Dict[str, Any]]:
        """从结果中提取所有检测到的物体信息
        
        Args:
            results: run() 方法返回的检测结果
        
        Returns:
            物体信息列表
        """
        if not results:
            return []
            
        objects = []
        for detection in results:
            bbox = detection.bounding_box
            category = detection.categories[0]
            objects.append({
                'label': category.category_name,
                'score': category.score,
                'bbox': (bbox.origin_x, bbox.origin_y, bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
            })
        return objects 