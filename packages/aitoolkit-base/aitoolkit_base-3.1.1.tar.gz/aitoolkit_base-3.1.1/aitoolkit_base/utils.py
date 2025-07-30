# 优先屏蔽所有可能的日志输出
import os
import sys
import warnings
import logging

# 最高优先级：屏蔽TensorFlow日志
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # 强制使用CPU，提高稳定性

# 屏蔽所有警告
warnings.simplefilter('ignore')
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# 设置所有可能的第三方库日志级别
for logger_name in ['tensorflow', 'mediapipe', 'absl', 'h5py', 'PIL']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

# 静默模式启动
def silent_import():
    """静默导入模式，屏蔽启动时的所有输出"""
    # 临时重定向stderr
    original_stderr = sys.stderr
    original_stdout = sys.stdout
    
    try:
        # 创建空的输出
        from io import StringIO
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        
        # 导入MediaPipe和TensorFlow相关模块
        import mediapipe as mp
        import cv2
        
        # 恢复输出
        sys.stderr = original_stderr
        sys.stdout = original_stdout
        
        return True
    except Exception as e:
        # 恢复输出
        sys.stderr = original_stderr  
        sys.stdout = original_stdout
        print(f"静默导入失败: {e}")
        return False

# 在模块加载时执行静默导入
# silent_import()

import cv2
import numpy as np
import time
import threading
import pathlib
from typing import Optional, Union, List, Tuple
import requests
from urllib.parse import urlparse

# MediaPipe相关导入
try:
    import mediapipe as mp
    from mediapipe.tasks.python.components.containers.bounding_box import BoundingBox
    from mediapipe.python.solutions import drawing_utils as mp_drawing
    from mediapipe.python.solutions import drawing_styles as mp_drawing_styles
    from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
    from mediapipe.framework.formats import landmark_pb2
    MEDIAPIPE_AVAILABLE = True
except ImportError as e:
    print(f"MediaPipe导入失败: {e}")
    # 创建占位符类
    class BoundingBox:
        def __init__(self):
            self.origin_x = 0
            self.origin_y = 0
            self.width = 0
            self.height = 0
    
    class NormalizedLandmark:
        def __init__(self):
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            
    MEDIAPIPE_AVAILABLE = False

# 模型文件映射表
MODEL_MAPPING = {
    "face_detector.tflite": "face_detector.tflite",
    "face_landmarker.task": "face_landmarker.task", 
    "hand_landmarker.task": "hand_landmarker.task",
    "pose_landmarker.task": "pose_landmarker.task",
    "gesture_recognizer.task": "gesture_recognizer.task",
    "selfie_segmenter.tflite": "selfie_segmenter.tflite",
    "selfie_segmenter_landscape.tflite": "selfie_segmenter_landscape.tflite",
    "deeplab_v3.tflite": "deeplab_v3.tflite",
}

