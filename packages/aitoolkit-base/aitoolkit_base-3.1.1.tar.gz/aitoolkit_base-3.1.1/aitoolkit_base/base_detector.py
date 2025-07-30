import os
import sys
import warnings
import logging

# 确保日志屏蔽生效
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')
warnings.filterwarnings('ignore')

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from .utils import ModelManager
import time
import pathlib
from mediapipe.framework.formats import landmark_pb2
import threading
from typing import Optional, Callable

class BaseMediaPipeError(Exception):
    """MediaPipe基础错误类"""
    pass

class BaseDetector:
    """检测器基类"""
    
    @staticmethod 
    def setup_environment():
        """设置运行环境，确保稳定性"""
        # 强制CPU模式，避免GPU兼容性问题
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
        
        # 设置OpenCV线程数，避免资源竞争
        cv2.setNumThreads(1)
        
        # 屏蔽不必要的警告
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=FutureWarning)

class BaseMediaPipeDetector:
    def __init__(self, 
                 input_source: Optional[str] = None,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence=0.5,
                 enable_gpu=False,  # 默认关闭GPU，提高稳定性
                 result_callback: Optional[Callable] = None,
                 async_method_name: str = 'detect_async',
                 timeout_seconds: float = 10.0):  # 增加超时控制
        """
        MediaPipe检测器基类 - PyPI稳定版
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            min_detection_confidence: 最小检测置信度
            min_tracking_confidence: 最小跟踪置信度
            enable_gpu: 是否启用GPU加速
            result_callback: 可选的回调函数，用于实时流模式
            async_method_name: 用于实时流模式的异步方法名称。
            timeout_seconds: 初始化超时时间（秒）
        """
        try:
            # 环境设置
            BaseDetector.setup_environment()
            
            # 同步和结果存储
            self._result_lock = threading.RLock()
            self._latest_result = None
            self._latest_frame = None
            self._fps_counter = 0
            self._fps = 0
            self._start_time = time.time()
            self._fps_avg_frame_count = 10
            
            # 增加初始化超时控制
            self._init_timeout = timeout_seconds
            self._initialization_complete = threading.Event()
            
            # 基础参数设置
            self.min_detection_confidence = min_detection_confidence
            self.min_tracking_confidence = min_tracking_confidence
            self.result_callback = result_callback
            self.enable_gpu = enable_gpu  # 生产环境建议关闭
            self.async_method_name = async_method_name
            
            # 根据输入源确定模式
            self.running_mode = self._determine_mode(input_source)
            
            # 增加重试机制的检测器初始化
            self.detector = None
            self._initialize_detector_with_retry()
            
            # 如果是图片模式，立即处理输入图片
            if input_source is not None:
                self._process_input_source(input_source)
                
        except Exception as e:
            raise BaseMediaPipeError(f"初始化失败: {str(e)}")
            
    def _initialize_detector_with_retry(self, max_retries: int = 3):
        """带重试机制的检测器初始化"""
        for attempt in range(max_retries):
            try:
                self._initialize_detector()
                self._initialization_complete.set()
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    raise BaseMediaPipeError(f"检测器初始化失败 (已重试{max_retries}次): {e}")
                time.sleep(0.5 * (attempt + 1))  # 递增延迟
            
    def _determine_mode(self, input_source):
        """根据输入源确定运行模式"""
        if input_source is None:
            return vision.RunningMode.LIVE_STREAM
            
        if isinstance(input_source, (str, pathlib.Path)):
            path = pathlib.Path(input_source)
            if not path.exists():
                raise FileNotFoundError(f"图片文件不存在: {path}")
            if not path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}:
                raise ValueError(f"不支持的图片格式: {path.suffix}")
                
        elif isinstance(input_source, np.ndarray):
            if len(input_source.shape) != 3:
                raise ValueError("输入图像必须是3通道图像")
                
        else:
            raise ValueError(f"不支持的输入类型: {type(input_source)}")
            
        return vision.RunningMode.IMAGE
            
    def _wait_for_initialization(self) -> bool:
        """等待初始化完成"""
        return self._initialization_complete.wait(timeout=self._init_timeout)
            
    def _save_result(self, result, output_image, timestamp_ms: int):
        """内部回调函数，用于处理异步检测结果"""
        with self._result_lock:
            self._latest_result = result
        
        # 更新FPS计数
        if self._fps_counter % self._fps_avg_frame_count == 0:
            current_time = time.time()
            elapsed = current_time - self._start_time
            if elapsed > 0:
                self._fps = self._fps_avg_frame_count / elapsed
            self._start_time = current_time
        
        self._fps_counter += 1
        
        if self.result_callback:
            try:
                self.result_callback(result, output_image, timestamp_ms)
            except Exception as e:
                # 回调函数错误不应该影响主流程
                print(f"回调函数错误: {e}")
            
    def _initialize_detector(self):
        """初始化检测器 - 子类必须实现此方法"""
        raise NotImplementedError("子类必须实现_initialize_detector方法")
            
    def _process_input_source(self, input_source):
        """处理输入源"""
        if isinstance(input_source, str):
            image = cv2.imread(str(input_source))
            if image is None:
                raise ValueError(f"无法读取图像: {input_source}")
        elif isinstance(input_source, np.ndarray):
            image = input_source.copy()
        else:
            raise ValueError(f"不支持的输入源类型: {type(input_source)}")
        
        # 转换为RGB格式
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        # 同步检测
        with self._result_lock:
            self._latest_result = self.detector.detect(mp_image)
            self._latest_frame = image
        
    def _process_result(self, detection_result, image_shape):
        """处理检测结果 - 子类可以重写此方法"""
        return detection_result

    def run(self, frame: np.ndarray = None):
        """运行检测"""
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    self._process_input_source(frame)
                with self._result_lock:
                    # 在图片模式下，确保返回处理后的结果
                    if self._latest_result:
                        return self._process_result(self._latest_result, self._latest_frame.shape)
                    return None
            
            if frame is None:
                raise ValueError("实时流模式下必须传入frame参数")
            
            # 记录当前帧
            self._latest_frame = frame

            # 转换为RGB格式并进行异步检测
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # 根据实例类型调用正确的异步方法
            async_method = getattr(self.detector, self.async_method_name, None)
            if async_method and callable(async_method):
                async_method(mp_image, time.time_ns() // 1_000_000)
            else:
                # 提供一个默认的回退或错误
                raise AttributeError(f"Detector '{type(self.detector).__name__}' a/n '{self.async_method_name}' n'a/e.")
            
            with self._result_lock:
                if self._latest_result:
                    return self._process_result(self._latest_result, frame.shape)
                return None
                
        except Exception as e:
            raise BaseMediaPipeError(f"运行检测失败: {str(e)}")

    def draw(self, image, detection_data=None):
        """在图像上绘制检测结果 - 子类必须实现此方法"""
        raise NotImplementedError("子类必须实现draw方法")
        
    def get_fps(self):
        """获取当前FPS"""
        return self._fps
        
    def is_ready(self) -> bool:
        """检查检测器是否就绪"""
        return self._initialization_complete.is_set() and self.detector is not None
        
    def close(self):
        """释放资源"""
        try:
            if hasattr(self, 'detector') and self.detector:
                self.detector.close()
                self.detector = None
        except Exception as e:
            print(f"关闭检测器时出错: {e}")
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 