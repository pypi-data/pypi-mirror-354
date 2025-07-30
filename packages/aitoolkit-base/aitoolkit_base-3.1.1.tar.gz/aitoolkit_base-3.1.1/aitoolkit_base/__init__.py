"""
AIToolkit Base 3.1.1 - 懒加载优化版本
只在需要时才加载对应的模块，大幅提升启动速度
"""

__version__ = '3.1.1'

# 模块映射表 - 按需加载
_MODULE_MAP = {
    # 核心检测器
    'FaceDetector': 'aitoolkit_base.face_detector',
    'FaceLandmarker': 'aitoolkit_base.face_landmarker',
    'HandLandmarker': 'aitoolkit_base.hand_landmarker', 
    'PoseLandmarker': 'aitoolkit_base.pose_landmarker',
    'GestureRecognizer': 'aitoolkit_base.gesture_recognizer',
    'ObjectDetector': 'aitoolkit_base.object_detector',
    
    # 图像处理
    'ImageSegmenter': 'aitoolkit_base.image_segmenter',
    'InteractiveSegmenter': 'aitoolkit_base.interactive_segmenter',
    'ImageClassifier': 'aitoolkit_base.image_classifier',
    'CustomImageClassifier': 'aitoolkit_base.image_classifier',
    'BatchImageClassifier': 'aitoolkit_base.image_classifier',
    
    # 高级功能
    'LicensePlateDetector': 'aitoolkit_base.license_plate_detector',
    'OCRDetector': 'aitoolkit_base.ocr_detector',
    'DepthEstimator': 'aitoolkit_base.depth_estimator',
    'StyleTransfer': 'aitoolkit_base.style_transfer',
    
    # 工具类
    'ModelManager': 'aitoolkit_base.utils',
    'ImageUtils': 'aitoolkit_base.utils',
}

# 训练功能映射
_TRAINING_MAP = {
    'train_image_classifier': 'aitoolkit_base.model_trainer',
    'train_object_detector': 'aitoolkit_base.model_trainer', 
    'prepare_classification_data': 'aitoolkit_base.model_trainer',
    'ImageClassifierTrainer': 'aitoolkit_base.model_trainer',
    'ObjectDetectorTrainer': 'aitoolkit_base.model_trainer',
    'DatasetPreprocessor': 'aitoolkit_base.model_trainer',
    'TrainingPipeline': 'aitoolkit_base.model_trainer',
}

def __getattr__(name):
    """懒加载机制 - 只在需要时导入对应模块"""
    if name in _MODULE_MAP:
        try:
            module_path = _MODULE_MAP[name]
            module = __import__(module_path, fromlist=[name])
            cls = getattr(module, name)
            
            # 缓存到全局命名空间以避免重复导入
            globals()[name] = cls
            return cls
            
        except ImportError as e:
            raise ImportError(f"无法导入 {name}: {e}")
            
    elif name in _TRAINING_MAP:
        try:
            module_path = _TRAINING_MAP[name]
            module = __import__(module_path, fromlist=[name])
            obj = getattr(module, name)
            
            # 缓存到全局命名空间
            globals()[name] = obj
            return obj
            
        except ImportError as e:
            raise ImportError(f"训练功能不可用，请安装训练依赖: pip install aitoolkit-base[training]")
    
    raise AttributeError(f"模块 'aitoolkit_base' 没有属性 '{name}'")

# 提供模块检查函数
def is_available(module_name: str) -> bool:
    """检查模块是否可用"""
    if module_name in _MODULE_MAP:
        try:
            __getattr__(module_name)
            return True
        except ImportError:
            return False
    return False

def list_available_modules():
    """列出所有可用的模块"""
    available = []
    for name in _MODULE_MAP:
        if is_available(name):
            available.append(name)
    return available

# 快速创建函数（推荐用法）
def create_face_detector(**kwargs):
    """快速创建人脸检测器"""
    FaceDetector = __getattr__('FaceDetector')
    return FaceDetector(**kwargs)

def create_hand_detector(**kwargs):
    """快速创建手部检测器"""
    HandLandmarker = __getattr__('HandLandmarker')
    return HandLandmarker(**kwargs)

def create_pose_detector(**kwargs):
    """快速创建姿态检测器"""
    PoseLandmarker = __getattr__('PoseLandmarker')
    return PoseLandmarker(**kwargs)

# 所有可导入的名称（用于IDE提示）
__all__ = list(_MODULE_MAP.keys()) + list(_TRAINING_MAP.keys()) + [
    'is_available',
    'list_available_modules', 
    'create_face_detector',
    'create_hand_detector',
    'create_pose_detector',
    'show_quick_usage',
]

# 快速使用指南
QUICK_USAGE = """
🚀 AIToolkit Base 3.1 - 懒加载版快速指南

# 推荐方式1：使用create函数（最快）
from aitoolkit_base import create_face_detector
detector = create_face_detector()

# 推荐方式2：按需导入（快速）
from aitoolkit_base import FaceDetector  # 只在这时才加载MediaPipe
detector = FaceDetector()

# 传统方式（兼容旧代码）
import aitoolkit_base
detector = aitoolkit_base.FaceDetector()

# 检查可用性
from aitoolkit_base import is_available, list_available_modules
print("人脸检测可用:", is_available('FaceDetector'))
print("所有可用模块:", list_available_modules())
"""

def show_quick_usage():
    """显示快速使用指南"""
    print(QUICK_USAGE) 