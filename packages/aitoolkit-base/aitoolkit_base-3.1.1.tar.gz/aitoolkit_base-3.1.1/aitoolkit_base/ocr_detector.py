#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR Text Detection and Recognition Module
Advanced OCR using cnocr for Chinese text and Tesseract fallback
"""

import cv2
import numpy as np
import re
from typing import List, Optional, Dict, Any, Tuple
from .base_detector import BaseDetector
from .utils import VisUtil, ModelManager

# 动态导入，避免对所有用户都强制安装这些依赖
try:
    import cnocr
except ImportError:
    cnocr = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

class OCRDetectorError(Exception):
    """OCR检测器错误"""
    pass

class OCRDetector(BaseDetector):
    """
    一个通用的OCR（光学字符识别）检测器，集成了cnocr和pytesseract。
    """
    def __init__(self,
                 lang: Optional[str] = 'eng',
                 use_cnocr: bool = True,
                 use_tesseract: bool = True,
                 **kwargs):
        """
        初始化OCR检测器。

        Args:
            lang (str, optional): 主要使用的语言。'ch' 或 'cn' 会优先使用cnocr，其他则会传递给Tesseract。
            use_cnocr (bool): 是否尝试使用cnocr（对中英文场景友好）。
            use_tesseract (bool): 是否尝试使用Tesseract（需要额外安装）。
        """
        super().__init__()
        self.cnocr_detector = None
        self.tesseract_lang = lang if lang not in ['ch', 'cn'] else 'chi_sim+eng'
        self.available_engines = []
        
        # 根据lang参数决定优先引擎
        if lang in ['ch', 'cn']:
            use_cnocr = True

        if use_cnocr and cnocr:
            try:
                # cnocr的初始化可能需要下载模型，这可能会花一些时间
                self.cnocr_detector = cnocr.CnOcr(rec_model_name='ch_PP-OCRv3')
                self.available_engines.append('cnocr')
            except Exception as e:
                print(f"⚠️ cnocr 初始化失败: {e}")
        elif use_cnocr:
            print("⚠️ cnocr 未安装。运行: pip install cnocr[ort-cpu]")

        if use_tesseract and pytesseract:
            self.available_engines.append('tesseract')
        elif use_tesseract:
            print("⚠️ pytesseract 未安装。运行: pip install pytesseract, 并确保Tesseract OCR引擎已安装在您的系统中。")
        
        if not self.available_engines:
            raise OCRDetectorError("没有任何可用的OCR引擎。请安装cnocr或pytesseract。")

        print(f"OCR Detector initialized (cnocr: {'✓' if 'cnocr' in self.available_engines else '✗'}, tesseract: {'✓' if 'tesseract' in self.available_engines else '✗'})")

    def run(self, image: np.ndarray, engine: str = 'auto', **kwargs) -> List[Tuple[list, str, float]]:
        """
        在图像上运行OCR。

        Args:
            image (np.ndarray): 输入的BGR图像。
            engine (str): 要使用的OCR引擎 ('cnocr', 'tesseract', 'auto')。
                          'auto'会优先选择cnocr。
            **kwargs: 传递给特定引擎的额外参数。

        Returns:
            一个列表，每个元素是一个元组，包含(边界框, 识别文本, 置信度)。
            边界框格式: [ [x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max] ]
        """
        if engine == 'auto':
            if 'cnocr' in self.available_engines:
                selected_engine = 'cnocr'
            elif 'tesseract' in self.available_engines:
                selected_engine = 'tesseract'
            else:
                raise OCRDetectorError("没有可用的OCR引擎。")
        else:
            if engine not in self.available_engines:
                raise OCRDetectorError(f"选择的引擎 '{engine}' 不可用。可用引擎: {self.available_engines}")
            selected_engine = engine

        if selected_engine == 'cnocr':
            return self._run_cnocr(image)
        elif selected_engine == 'tesseract':
            return self._run_tesseract(image, **kwargs)
        
        return []

    def _run_cnocr(self, image: np.ndarray) -> List[Tuple[list, str, float]]:
        """使用cnocr运行OCR"""
        ocr_results = self.cnocr_detector.ocr(image)
        # 将cnocr的输出格式转换为标准格式
        formatted_results = []
        for res in ocr_results:
            box = [[int(p[0]), int(p[1])] for p in res['position']]
            text = res['text']
            score = res['score']
            formatted_results.append((box, text, score))
        return formatted_results

    def _run_tesseract(self, image: np.ndarray, **kwargs) -> List[Tuple[list, str, float]]:
        """使用Tesseract运行OCR"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 使用pytesseract获取详细的输出数据
        data = pytesseract.image_to_data(rgb_image, lang=self.tesseract_lang, output_type=pytesseract.Output.DICT, **kwargs)
        
        formatted_results = []
        n_boxes = len(data['level'])
        for i in range(n_boxes):
            # 只考虑有文本的单词级别的框
            if int(data['conf'][i]) > 0:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                text = data['text'][i]
                conf = float(data['conf'][i]) / 100.0

                if text.strip():
                    box = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
                    formatted_results.append((box, text, conf))
                    
        return formatted_results

    def draw(
        self,
        image: np.ndarray,
        results: list,
        color=(0, 255, 0),
        thickness=2
    ) -> np.ndarray:
        """
        在图像上绘制OCR结果。
        """
        vis_image = image.copy()
        for box, text, _ in results:
            # box 的格式是 [[x,y], [x,y], [x,y], [x,y]]
            # VisUtil.draw_ocr_box 需要 [xmin, ymin, xmax, ymax]
            # 我们需要先计算这个边界
            pts = np.array(box, dtype=np.int32)
            xmin, ymin = np.min(pts, axis=0)
            xmax, ymax = np.max(pts, axis=0)
            
            # 使用 VisUtil 绘制更美观的框
            vis_image = VisUtil.draw_ocr_box(vis_image, (xmin, ymin, xmax, ymax), text, color, thickness)
            
        return vis_image
        
    def close(self):
        """清理资源"""
        print("OCRDetector closed.")

    def find_text(self, text_to_find: str, ocr_results: List[dict]) -> List[Dict[str, Any]]:
        """
        在OCR结果中查找特定文本。

        Args:
            text_to_find (str): 要查找的文本。
            ocr_results (List[dict]): `run` 方法返回的OCR结果列表。

        Returns:
            一个列表，包含所有匹配文本的位置和其他信息。
        """
        matching_regions = []
        for region in ocr_results:
            if text_to_find in region['text']:
                matching_regions.append(region)
        return matching_regions

    def get_all_text(self, image: np.ndarray) -> str:
        """Extract all text from image as a single string
        
        Args:
            image: Input image
            
        Returns:
            Combined text from all detected regions
        """
        text_regions = self.run(image)
        
        # Sort by position (top to bottom, left to right)
        text_regions.sort(key=lambda r: (r[0][1], r[0][0]))
        
        # Combine all text
        all_text = '\n'.join(r[1] for r in text_regions if r[1])
        
        return all_text
    
    def search_text(self, image: np.ndarray, pattern: str) -> List[Dict[str, Any]]:
        """Search for specific text pattern in image
        
        Args:
            image: Input image
            pattern: Regular expression pattern to search for
            
        Returns:
            List of regions containing matching text
        """
        text_regions = self.run(image)
        matching_regions = []
        
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            
            for region in text_regions:
                if compiled_pattern.search(region[1]):
                    matching_regions.append(region)
        
        except re.error as e:
            print(f"Invalid regex pattern: {e}")
        
        return matching_regions 