class ModelManager:
    """模型管理器 - 处理模型文件的下载和路径管理"""
    
    BASE_URL = "https://storage.googleapis.com/mediapipe-models"
    MODELS_DIR = pathlib.Path(__file__).parent / "models"
    
    @classmethod
    def ensure_models_dir(cls):
        """确保模型目录存在"""
        cls.MODELS_DIR.mkdir(exist_ok=True)
        return cls.MODELS_DIR
    
    @classmethod 
    def get_model_path(cls, model_name: str) -> str:
        """获取模型文件路径，如果不存在则下载"""
        models_dir = cls.ensure_models_dir()
        
        # 规范化模型名称
        if model_name in MODEL_MAPPING:
            actual_name = MODEL_MAPPING[model_name]
        else:
            actual_name = model_name
            
        model_path = models_dir / actual_name
        
        if model_path.exists():
            return str(model_path)
        
        # 如果文件不存在，尝试下载
        success = cls.download_model(model_name, str(model_path))
        if success:
            return str(model_path)
        else:
            raise FileNotFoundError(f"模型文件不存在且下载失败: {model_name}")
    
    @classmethod
    def download_model(cls, model_name: str, save_path: str) -> bool:
        """下载模型文件"""
        try:
            # MediaPipe模型的标准下载URL构建
            model_urls = {
                "face_detector.tflite": f"{cls.BASE_URL}/face_detection/face_detection_short_range/float16/1/face_detection_short_range.tflite",
                "face_landmarker.task": f"{cls.BASE_URL}/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
                "hand_landmarker.task": f"{cls.BASE_URL}/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
                "pose_landmarker.task": f"{cls.BASE_URL}/pose_landmarker/pose_landmarker/float16/1/pose_landmarker.task",
                "gesture_recognizer.task": f"{cls.BASE_URL}/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
            }
            
            actual_name = MODEL_MAPPING.get(model_name, model_name)
            if actual_name not in model_urls:
                print(f"未知的模型: {model_name}")
                return False
            
            url = model_urls[actual_name]
            print(f"正在下载模型: {model_name}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"模型下载完成: {model_name}")
            return True
            
        except Exception as e:
            print(f"模型下载失败 {model_name}: {e}")
            return False

class ImageUtils:
    """图像处理工具类"""
    
    @staticmethod
    def resize_image(image, max_size=1024):
        """
        调整图像大小，保持宽高比
        参数:
            image: 输入图像
            max_size: 最大边长
        返回:
            调整后的图像
        """
        height, width = image.shape[:2]
        
        # 如果图像尺寸已经小于最大尺寸，直接返回
        if max(height, width) <= max_size:
            return image
        
        # 计算缩放比例
        scale = max_size / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 调整图像大小
        resized = cv2.resize(image, (new_width, new_height))
        return resized
    
    @staticmethod
    def draw_fps(image, fps):
        """
        在图像上绘制FPS
        参数:
            image: 输入图像
            fps: FPS值
        返回:
            添加FPS显示的图像
        """
        # 在左上角绘制FPS
        cv2.putText(image, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return image

class VisUtil:
    """可视化工具类"""
    
    @staticmethod
    def draw_bounding_box(image: np.ndarray, box: BoundingBox, label: str = "", color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
        """
        在图像上绘制边界框
        参数:
            image: 输入图像
            box: 边界框对象
            label: 标签文本
            color: 边界框颜色
            thickness: 线条粗细
        返回:
            绘制后的图像
        """
        if not MEDIAPIPE_AVAILABLE:
            return image
            
        # 计算边界框坐标
        start_point = (int(box.origin_x), int(box.origin_y))
        end_point = (int(box.origin_x + box.width), int(box.origin_y + box.height))
        
        # 绘制矩形
        cv2.rectangle(image, start_point, end_point, color, thickness)
        
        # 如果有标签，绘制标签
        if label:
            cv2.putText(image, label, (start_point[0], start_point[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
        
        return image
    
    @staticmethod 
    def draw_landmarks(image: np.ndarray, landmarks: List[NormalizedLandmark], connections=None, 
                      landmark_color: Tuple[int, int, int] = (0, 255, 0), 
                      connection_color: Tuple[int, int, int] = (255, 255, 255),
                      thickness: int = 2) -> np.ndarray:
        """
        在图像上绘制关键点
        参数:
            image: 输入图像
            landmarks: 关键点列表
            connections: 连接关系
            landmark_color: 关键点颜色
            connection_color: 连接线颜色
            thickness: 线条粗细
        返回:
            绘制后的图像
        """
        if not MEDIAPIPE_AVAILABLE or not landmarks:
            return image
            
        h, w = image.shape[:2]
        
        # 绘制连接线
        if connections:
            for connection in connections:
                start_idx, end_idx = connection
                if start_idx < len(landmarks) and end_idx < len(landmarks):
                    start_point = (int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h))
                    end_point = (int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h))
                    cv2.line(image, start_point, end_point, connection_color, thickness)
        
        # 绘制关键点
        for landmark in landmarks:
            point = (int(landmark.x * w), int(landmark.y * h))
            cv2.circle(image, point, thickness + 1, landmark_color, -1)
        
        return image

# 运行测试和安装指南的命令行函数
def run_tests():
    """运行测试套件"""
    print("🧪 运行AIToolkit Base测试套件...")
    # 这里可以添加具体的测试逻辑
    
def run_install_guide():
    """运行安装指南"""
    print("📦 AIToolkit Base 安装指南")
    print("使用以下命令安装:")
    print("pip install aitoolkit-base")
    print("或安装所有功能:")
    print("pip install aitoolkit-base[all]") 