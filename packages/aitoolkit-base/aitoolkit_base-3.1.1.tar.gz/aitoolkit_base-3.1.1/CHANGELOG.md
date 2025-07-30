# 更新日志

## [3.0.0] - 2024-12-19

### 新增功能
- **图像分割模块 (ImageSegmenter)**
  - 人像分割功能，支持实时背景替换
  - 基于MediaPipe的高精度分割
  - 支持自定义背景颜色
  - 提供二值化掩码生成

- **图像分类模块 (ImageClassifier)**
  - 通用图像分类功能
  - 自定义分类器支持（CustomImageClassifier）
  - 批量图像分类（BatchImageClassifier）
  - 支持自定义标签文件

- **模型训练模块 (ModelTrainer)**
  - 基于MediaPipe Model Maker的分类模型训练
  - 目标检测模型训练支持
  - 数据集预处理工具（DatasetPreprocessor）
  - 完整的训练流水线（TrainingPipeline）

- **交互式分割功能 (InteractiveSegmenter)**
  - 基于点击的交互式分割（开发中）
  - 支持正负样本点标记

### 重大变更
- **移除Camera模块**
  - 简化项目架构，专注于AI算法功能
  - 用户可直接使用cv2.VideoCapture进行视频处理
  - 移除所有Camera相关的代码和文档

### 优化改进
- 统一了所有模块的API接口风格
- 改进了错误处理和资源管理
- 优化了模型加载和内存使用
- 增强了文档和示例代码

### 依赖更新
- 新增mediapipe-model-maker支持（可选）
- 新增tensorflow>=2.13.0（训练功能需要）
- 新增Pillow、matplotlib等图像处理库
- 新增pandas、scikit-learn用于数据处理

### 版本兼容性
- Python >= 3.8
- MediaPipe >= 0.10.0
- OpenCV >= 4.8.0

### 已知问题
- 交互式分割功能仍在开发中
- 某些模型需要额外下载

---

## [2.0.0] - 2024-XX-XX

### 新增功能
- 人脸检测和关键点检测
- 手部关键点检测
- 人体姿态检测
- 手势识别
- 物体检测
- Camera工具模块

### 性能优化
- 同步检测技术
- 自动跳帧控制
- 线程安全设计

---

## [1.0.0] - 2024-XX-XX

### 初始版本
- 基础人脸检测功能
- 基础手部检测功能
- 基本的API框架
