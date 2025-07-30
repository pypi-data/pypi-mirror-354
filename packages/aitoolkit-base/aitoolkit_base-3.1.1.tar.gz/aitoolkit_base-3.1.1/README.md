# AIToolkit Base - 基于MediaPipe的AI视觉工具包

一个易用的AI视觉处理工具包，集成了人脸检测、深度估计、风格转换、OCR等功能，并支持一键训练自定义模型。

## 版本 3.1 新特性 ✨

- 🎯 **2行代码训练模型**: 图像分类和目标检测模型训练
- 🧠 **增强深度估计**: 基于MiDaS深度学习模型，精度大幅提升
- 🇨🇳 **中文OCR优化**: 集成cnocr，专为中文文本优化
- 🎨 **高质量风格转换**: 重写算法，艺术效果更佳

## 快速安装 🚀

### 方法1: 智能安装向导（推荐）
```bash
python install_guide.py
```

### 方法2: 手动安装
```bash
pip install -r requirements.txt
```

### 方法3: 最小安装
```bash
pip install mediapipe opencv-python numpy Pillow
```

## 数据准备 📁

### 训练分类模型数据结构
```
dataset/classification/
├── train/
│   ├── 猫/
│   │   ├── cat1.jpg
│   │   └── cat2.jpg
│   ├── 狗/
│   └── 鸟/
└── val/
    ├── 猫/
    ├── 狗/
    └── 鸟/
```

### 训练检测模型数据结构
```
dataset/detection/
├── images/
│   ├── img1.jpg
│   └── img2.jpg
└── labels/
    ├── img1.txt  # YOLO格式: class_id center_x center_y width height
    └── img2.txt
```

### 快速创建数据结构
```bash
python data_preparation_guide.py
```

## 一键训练 ⚡

```python
from aitoolkit_base import train_image_classifier, train_object_detector

# 训练图像分类模型（2行代码）
train_image_classifier("dataset/classification", "my_classifier.pth")

# 训练目标检测模型（2行代码）
train_object_detector("dataset/detection", "my_detector.pth")
```

## 核心功能示例

```python
import cv2
from aitoolkit_base import (
    FaceDetector, DepthEstimator, StyleTransfer, 
    OCRDetector, PoseLandmarker, ImageSegmenter
)

# 读取图片
image = cv2.imread("example.jpg")

# 人脸检测
face_detector = FaceDetector()
faces = face_detector.run(image)
print(f"检测到 {len(faces)} 个人脸")

# 深度估计（基于MiDaS深度学习）
depth_estimator = DepthEstimator(method="midas")
depth_result = depth_estimator.run(image)
depth_map = depth_result['depth_map']

# 艺术风格转换
style_transfer = StyleTransfer()
oil_painting = style_transfer.apply_style(image, "oil_painting")
watercolor = style_transfer.apply_style(image, "watercolor")

# 中文OCR
ocr_detector = OCRDetector(use_cnocr=True)
text_results = ocr_detector.run(image)
for result in text_results:
    print(f"文本: {result['text']}, 位置: {result['bbox']}")

# 姿态检测
pose_detector = PoseLandmarker()
pose_landmarks = pose_detector.run(image)

# 图像分割
segmenter = ImageSegmenter()
segments = segmenter.run(image)
```

## 功能特性

### 🔍 计算机视觉基础
- **人脸检测**: MediaPipe FaceDetection
- **姿态估计**: MediaPipe Pose 
- **手部检测**: MediaPipe Hands
- **图像分割**: MediaPipe Selfie Segmentation

### 🎨 艺术效果
- **风格转换**: 油画、水彩、素描、卡通等多种艺术风格
- **滤镜效果**: 复古、黑白、暖色调等

### 📊 深度学习增强
- **智能深度估计**: MiDaS → DPT → 传统方法的智能回退
- **中文OCR**: cnocr → Tesseract → OpenCV的多引擎支持

### 🤖 模型训练
- **图像分类**: 一键训练ResNet分类模型
- **目标检测**: 一键训练YOLO检测模型
- **数据准备**: 自动化数据验证和预处理

## 测试安装

```bash
python test_all_functions.py
```

## 进阶用法

查看 `examples_improved.py` 了解所有功能的详细使用方法。

## 故障排除

### 常见问题

1. **protobuf版本冲突**
   ```bash
   pip install protobuf>=3.20.0,<5.0.0 --force-reinstall
   ```

2. **Windows PyTorch安装**
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

3. **cnocr安装失败**
   ```bash
   pip install cnocr --no-deps
   pip install onnxruntime opencv-python pillow numpy
   ```

### 获取帮助

运行安装向导获取个性化帮助：
```bash
python install_guide.py
```

## 版本历史

- **v3.1**: 项目整理、简化安装、优化稳定性
- **v3.0**: MediaPipe集成、风格转换、基础训练功能
- **v2.0**: OpenCV基础功能

## 系统要求

- Python 3.8+
- Windows/macOS/Linux
- 4GB+ RAM (训练需要8GB+)

---

享受AI视觉处理的便利！🎉 