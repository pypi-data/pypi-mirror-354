"""
模型训练模块
基于MediaPipe Model Maker实现分类和检测模型训练
一键式训练，用户10行代码完成模型训练
"""

import os
import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
import pandas as pd
from pathlib import Path

try:
    import mediapipe_model_maker as mm
    from mediapipe_model_maker import image_classifier
    from mediapipe_model_maker import object_detector
    MODEL_MAKER_AVAILABLE = True
except ImportError:
    MODEL_MAKER_AVAILABLE = False
    # 移除这里的警告，只在用户尝试使用训练功能时才显示
    # print("MediaPipe Model Maker未安装，训练功能不可用")


# 一键式训练函数
def train_image_classifier(data_dir: str, 
                          output_dir: str = "./trained_models",
                          epochs: int = 10,
                          model_name: str = "my_classifier") -> bool:
    """一键训练图像分类器
    
    用户只需调用这一个函数即可完成训练
    
    Args:
        data_dir: 训练数据目录(包含按类别分类的子文件夹)
        output_dir: 模型输出目录
        epochs: 训练轮数
        model_name: 模型名称
        
    Returns:
        训练是否成功
        
    示例使用:
        # 只需2行代码训练分类器!
        from aitoolkit_base import train_image_classifier
        train_image_classifier("./my_data", epochs=5)
    """
    if not MODEL_MAKER_AVAILABLE:
        print("❌ 需要安装 mediapipe-model-maker 才能使用训练功能")
        return False
    
    try:
        print(f"🚀 开始训练图像分类器...")
        
        # 1. 加载数据
        print("📂 加载训练数据...")
        data = image_classifier.Dataset.from_folder(data_dir)
        train_data, validation_data = data.split(0.2)
        print(f"✅ 训练集: {len(train_data)} 张, 验证集: {len(validation_data)} 张")
        
        # 2. 创建并训练模型
        print("🤖 开始训练模型...")
        model = image_classifier.create(
            train_data,
            model_spec=image_classifier.SupportedModels.MOBILENET_V2,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=32,
            learning_rate=0.001
        )
        
        # 3. 评估模型
        print("📊 评估模型性能...")
        loss, accuracy = model.evaluate(validation_data)
        print(f"✅ 训练完成! 准确率: {accuracy:.3f}, 损失: {loss:.3f}")
        
        # 4. 导出模型
        print("💾 导出模型...")
        os.makedirs(output_dir, exist_ok=True)
        model_path = os.path.join(output_dir, f"{model_name}.tflite")
        model.export_model(model_path)
        
        # 5. 保存标签
        labels_path = os.path.join(output_dir, f"{model_name}_labels.txt")
        with open(labels_path, 'w', encoding='utf-8') as f:
            for label in data.label_names:
                f.write(f"{label}\n")
        
        print(f"🎉 模型训练完成!")
        print(f"📁 模型文件: {model_path}")
        print(f"📁 标签文件: {labels_path}")
        return True
        
    except Exception as e:
        print(f"❌ 训练失败: {e}")
        return False


def train_object_detector(data_dir: str,
                         annotations_dir: str,
                         output_dir: str = "./trained_models", 
                         epochs: int = 20,
                         model_name: str = "my_detector") -> bool:
    """一键训练目标检测器
    
    Args:
        data_dir: 图像目录
        annotations_dir: 标注文件目录(PASCAL VOC格式)
        output_dir: 模型输出目录  
        epochs: 训练轮数
        model_name: 模型名称
        
    Returns:
        训练是否成功
        
    示例使用:
        # 只需2行代码训练检测器!
        from aitoolkit_base import train_object_detector
        train_object_detector("./images", "./annotations", epochs=10)
    """
    if not MODEL_MAKER_AVAILABLE:
        print("❌ 需要安装 mediapipe-model-maker")
        return False
    
    try:
        print(f"🚀 开始训练目标检测器...")
        
        # 1. 加载数据
        print("📂 加载训练数据...")
        data = object_detector.Dataset.from_pascal_voc_folder(
            data_dir, annotations_dir
        )
        train_data, validation_data = data.split(0.2)
        print(f"✅ 训练集: {len(train_data)} 张, 验证集: {len(validation_data)} 张")
        
        # 2. 创建并训练模型
        print("🤖 开始训练模型...")
        model = object_detector.create(
            train_data,
            model_spec=object_detector.SupportedModels.MOBILENET_V2,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=8,
            learning_rate=0.3
        )
        
        # 3. 评估模型
        print("📊 评估模型性能...")
        loss = model.evaluate(validation_data)
        print(f"✅ 训练完成! 损失: {loss:.3f}")
        
        # 4. 导出模型
        print("💾 导出模型...")
        os.makedirs(output_dir, exist_ok=True)
        model_path = os.path.join(output_dir, f"{model_name}.tflite")
        model.export_model(model_path)
        
        print(f"🎉 检测器训练完成!")
        print(f"📁 模型文件: {model_path}")
        return True
        
    except Exception as e:
        print(f"❌ 训练失败: {e}")
        return False


