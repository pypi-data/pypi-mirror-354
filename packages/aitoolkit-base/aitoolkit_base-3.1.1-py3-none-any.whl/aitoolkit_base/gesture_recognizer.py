from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError
from .utils import ModelManager, VisUtil
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerResult
from mediapipe.framework.formats import landmark_pb2
from typing import List, Tuple
import numpy as np
import cv2
import mediapipe as mp
import time
import pathlib
from collections import deque
import threading

class GestureRecognizerError(Exception):
    """手势识别错误"""
    pass

class GestureRecognizer(BaseMediaPipeDetector):
    """
    手势识别器，封装了MediaPipe的GestureRecognizer。
    """
    def __init__(self, **kwargs):
        """
        初始化手势识别器。

        Args:
            **kwargs: 传入BaseMediaPipeDetector的参数。
                      会自动处理 input_source, running_mode, 以及其他MediaPipe选项。
                      例如:
                      - num_hands
                      - min_hand_detection_confidence
        """
        # 保存GestureRecognizer特有的参数
        self.model_path = ModelManager.get_model_path('gesture_recognizer.task')
        self.async_method_name = 'recognize_async'
        self.num_hands = kwargs.pop('num_hands', 2)
        self.min_hand_detection_confidence = kwargs.pop('min_hand_detection_confidence', 0.5)
        self.min_hand_presence_confidence = kwargs.pop('min_hand_presence_confidence', 0.5)
        self.min_tracking_confidence = kwargs.pop('min_tracking_confidence', 0.5)
        
        # 跳帧控制
        self._last_frame_time = 0
        self._target_fps = 30  # 目标FPS
        self._min_process_interval = 1.0 / self._target_fps
        self._skip_frame_count = 0
        
        # 调用父类初始化
        super().__init__(async_method_name='recognize_async', **kwargs)
        
        # 性能监控
        self._fps_counter = 0
        self._fps = 0
        self._start_time = time.time()
        self._fps_avg_frame_count = 10
        
        # 同步控制
        self._result_lock = threading.RLock()
        self._latest_result = None
        self._latest_frame = None
        
        # 如果是图片模式，立即处理输入图片
        if self.running_mode == vision.RunningMode.IMAGE:
            self._process_input_source(self.model_path)
            
    def _initialize_detector(self):
        """
        根据运行模式初始化MediaPipe手势识别器。
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
            
            options = vision.GestureRecognizerOptions(**options_args)
            self.detector = vision.GestureRecognizer.create_from_options(options)
        except Exception as e:
            raise BaseMediaPipeError(f"初始化手势识别器失败: {e}")

    def _process_input_source(self, input_source):
        """
        处理输入源
        """
        try:
            if isinstance(input_source, (str, pathlib.Path)):
                image = cv2.imread(str(input_source))
                if image is None:
                    raise ValueError(f"无法读取图片: {input_source}")
            else:
                image = input_source
                
            # 转换为RGB格式
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            
            # 图片模式下直接进行同步检测
            self._latest_result = self.detector.recognize(mp_image)
            self._latest_frame = image
            
        except Exception as e:
            raise GestureRecognizerError(f"处理输入源失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        return detection_result

    def _can_process_frame(self, timestamp_ms):
        """
        判断是否可以处理当前帧，用于控制帧率
        """
        current_time = time.time()
        elapsed = current_time - self._last_frame_time
        
        # 如果距离上次处理的时间小于最小处理间隔，则跳过此帧
        if elapsed < self._min_process_interval:
            self._skip_frame_count += 1
            return False
            
        self._last_frame_time = current_time
        return True

    def run(self, frame: np.ndarray) -> GestureRecognizerResult:
        """
        对输入的图像帧进行手势识别。

        Args:
            frame: BGR格式的图像帧。

        Returns:
            GestureRecognizerResult: MediaPipe的手势识别结果。
        """
        if self.running_mode == vision.RunningMode.IMAGE:
            # 图片模式，同步执行
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            return self.detector.recognize(mp_image)
        
        elif self.running_mode == vision.RunningMode.LIVE_STREAM:
            # 视频流模式，异步执行
            timestamp_ms = int(time.time() * 1000)
            if not self._can_process_frame(timestamp_ms):
                return self._latest_result

            self._latest_frame = frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # GestureRecognizer 使用 recognize_async
            self.detector.recognize_async(mp_image, timestamp_ms)
            return self._latest_result
            
        else:
            raise ValueError(f"不支持的运行模式: {self.running_mode}")

    def draw(self, image: np.ndarray, results: GestureRecognizerResult) -> np.ndarray:
        """
        在图像上绘制手势识别结果。

        Args:
            image: 原始图像 (BGR)。
            results: run() 方法返回的检测结果。

        Returns:
            绘制了手势和关键点的图像。
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

            if results.gestures and i < len(results.gestures) and results.gestures[i]:
                gesture = results.gestures[i][0]
                category_name = gesture.category_name
                score = round(gesture.score, 2)
                
                wrist_landmark = hand_landmarks_list[0]
                h, w, _ = vis_image.shape
                text_origin = (int(wrist_landmark.x * w), int(wrist_landmark.y * h) - 15)
                
                cv2.putText(vis_image, f'{category_name} ({score})', 
                            text_origin, 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, (50, 205, 50), 2, cv2.LINE_AA)
                            
        return vis_image

    def get_fps(self):
        """获取当前处理帧率"""
        return self._fps

    def get_skipped_frames(self):
        """获取跳过的帧数"""
        return self._skip_frame_count

    def close(self):
        """关闭检测器，释放资源"""
        if hasattr(self, 'detector') and self.detector:
            self.detector.close()
            print("手势识别器已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_gestures(self, results: GestureRecognizerResult) -> List[dict]:
        """
        从结果中提取所有识别到的手势名称。

        Args:
            results: run() 方法返回的检测结果。

        Returns:
            一个字典列表，每个字典包含手势的 'category' 和 'score'。
        """
        if not results or not results.gestures:
            return []
        
        gestures_info = []
        for gesture_list in results.gestures:
            if gesture_list:
                gestures_info.append({
                    "category": gesture_list[0].category_name,
                    "score": gesture_list[0].score
                })
        return gestures_info