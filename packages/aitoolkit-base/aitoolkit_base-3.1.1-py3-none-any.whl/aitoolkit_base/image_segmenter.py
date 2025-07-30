"""
图像分割模块
基于MediaPipe实现图像分割功能
"""

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.components.containers.category import Category
from mediapipe.tasks.python.vision.image_segmenter import ImageSegmenterResult
from typing import List, Optional, Tuple, Union
from .base_detector import BaseDetector, BaseMediaPipeDetector, BaseMediaPipeError
from .utils import ModelManager
from mediapipe.tasks.python.vision import ImageSegmenterOptions
from .utils import VisUtil


class ImageSegmentationError(Exception):
    """自定义图像分割错误"""
    pass

class ImageSegmenterError(Exception):
    """图像分割错误"""
    pass

class ImageSegmenter(BaseMediaPipeDetector):
    """
    图像分割器，封装了MediaPipe的ImageSegmenter。
    """
    def __init__(self, model: str = 'selfie_segmenter', **kwargs):
        """
        初始化图像分割器。
        
        Args:
            model (str): 要使用的模型名称。
                         支持的模型: 'selfie_segmenter', 'deeplab_v3'。
            **kwargs: 传入BaseMediaPipeDetector的参数。
        """
        self.model_name = model
        # 分割模型使用 .tflite 文件
        self.model_path = ModelManager.get_model_path(self.model_name + ".tflite")
        
        self.output_category_mask = True
        
        # 为BaseDetector提供异步方法名
        super().__init__(async_method_name='segment_async', **kwargs)

    def _initialize_detector(self):
        """
        根据运行模式初始化MediaPipe图像分割器。
        """
        try:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            
            options_args = {
                'base_options': base_options,
                'running_mode': self.running_mode,
                'output_category_mask': self.output_category_mask,
            }
            
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                options_args['result_callback'] = self._save_result
            
            options = ImageSegmenterOptions(**options_args)
            self.detector = vision.ImageSegmenter.create_from_options(options)
        except Exception as e:
            raise ImageSegmentationError(f"初始化图像分割器失败: {e}")

    def run(self, image: np.ndarray) -> ImageSegmenterResult:
        """运行图像分割
        Args:
            image: BGR格式的图像
        Returns:
            原始的分割结果
        """
        # 在图像模式下，直接调用同步方法
        if self.running_mode == vision.RunningMode.IMAGE:
             # 将图像从BGR转换为RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            self._latest_result = self.detector.segment(mp_image)
            self._latest_frame = image
            return self._latest_result
        
        # 对于实时视频流，依赖于异步回调
        elif self.running_mode == vision.RunningMode.LIVE_STREAM:
            super().run(image) # 调用父类的run来处理异步逻辑
            return self._latest_result
            
        return None
    
    def _process_result(self, detection_result, image_shape):
        """处理分割结果"""
        # 这个类直接返回原始结果，所以这里不需要做什么
        return detection_result

    def draw(self, image: np.ndarray, results: ImageSegmenterResult) -> np.ndarray:
        """
        将分割蒙版绘制到图像上。
        
        Args:
            image: 原始图像 (BGR)。
            results: run() 方法返回的分割结果。
            
        Returns:
            带有分割蒙版的图像。
        """
        if not results or results.category_mask is None:
            return image
            
        # 从结果中获取分割蒙版
        segmentation_mask = results.category_mask.numpy_view()
        
        # 使用VisUtil来叠加蒙版
        vis_image = VisUtil.draw_segmentation_mask(image, segmentation_mask)
        
        return vis_image

    def get_mask(self, result: ImageSegmenterResult) -> Optional[np.ndarray]:
        """
        从结果中获取二值化类别掩码
        
        Args:
            result: run() 方法返回的分割结果
            
        Returns:
            二值化掩码 (0或255)
        """
        if not result or not hasattr(result, 'category_mask'):
            return None
        
        # 假设我们关心所有非背景的类别
        mask = result.category_mask.numpy_view()
        binary_mask = (mask > 0).astype(np.uint8) * 255
        return binary_mask


class InteractiveSegmenter(BaseDetector):
    """交互式图像分割器
    
    基于点击点进行交互式分割
    """
    
    def __init__(self, **kwargs):
        """初始化交互式分割器"""
        super().__init__(**kwargs)
        self.mp_interactive_segmenter = mp.solutions.interactive_segmenter
        self.click_points = []  # 存储点击点
        self._initialize_model()
    
    def _initialize_model(self):
        """初始化交互式分割模型"""
        try:
            # 注意：交互式分割需要特定的模型文件
            # 这里提供基本框架，实际使用需要相应的模型文件
            print("交互式分割器初始化 - 需要额外的模型文件")
        except Exception as e:
            print(f"交互式分割器初始化失败: {e}")
    
    def add_click_point(self, x: int, y: int, is_positive: bool = True):
        """添加点击点
        
        Args:
            x: x坐标
            y: y坐标
            is_positive: 是否为正样本点
        """
        self.click_points.append({
            'x': x,
            'y': y,
            'positive': is_positive
        })
    
    def clear_points(self):
        """清除所有点击点"""
        self.click_points = []
    
    def _process_image(self, image: np.ndarray) -> List:
        """处理图像进行交互式分割
        
        Args:
            image: 输入图像
            
        Returns:
            分割结果
        """
        # 这里需要实现具体的交互式分割逻辑
        # 当前返回空列表作为占位符
        return []
    
    def draw(self, image: np.ndarray, segments: List) -> np.ndarray:
        """绘制交互式分割结果
        
        Args:
            image: 原始图像
            segments: 分割结果
            
        Returns:
            绘制结果的图像
        """
        result_image = image.copy()
        
        # 绘制点击点
        for point in self.click_points:
            color = (0, 255, 0) if point['positive'] else (0, 0, 255)
            cv2.circle(result_image, (point['x'], point['y']), 5, color, -1)
        
        return result_image 