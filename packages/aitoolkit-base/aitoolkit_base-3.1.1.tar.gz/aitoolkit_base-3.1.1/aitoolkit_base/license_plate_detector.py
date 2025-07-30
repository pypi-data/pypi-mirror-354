#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
License Plate Detection Module
Car license plate detection and recognition using OpenCV
"""

import cv2
import numpy as np
import re
from typing import List, Optional, Dict, Any, Tuple
from .base_detector import BaseDetector


class LicensePlateDetector(BaseDetector):
    """License Plate Detector
    
    Detect and recognize license plates using traditional CV methods
    """
    
    def __init__(self, 
                 min_area: int = 1000,
                 max_area: int = 50000,
                 min_aspect_ratio: float = 2.0,
                 max_aspect_ratio: float = 6.0,
                 **kwargs):
        """Initialize license plate detector
        
        Args:
            min_area: Minimum contour area for plate detection
            max_area: Maximum contour area for plate detection  
            min_aspect_ratio: Minimum width/height ratio
            max_aspect_ratio: Maximum width/height ratio
        """
        super().__init__(**kwargs)
        self.min_area = min_area
        self.max_area = max_area
        self.min_aspect_ratio = min_aspect_ratio
        self.max_aspect_ratio = max_aspect_ratio
        
        # Cascade classifier for initial detection (optional)
        self.cascade = None
        self._try_load_cascade()
        
        print("License Plate Detector initialized")
    
    def _try_load_cascade(self):
        """Try to load Haar cascade for license plate detection"""
        try:
            # Try to load pre-trained cascade (if available)
            cascade_path = cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml'
            self.cascade = cv2.CascadeClassifier(cascade_path)
            if self.cascade.empty():
                self.cascade = None
        except:
            self.cascade = None
    
    def run(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        处理图像以检测和识别车牌
        
        Args:
            image: 输入图像
            
        Returns:
            包含已识别文本的检测到的车牌区域列表
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 方法1: 首先尝试级联分类器
        plates_cascade = []
        if self.cascade is not None:
            plates_cascade = self._detect_with_cascade(gray)
        
        # 方法2: 基于轮廓的检测
        plates_contour = self._detect_with_contours(gray)
        
        # 合并结果并移除重复项
        all_plates = self._remove_duplicate_plates(plates_cascade + plates_contour)

        # 为每个车牌识别文本
        for plate in all_plates:
            plate['text'] = self.recognize_text(image, plate['box'])
        
        return all_plates
    
    def _detect_with_cascade(self, gray: np.ndarray) -> List[Dict[str, Any]]:
        """Detect plates using Haar cascade"""
        plates = []
        
        try:
            detected = self.cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(100, 30)
            )
            
            for (x, y, w, h) in detected:
                aspect_ratio = w / h
                if self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio:
                    plates.append({
                        'box': (x, y, x + w, y + h),
                        'confidence': 0.8,  # 级联分类器的默认置信度
                        'method': 'cascade'
                    })
        except:
            pass
        
        return plates
    
    def _detect_with_contours(self, gray: np.ndarray) -> List[Dict[str, Any]]:
        """Detect plates using contour analysis"""
        plates = []
        
        try:
            # Apply bilateral filter to reduce noise
            filtered = cv2.bilateralFilter(gray, 11, 17, 17)
            
            # Edge detection
            edges = cv2.Canny(filtered, 30, 200)
            
            # Morphological operations to close gaps
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                if self.min_area <= area <= self.max_area:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    if self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio:
                        # Check if the region looks like a license plate
                        confidence = self._calculate_plate_confidence(gray[y:y+h, x:x+w])
                        
                        if confidence > 0.3:  # 最低置信度阈值
                            plates.append({
                                'box': (x, y, x + w, y + h),
                                'confidence': confidence,
                                'method': 'contour'
                            })
        
        except Exception as e:
            print(f"Contour detection error: {e}")
        
        return plates
    
    def _calculate_plate_confidence(self, roi: np.ndarray) -> float:
        """Calculate confidence that ROI contains a license plate"""
        if roi.size == 0:
            return 0.0
        
        try:
            # Check for horizontal edges (typical in license plates)
            edges = cv2.Canny(roi, 50, 150)
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
            horizontal_edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
            
            # Calculate ratio of horizontal edges
            total_edges = np.sum(edges > 0)
            horizontal_ratio = np.sum(horizontal_edges > 0) / max(total_edges, 1)
            
            # Check for text-like patterns
            _, binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Calculate connected components (characters)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
            
            # Filter components by size (character-like)
            char_count = 0
            for i in range(1, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                width = stats[i, cv2.CC_STAT_WIDTH]
                height = stats[i, cv2.CC_STAT_HEIGHT]
                
                if 20 <= area <= 1000 and 5 <= width <= 50 and 10 <= height <= 50:
                    char_count += 1
            
            # Combine features for confidence score
            char_score = min(char_count / 8.0, 1.0)  # Normalize to 8 characters
            edge_score = horizontal_ratio
            
            confidence = (char_score * 0.6 + edge_score * 0.4)
            return min(confidence, 1.0)
            
        except:
            return 0.0
    
    def _remove_duplicate_plates(self, plates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate plate detections"""
        if len(plates) <= 1:
            return plates
        
        # Sort by confidence
        plates.sort(key=lambda x: x['confidence'], reverse=True)
        
        filtered_plates = []
        for plate in plates:
            is_duplicate = False
            
            for existing in filtered_plates:
                if self._calculate_overlap(plate['box'], existing['box']) > 0.5:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered_plates.append(plate)
        
        return filtered_plates
    
    def _calculate_overlap(self, bbox1: Tuple[int, int, int, int], bbox2: Tuple[int, int, int, int]) -> float:
        """Calculate overlap ratio between two bounding boxes"""
        x1, y1, x1_max, y1_max = bbox1
        x2, y2, x2_max, y2_max = bbox2
        
        # Calculate intersection
        left = max(x1, x2)
        top = max(y1, y2)
        right = min(x1_max, x2_max)
        bottom = min(y1_max, y2_max)
        
        if left >= right or top >= bottom:
            return 0.0
        
        intersection = (right - left) * (bottom - top)
        area1 = (x1_max - x1) * (y1_max - y1)
        area2 = (x2_max - x2) * (y2_max - y2)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def recognize_text(self, image: np.ndarray, box: Tuple[int, int, int, int]) -> str:
        """
        识别车牌区域中的文本
        
        Args:
            image: 原始图像
            box: 车牌的边界框 (xmin, ymin, xmax, ymax)
            
        Returns:
            识别出的文本
        """
        x, y, x_max, y_max = box
        roi = image[y:y_max, x:x_max]
        
        if roi.size == 0:
            return ""
        
        try:
            # Tesseract更适合此任务
            import pytesseract
            # 为更好的OCR进行预处理
            enhanced_roi = self._enhance_for_ocr(roi)
            
            # 使用针对车牌的特定配置
            config = "--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            text = pytesseract.image_to_string(enhanced_roi, lang='eng', config=config)
            
            # 清理结果
            return re.sub(r'[\W_]+', '', text).upper()
            
        except ImportError:
            # 如果未安装tesseract，则回退
            return self._simple_text_recognition(roi)
        except Exception as e:
            print(f"Tesseract识别错误: {e}")
            return self._simple_text_recognition(roi)
    
    def _enhance_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """Enhance image for better OCR results"""
        # Apply adaptive thresholding
        enhanced = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_CLOSE, kernel)
        
        return enhanced
    
    def _simple_text_recognition(self, image: np.ndarray) -> str:
        """Simple template-based character recognition (fallback)"""
        # This is a simplified implementation
        # In practice, you'd use machine learning or template matching
        
        # Find connected components (characters)
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
        
        characters = []
        for i in range(1, num_labels):
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            area = stats[i, cv2.CC_STAT_AREA]
            
            # Filter by size (character-like components)
            if 20 <= area <= 1000 and 5 <= w <= 50 and 10 <= h <= 50:
                characters.append((x, w, h))  # Store position and size
        
        # Sort characters by x position (left to right)
        characters.sort()
        
        # Simple heuristic: return placeholder based on character count
        char_count = len(characters)
        if 4 <= char_count <= 10:
            return "PLATE" + "X" * (char_count - 5) if char_count > 5 else "PLATE"
        
        return ""
    
    def draw(self, image: np.ndarray, plates: List[Dict[str, Any]]) -> np.ndarray:
        """
        在图像上绘制车牌检测和识别结果
        
        Args:
            image: BGR格式的图像
            plates: run() 方法返回的车牌数据列表
            
        Returns:
            标注后的图像
        """
        if not plates:
            return image

        vis_image = image.copy()
        from .utils import vis_util

        for plate in plates:
            box = plate.get('box')
            text = plate.get('text', '')
            confidence = plate.get('confidence', 0)
            display_text = f"{text} ({confidence:.2f})"
            
            if box:
                vis_util.draw_ocr_box(vis_image, box, display_text, color=(0, 255, 0))
                
        return vis_image
    
    def get_plate_regions(self, image: np.ndarray) -> List[np.ndarray]:
        """获取检测到的车牌的ROI
        
        Args:
            image: Input image
            
        Returns:
            List of extracted plate region images
        """
        plates = self.run(image)
        regions = []
        
        for plate in plates:
            bbox = plate['box']
            x, y, x_max, y_max = bbox
            
            # Add some padding
            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x_max + padding)
            y2 = min(image.shape[0], y_max + padding)
            
            region = image[y1:y2, x1:x2]
            if region.size > 0:
                regions.append(region) 