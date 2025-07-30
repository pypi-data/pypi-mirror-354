import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import time
import pathlib
from typing import List, Tuple

from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError
from .utils import ModelManager, VisUtil

class HandLandmarkerError(Exception):
    """手部关键点检测错误"""
    pass

class HandLandmarker(BaseMediaPipeDetector):
    """
    手部关键点检测器，封装了MediaPipe的HandLandmarker。
    """
    def __init__(self, **kwargs):
        """
        初始化手部关键点检测器。

        Args:
            **kwargs: 传入BaseMediaPipeDetector的参数。
                      会自动处理 input_source, running_mode, 以及其他MediaPipe选项。
                      例如:
                      - num_hands
                      - min_hand_detection_confidence
        """
        # 保存HandLandmarker特有的参数
        self.model_path = ModelManager.get_model_path('hand_landmarker.task')
        self.async_method_name = 'detect_async'
        self.num_hands = kwargs.pop('num_hands', 2)
        self.min_hand_detection_confidence = kwargs.pop('min_hand_detection_confidence', 0.5)
        self.min_hand_presence_confidence = kwargs.pop('min_hand_presence_confidence', 0.5)
        
        # 记录帧率控制参数
        self._last_frame_time = 0
        self._min_process_interval = 1.0 / 30  # 控制最大30FPS
        self._skip_frame_count = 0
        
        # 调用父类初始化
        super().__init__(async_method_name='detect_async', **kwargs)

    def _initialize_detector(self):
        """
        根据运行模式初始化MediaPipe手部关键点检测器。
        """
        try:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            
            options_args = {
                'base_options': base_options,
                'running_mode': self.running_mode,
                'num_hands': self.num_hands,
                'min_hand_detection_confidence': self.min_hand_detection_confidence,
                'min_hand_presence_confidence': self.min_hand_presence_confidence,
                'min_tracking_confidence': self.min_tracking_confidence,
            }
            
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                options_args['result_callback'] = self._save_result
            
            options = vision.HandLandmarkerOptions(**options_args)
            self.detector = vision.HandLandmarker.create_from_options(options)
        except Exception as e:
            raise BaseMediaPipeError(f"初始化手部关键点检测器失败: {e}")

    def draw(self, image: np.ndarray, results: HandLandmarkerResult) -> np.ndarray:
        """
        在图像上绘制手部关键点检测结果。

        Args:
            image: 原始图像 (BGR)。
            results: run() 方法返回的检测结果。

        Returns:
            绘制了关键点的图像。
        """
        if not results or not results.hand_landmarks:
            return image
        
        vis_image = image.copy()
        
        for i, hand_landmarks_list in enumerate(results.hand_landmarks):
            handedness = results.handedness[i] if results.handedness and i < len(results.handedness) else None
            
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) 
                for landmark in hand_landmarks_list
            ])

            if handedness:
                VisUtil.draw_hand_landmarks(
                    vis_image,
                    hand_landmarks_proto,
                    handedness
                )
                            
        return vis_image

    def _save_result(self, result, output_image, timestamp_ms):
        """回调函数，用于处理检测结果"""
        with self._result_lock:
            self._latest_result = result
        
        # 更新FPS计数
        if self._fps_counter % self._fps_avg_frame_count == 0:
            self._fps = self._fps_avg_frame_count / (time.time() - self._start_time)
            self._start_time = time.time()
        
        self._fps_counter += 1
        
        # 如果用户提供了回调，则调用它
        if self.result_callback:
            self.result_callback(result, output_image, timestamp_ms)
    
    def _process_input_source(self, input_source):
        """处理输入源"""
        try:
            if isinstance(input_source, (str, pathlib.Path)):
                image = cv2.imread(str(input_source))
                if image is None:
                    raise ValueError(f"无法读取图片: {input_source}")
            else:
                image = input_source
            
            # 转换为RGB格式并检测
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            self._latest_result = self.detector.detect(mp_image)
            self._latest_frame = image
            
        except Exception as e:
            raise HandLandmarkerError(f"处理输入源失败: {str(e)}")
    
    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        if not detection_result or not detection_result.hand_landmarks:
            return None
        
        h, w = image_shape[:2]
        hands_data = []
        
        for hand_landmarks, handedness in zip(detection_result.hand_landmarks, detection_result.handedness):
            # 转换关键点坐标
            landmarks = []
            for landmark in hand_landmarks:
                landmarks.append((int(landmark.x * w), int(landmark.y * h), landmark.z))
            
            hands_data.append({
                'landmarks': landmarks,
                'handedness': handedness[0].category_name,
                'score': handedness[0].score
            })
        
        return hands_data
    
    def run(self, frame=None):
        """运行检测"""
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    raise ValueError("图片模式下不应该传入frame参数")
                return self._latest_result
            
            if frame is None:
                raise ValueError("实时流模式下必须传入frame参数")
            
            # 计算帧间隔，控制处理频率
            current_time = time.time()
            elapsed = current_time - self._last_frame_time
            
            # 控制帧率，避免过度处理导致积压
            if elapsed < self._min_process_interval:
                self._skip_frame_count += 1
                return self._latest_result
            
            # 记录时间以控制帧率
            self._last_frame_time = current_time
            
            # 转换为RGB并使用适当的检测方法
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # 确保在LIVE_STREAM模式下使用正确的方法
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                # 使用异步方法
                self.detector.detect_async(mp_image, time.time_ns() // 1_000_000)
                
                with self._result_lock:
                    self._latest_frame = frame
                    return self._latest_result
            else:
                # 如果不是LIVE_STREAM模式，则使用同步方法
                with self._result_lock:
                    self._latest_result = self.detector.detect(mp_image)
                    self._latest_frame = frame
                    
                    # 更新FPS计数
                    if self._fps_counter % self._fps_avg_frame_count == 0:
                        self._fps = self._fps_avg_frame_count / (time.time() - self._start_time)
                        self._start_time = time.time()
                    
                    self._fps_counter += 1
                    
                    # 如果用户提供了回调，则调用它
                    if self.result_callback:
                        self.result_callback(self._latest_result, frame, time.time_ns() // 1_000_000)
                    
                    return self._latest_result
            
        except Exception as e:
            raise HandLandmarkerError(f"运行检测失败: {str(e)}")
    
    def get_fps(self):
        """获取当前FPS"""
        return self._fps
    
    def get_skipped_frames(self):
        """获取跳过的帧数"""
        return self._skip_frame_count
    
    def close(self):
        """释放资源"""
        # 释放检测器
        if hasattr(self, 'detector'):
            self.detector.close()
        
        # 清理内部数据结构
        with self._result_lock:
            self._latest_frame = None
            self._latest_result = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 

    def get_landmarks(self, results: HandLandmarkerResult) -> List[List[Tuple[int, int]]]:
        """从结果中提取所有手部关键点坐标
        Args:
            results: run() 方法返回的检测结果
            
        Returns:
            手部关键点坐标列表
        """
        if not results or not results.hand_landmarks:
            return []
        
        landmarks_list = []
        for hand_landmarks in results.hand_landmarks:
            landmarks = []
            for landmark in hand_landmarks:
                landmarks.append((int(landmark.x * self._latest_frame.shape[1]), int(landmark.y * self._latest_frame.shape[0])))
            landmarks_list.append(landmarks)
        
        return landmarks_list
    
    def get_world_landmarks(self, results: HandLandmarkerResult) -> List[List[Tuple[float, float, float]]]:
        """从结果中提取所有手部的世界坐标
        
        Args:
            results: run() 方法返回的检测结果
            
        Returns:
            手部世界坐标列表
        """
        if not results or not results.hand_world_landmarks:
            return []
        
        landmarks_list = []
        for hand_world_landmarks in results.hand_world_landmarks:
            landmark_coords = []
            for landmark in hand_world_landmarks:
                landmark_coords.append((landmark.x, landmark.y, landmark.z))
            landmarks_list.append(landmark_coords)
            
        return landmarks_list 