# 快速数据准备工具
def prepare_classification_data(source_dir: str, target_dir: str, image_size: int = 224) -> bool:
    """快速准备分类训练数据
    
    Args:
        source_dir: 原始数据目录
        target_dir: 处理后数据目录
        image_size: 图像大小
        
    Returns:
        是否成功
    """
    try:
        print("📂 准备分类训练数据...")
        
        os.makedirs(target_dir, exist_ok=True)
        
        # 遍历源目录中的类别文件夹
        for class_name in os.listdir(source_dir):
            class_path = os.path.join(source_dir, class_name)
            if not os.path.isdir(class_path):
                continue
            
            # 创建目标类别文件夹
            target_class_path = os.path.join(target_dir, class_name)
            os.makedirs(target_class_path, exist_ok=True)
            
            # 处理图像
            image_count = 0
            for filename in os.listdir(class_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    source_img_path = os.path.join(class_path, filename)
                    target_img_path = os.path.join(target_class_path, filename)
                    
                    # 读取并调整图像大小
                    img = cv2.imread(source_img_path)
                    if img is not None:
                        img_resized = cv2.resize(img, (image_size, image_size))
                        cv2.imwrite(target_img_path, img_resized)
                        image_count += 1
            
            print(f"✅ 类别 '{class_name}': {image_count} 张图像")
        
        print(f"🎉 数据准备完成! 输出目录: {target_dir}")
        return True
        
    except Exception as e:
        print(f"❌ 数据准备失败: {e}")
        return False


class ImageClassifierTrainer:
    """图像分类器训练器 (高级用法)"""
    
    def __init__(self, 
                 data_dir: str,
                 validation_split: float = 0.2,
                 model_spec: str = 'mobilenet_v2'):
        """初始化训练器"""
        if not MODEL_MAKER_AVAILABLE:
            raise ImportError("需要安装 mediapipe-model-maker")
        
        self.data_dir = data_dir
        self.validation_split = validation_split
        self.model_spec = model_spec
        self.model = None
        self.train_data = None
        self.validation_data = None
        
    def prepare_data(self):
        """准备训练数据"""
        try:
            data = image_classifier.Dataset.from_folder(self.data_dir)
            self.train_data, self.validation_data = data.split(self.validation_split)
            print(f"训练数据: {len(self.train_data)} 张")
            print(f"验证数据: {len(self.validation_data)} 张")
            return True
        except Exception as e:
            print(f"数据准备失败: {e}")
            return False
    
    def create_model_spec(self):
        """创建模型规格"""
        try:
            if self.model_spec == 'mobilenet_v2':
                return image_classifier.SupportedModels.MOBILENET_V2
            elif self.model_spec == 'efficientnet_lite0':
                return image_classifier.SupportedModels.EFFICIENTNET_LITE0
            elif self.model_spec == 'efficientnet_lite2':
                return image_classifier.SupportedModels.EFFICIENTNET_LITE2
            else:
                return image_classifier.SupportedModels.MOBILENET_V2
        except Exception as e:
            print(f"创建模型规格失败: {e}")
            return image_classifier.SupportedModels.MOBILENET_V2
    
    def train(self, 
              epochs: int = 10,
              batch_size: int = 32,
              learning_rate: float = 0.001,
              shuffle: bool = True) -> bool:
        """训练模型"""
        if self.train_data is None:
            if not self.prepare_data():
                return False
        
        try:
            spec = self.create_model_spec()
            
            self.model = image_classifier.create(
                self.train_data,
                model_spec=spec,
                validation_data=self.validation_data,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
                shuffle=shuffle
            )
            
            print("模型训练完成")
            return True
            
        except Exception as e:
            print(f"模型训练失败: {e}")
            return False
    
    def evaluate(self) -> Optional[Dict[str, float]]:
        """评估模型"""
        if self.model is None or self.validation_data is None:
            print("模型或验证数据未准备好")
            return None
        
        try:
            loss, accuracy = self.model.evaluate(self.validation_data)
            results = {
                'loss': loss,
                'accuracy': accuracy
            }
            
            print(f"模型评估结果:")
            print(f"损失: {loss:.4f}")
            print(f"准确率: {accuracy:.4f}")
            
            return results
            
        except Exception as e:
            print(f"模型评估失败: {e}")
            return None
    
    def export_model(self, export_dir: str, model_name: str = "classifier") -> bool:
        """导出模型"""
        if self.model is None:
            print("模型未训练")
            return False
        
        try:
            os.makedirs(export_dir, exist_ok=True)
            export_path = os.path.join(export_dir, f"{model_name}.tflite")
            
            self.model.export_model(export_path)
            print(f"模型已导出到: {export_path}")
            
            # 导出标签文件
            labels_path = os.path.join(export_dir, f"{model_name}_labels.txt")
            with open(labels_path, 'w', encoding='utf-8') as f:
                for label in self.model.model_spec.config.label_names:
                    f.write(f"{label}\n")
            print(f"标签文件已导出到: {labels_path}")
            
            return True
            
        except Exception as e:
            print(f"模型导出失败: {e}")
            return False


class ObjectDetectorTrainer:
    """目标检测器训练器 (高级用法)"""
    
    def __init__(self, 
                 data_dir: str,
                 annotations_dir: str,
                 validation_split: float = 0.2,
                 model_spec: str = 'mobilenet_v2'):
        """初始化训练器"""
        if not MODEL_MAKER_AVAILABLE:
            raise ImportError("需要安装 mediapipe-model-maker")
        
        self.data_dir = data_dir
        self.annotations_dir = annotations_dir
        self.validation_split = validation_split
        self.model_spec = model_spec
        self.model = None
        self.train_data = None
        self.validation_data = None
    
    def prepare_data(self):
        """准备训练数据"""
        try:
            # 加载PASCAL VOC格式的数据
            data = object_detector.Dataset.from_pascal_voc_folder(
                self.data_dir, 
                self.annotations_dir
            )
            
            # 分割训练集和验证集
            self.train_data, self.validation_data = data.split(self.validation_split)
            
            print(f"训练数据: {len(self.train_data)} 张")
            print(f"验证数据: {len(self.validation_data)} 张")
            
            return True
            
        except Exception as e:
            print(f"数据准备失败: {e}")
            return False
    
    def create_model_spec(self):
        """创建模型规格"""
        try:
            if self.model_spec == 'mobilenet_v2':
                return object_detector.SupportedModels.MOBILENET_V2
            else:
                return object_detector.SupportedModels.MOBILENET_V2
        except Exception as e:
            print(f"创建模型规格失败: {e}")
            return object_detector.SupportedModels.MOBILENET_V2
    
    def train(self, 
              epochs: int = 50,
              batch_size: int = 8,
              learning_rate: float = 0.3) -> bool:
        """训练模型"""
        if self.train_data is None:
            if not self.prepare_data():
                return False
        
        try:
            # 创建模型规格
            spec = self.create_model_spec()
            
            # 创建并训练模型
            self.model = object_detector.create(
                self.train_data,
                model_spec=spec,
                validation_data=self.validation_data,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate
            )
            
            print("目标检测模型训练完成")
            return True
            
        except Exception as e:
            print(f"模型训练失败: {e}")
            return False
    
    def evaluate(self) -> Optional[Dict[str, float]]:
        """评估模型"""
        if self.model is None or self.validation_data is None:
            print("模型或验证数据未准备好")
            return None
        
        try:
            loss = self.model.evaluate(self.validation_data)
            results = {'loss': loss}
            
            print(f"模型评估结果:")
            print(f"损失: {loss:.4f}")
            
            return results
            
        except Exception as e:
            print(f"模型评估失败: {e}")
            return None
    
    def export_model(self, export_dir: str, model_name: str = "detector") -> bool:
        """导出模型"""
        if self.model is None:
            print("模型未训练")
            return False
        
        try:
            os.makedirs(export_dir, exist_ok=True)
            export_path = os.path.join(export_dir, f"{model_name}.tflite")
            
            self.model.export_model(export_path)
            print(f"目标检测模型已导出到: {export_path}")
            
            return True
            
        except Exception as e:
            print(f"模型导出失败: {e}")
            return False


class DatasetPreprocessor:
    """数据集预处理器
    
    用于准备和预处理训练数据
    """
    
    @staticmethod
    def create_classification_dataset(source_dir: str, 
                                    target_dir: str,
                                    image_size: Tuple[int, int] = (224, 224),
                                    valid_extensions: List[str] = ['.jpg', '.jpeg', '.png']) -> bool:
        """创建分类数据集
        
        Args:
            source_dir: 源数据目录
            target_dir: 目标数据目录
            image_size: 图像尺寸
            valid_extensions: 有效的图像扩展名
            
        Returns:
            处理是否成功
        """
        try:
            os.makedirs(target_dir, exist_ok=True)
            
            for class_name in os.listdir(source_dir):
                class_path = os.path.join(source_dir, class_name)
                if not os.path.isdir(class_path):
                    continue
                
                target_class_path = os.path.join(target_dir, class_name)
                os.makedirs(target_class_path, exist_ok=True)
                
                for filename in os.listdir(class_path):
                    if any(filename.lower().endswith(ext) for ext in valid_extensions):
                        source_file = os.path.join(class_path, filename)
                        target_file = os.path.join(target_class_path, filename)
                        
                        # 读取并调整图像大小
                        image = cv2.imread(source_file)
                        if image is not None:
                            resized_image = cv2.resize(image, image_size)
                            cv2.imwrite(target_file, resized_image)
            
            print(f"分类数据集已创建到: {target_dir}")
            return True
            
        except Exception as e:
            print(f"创建分类数据集失败: {e}")
            return False
    
    @staticmethod
    def validate_dataset_structure(data_dir: str, min_images_per_class: int = 10) -> Dict[str, Any]:
        """验证数据集结构
        
        Args:
            data_dir: 数据目录
            min_images_per_class: 每个类别的最少图像数
            
        Returns:
            验证结果
        """
        results = {
            'valid': True,
            'classes': [],
            'image_counts': {},
            'warnings': [],
            'errors': []
        }
        
        try:
            if not os.path.exists(data_dir):
                results['valid'] = False
                results['errors'].append(f"数据目录不存在: {data_dir}")
                return results
            
            for class_name in os.listdir(data_dir):
                class_path = os.path.join(data_dir, class_name)
                if not os.path.isdir(class_path):
                    continue
                
                results['classes'].append(class_name)
                
                # 统计图像数量
                image_count = 0
                for filename in os.listdir(class_path):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_count += 1
                
                results['image_counts'][class_name] = image_count
                
                if image_count < min_images_per_class:
                    results['warnings'].append(
                        f"类别 '{class_name}' 只有 {image_count} 张图像，少于推荐的 {min_images_per_class} 张"
                    )
            
            if len(results['classes']) < 2:
                results['valid'] = False
                results['errors'].append("至少需要2个类别进行分类训练")
            
            print(f"找到 {len(results['classes'])} 个类别")
            for class_name, count in results['image_counts'].items():
                print(f"  {class_name}: {count} 张图像")
            
        except Exception as e:
            results['valid'] = False
            results['errors'].append(f"验证数据集结构失败: {e}")
        
        return results


class TrainingPipeline:
    """训练流水线
    
    整合数据预处理、模型训练和评估的完整流程
    """
    
    def __init__(self, project_name: str, base_dir: str = "./training_projects"):
        """初始化训练流水线
        
        Args:
            project_name: 项目名称
            base_dir: 基础目录
        """
        self.project_name = project_name
        self.project_dir = os.path.join(base_dir, project_name)
        self.data_dir = os.path.join(self.project_dir, "data")
        self.models_dir = os.path.join(self.project_dir, "models")
        self.logs_dir = os.path.join(self.project_dir, "logs")
        
        # 创建项目目录
        for dir_path in [self.project_dir, self.data_dir, self.models_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def run_classification_training(self, 
                                  source_data_dir: str,
                                  model_spec: str = 'mobilenet_v2',
                                  epochs: int = 10,
                                  validation_split: float = 0.2) -> Dict[str, Any]:
        """运行分类模型训练流程
        
        Args:
            source_data_dir: 源数据目录
            model_spec: 模型规格
            epochs: 训练轮数
            validation_split: 验证集比例
            
        Returns:
            训练结果
        """
        results = {'success': False, 'model_path': None, 'metrics': None}
        
        try:
            # 1. 验证数据集
            print("1. 验证数据集结构...")
            validation_results = DatasetPreprocessor.validate_dataset_structure(source_data_dir)
            if not validation_results['valid']:
                results['errors'] = validation_results['errors']
                return results
            
            # 2. 预处理数据
            print("2. 预处理数据...")
            processed_data_dir = os.path.join(self.data_dir, "processed")
            DatasetPreprocessor.create_classification_dataset(source_data_dir, processed_data_dir)
            
            # 3. 训练模型
            print("3. 训练模型...")
            trainer = ImageClassifierTrainer(
                processed_data_dir, 
                validation_split=validation_split,
                model_spec=model_spec
            )
            
            if trainer.train(epochs=epochs):
                # 4. 评估模型
                print("4. 评估模型...")
                metrics = trainer.evaluate()
                
                # 5. 导出模型
                print("5. 导出模型...")
                model_name = f"{self.project_name}_{model_spec}"
                if trainer.export_model(self.models_dir, model_name):
                    results['success'] = True
                    results['model_path'] = os.path.join(self.models_dir, f"{model_name}.tflite")
                    results['metrics'] = metrics
            
        except Exception as e:
            results['error'] = str(e)
            print(f"训练流程失败: {e}")
        
        return results 