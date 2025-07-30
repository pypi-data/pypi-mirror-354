#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Depth Estimation Module
Advanced monocular depth estimation using DL models and traditional CV
"""

import cv2
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from .base_detector import BaseDetector


class DepthEstimator(BaseDetector):
    """Advanced Depth Estimator
    
    Estimate depth from single images using deep learning models and traditional CV
    """
    
    def __init__(self, 
                 method: str = 'midas',
                 model_type: str = 'small',
                 **kwargs):
        """Initialize depth estimator
        
        Args:
            method: Depth estimation method ('midas', 'dpt', 'traditional')
            model_type: Model size ('small', 'large') for DL models
        """
        super().__init__(**kwargs)
        self.method = method
        self.model_type = model_type
        
        # Try to load deep learning models
        self.dl_model = None
        self.transform = None
        
        if method in ['midas', 'dpt']:
            self._load_dl_model()
        
        # Fallback stereo matcher
        if method == 'traditional':
            self.stereo_matcher = self._create_stereo_matcher()
        else:
            self.stereo_matcher = None
        
        # Previous frame for motion-based estimation
        self.prev_frame = None
        
        print(f"Depth Estimator initialized (method: {method}, model: {model_type})")
    
    def _load_dl_model(self):
        """Load deep learning depth estimation model"""
        try:
            # Try to import torch and load MiDaS
            import torch
            
            if self.method == 'midas':
                # Load MiDaS model
                if self.model_type == 'small':
                    model_name = 'MiDaS_small'
                else:
                    model_name = 'MiDaS'
                
                self.dl_model = torch.hub.load('intel-isl/MiDaS', model_name, pretrained=True)
                self.dl_model.eval()
                
                # Load transforms
                midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
                if self.model_type == 'small':
                    self.transform = midas_transforms.small_transform
                else:
                    self.transform = midas_transforms.default_transform
                
                print(f"✅ MiDaS {self.model_type} model loaded successfully")
                
            elif self.method == 'dpt':
                # Try to load DPT model (if available)
                try:
                    self.dl_model = torch.hub.load('intel-isl/MiDaS', 'DPT_Large', pretrained=True)
                    self.dl_model.eval()
                    
                    midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
                    self.transform = midas_transforms.dpt_transform
                    
                    print("✅ DPT model loaded successfully")
                except:
                    print("⚠️ DPT model not available, falling back to MiDaS")
                    self.method = 'midas'
                    self._load_dl_model()
                    return
            
        except ImportError:
            print("⚠️ PyTorch not installed, using traditional methods")
            self.method = 'traditional'
            self.dl_model = None
            self.transform = None
        except Exception as e:
            print(f"⚠️ Failed to load DL model: {e}, using traditional methods")
            self.method = 'traditional'
            self.dl_model = None
            self.transform = None
    
    def _create_stereo_matcher(self):
        """Create stereo matcher for traditional methods"""
        try:
            min_disp = 0
            num_disp = 16 * 5
            block_size = 11
            
            stereo = cv2.StereoSGBM_create(
                minDisparity=min_disp,
                numDisparities=num_disp,
                blockSize=block_size,
                P1=8 * 3 * block_size ** 2,
                P2=32 * 3 * block_size ** 2,
                disp12MaxDiff=1,
                uniquenessRatio=10,
                speckleWindowSize=100,
                speckleRange=32
            )
            
            return stereo
        except:
            return None
    
    def _process_image(self, image: np.ndarray) -> Dict[str, Any]:
        """Process image to estimate depth"""
        if self.method in ['midas', 'dpt'] and self.dl_model is not None:
            return self._depth_from_dl_model(image)
        else:
            return self._depth_from_traditional(image)
    
    def _depth_from_dl_model(self, image: np.ndarray) -> Dict[str, Any]:
        """Estimate depth using deep learning model"""
        try:
            import torch
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Apply transforms
            input_tensor = self.transform(rgb_image).unsqueeze(0)
            
            # Run inference
            with torch.no_grad():
                depth_map = self.dl_model(input_tensor)
                depth_map = torch.nn.functional.interpolate(
                    depth_map.unsqueeze(1),
                    size=image.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()
            
            # Convert to numpy and normalize
            depth_map = depth_map.cpu().numpy()
            
            # Normalize to 0-255 (invert for better visualization)
            depth_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
            depth_uint8 = 255 - depth_normalized.astype(np.uint8)  # Invert so closer = brighter
            
            # Apply slight smoothing
            depth_uint8 = cv2.medianBlur(depth_uint8, 3)
            
            # Calculate statistics
            mean_depth = np.mean(depth_uint8)
            std_depth = np.std(depth_uint8)
            
            return {
                'depth_map': depth_uint8,
                'raw_depth': depth_map,
                'method': f'{self.method}_{self.model_type}',
                'mean_depth': mean_depth,
                'std_depth': std_depth,
                'confidence': 0.9  # High confidence for DL models
            }
            
        except Exception as e:
            print(f"DL depth estimation error: {e}")
            return self._depth_from_traditional(image)
    
    def _depth_from_traditional(self, image: np.ndarray) -> Dict[str, Any]:
        """Estimate depth using traditional computer vision methods"""
        # Use improved focus-based method
        return self._depth_from_improved_focus(image)
    
    def _depth_from_improved_focus(self, image: np.ndarray) -> Dict[str, Any]:
        """Improved focus-based depth estimation"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Multi-scale focus detection
            focus_maps = []
            scales = [0.5, 1.0, 1.5, 2.0]
            
            for scale in scales:
                # Resize image
                if scale != 1.0:
                    h, w = gray.shape
                    new_h, new_w = int(h * scale), int(w * scale)
                    scaled = cv2.resize(gray, (new_w, new_h))
                else:
                    scaled = gray
                
                # Calculate focus measure using multiple methods
                laplacian = cv2.Laplacian(scaled, cv2.CV_64F, ksize=3)
                sobel_x = cv2.Sobel(scaled, cv2.CV_64F, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(scaled, cv2.CV_64F, 0, 1, ksize=3)
                
                # Combine gradients
                gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
                
                # Weight by Laplacian variance
                laplacian_var = cv2.GaussianBlur(np.abs(laplacian), (5, 5), 0)
                gradient_smooth = cv2.GaussianBlur(gradient_magnitude, (5, 5), 0)
                
                # Combine focus measures
                focus_measure = 0.6 * laplacian_var + 0.4 * gradient_smooth
                
                # Resize back to original size
                if scale != 1.0:
                    focus_measure = cv2.resize(focus_measure, (gray.shape[1], gray.shape[0]))
                
                focus_maps.append(focus_measure)
            
            # Combine multi-scale focus maps
            combined_focus = np.mean(focus_maps, axis=0)
            
            # Apply edge-preserving smoothing
            combined_focus = cv2.bilateralFilter(combined_focus.astype(np.float32), 9, 75, 75)
            
            # Enhance depth contrast
            combined_focus = cv2.convertScaleAbs(combined_focus, alpha=1.5, beta=10)
            
            # Normalize to 0-255
            depth_map = cv2.normalize(combined_focus, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Invert so higher focus = closer = brighter
            depth_map = 255 - depth_map
            
            # Final smoothing
            depth_map = cv2.medianBlur(depth_map, 5)
            
            # Calculate statistics
            mean_depth = np.mean(depth_map)
            std_depth = np.std(depth_map)
            
            # Calculate confidence based on focus variation
            confidence = min(std_depth / 50.0, 1.0)  # Normalize by expected range
            
            return {
                'depth_map': depth_map,
                'method': 'improved_focus',
                'mean_depth': mean_depth,
                'std_depth': std_depth,
                'confidence': confidence
            }
            
        except Exception as e:
            print(f"Traditional depth estimation error: {e}")
            return self._create_empty_result()
    
    def _calculate_depth_confidence(self, depth_map: np.ndarray) -> float:
        """Calculate confidence in depth estimation"""
        try:
            variance = np.var(depth_map)
            confidence = min(variance / 2000.0, 1.0)
            return confidence
        except:
            return 0.0
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """Create empty result for error cases"""
        return {
            'depth_map': None,
            'method': self.method,
            'mean_depth': 0.0,
            'std_depth': 0.0,
            'confidence': 0.0
        }
    
    def estimate_stereo_depth(self, left_image: np.ndarray, right_image: np.ndarray) -> Dict[str, Any]:
        """Estimate depth from stereo image pair"""
        if self.stereo_matcher is None:
            self.stereo_matcher = self._create_stereo_matcher()
        
        if self.stereo_matcher is None:
            print("Stereo matcher not available")
            return self._create_empty_result()
        
        try:
            left_gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY) if len(left_image.shape) == 3 else left_image
            right_gray = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY) if len(right_image.shape) == 3 else right_image
            
            disparity = self.stereo_matcher.compute(left_gray, right_gray)
            disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            depth_map = 255 - disparity_normalized
            
            mean_depth = np.mean(depth_map)
            std_depth = np.std(depth_map)
            
            return {
                'depth_map': depth_map,
                'disparity_map': disparity_normalized,
                'method': 'stereo_sgbm',
                'mean_depth': mean_depth,
                'std_depth': std_depth,
                'confidence': self._calculate_depth_confidence(depth_map)
            }
            
        except Exception as e:
            print(f"Stereo depth estimation error: {e}")
            return self._create_empty_result()
    
    def draw(self, image: np.ndarray, depth_result: Dict[str, Any] = None) -> np.ndarray:
        """Draw depth estimation visualization
        
        Args:
            image: Original image
            depth_result: Depth estimation result
            
        Returns:
            Image with depth visualization
        """
        if depth_result is None:
            depth_result = self.run(image)
        
        if depth_result['depth_map'] is None:
            return image.copy()
        
        depth_map = depth_result['depth_map']
        
        try:
            # Create colorized depth map
            depth_colored = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)
            
            # Create side-by-side visualization
            h, w = image.shape[:2]
            result_image = np.zeros((h, w * 2, 3), dtype=np.uint8)
            
            # Original image on the left
            result_image[:, :w] = image
            
            # Depth map on the right
            result_image[:, w:] = depth_colored
            
            # Add text overlay
            method = depth_result['method']
            confidence = depth_result['confidence']
            mean_depth = depth_result['mean_depth']
            
            # Text for original image
            cv2.putText(result_image, "Original", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Text for depth map
            cv2.putText(result_image, f"Depth ({method})", (w + 10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(result_image, f"Confidence: {confidence:.2f}", (w + 10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(result_image, f"Mean Depth: {mean_depth:.1f}", (w + 10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add depth scale
            scale_height = 20
            scale_width = 200
            scale_x = w + 10
            scale_y = h - 50
            
            # Create depth scale bar
            scale_bar = np.linspace(0, 255, scale_width, dtype=np.uint8)
            scale_bar = np.tile(scale_bar, (scale_height, 1))
            scale_colored = cv2.applyColorMap(scale_bar, cv2.COLORMAP_JET)
            
            # Add scale to image
            result_image[scale_y:scale_y+scale_height, scale_x:scale_x+scale_width] = scale_colored
            
            # Scale labels
            cv2.putText(result_image, "Near", (scale_x, scale_y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(result_image, "Far", (scale_x + scale_width - 25, scale_y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            return result_image
            
        except Exception as e:
            print(f"Depth visualization error: {e}")
            return image.copy()
    
    def get_depth_at_point(self, depth_result: Dict[str, Any], x: int, y: int) -> float:
        """Get depth value at specific point
        
        Args:
            depth_result: Depth estimation result
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Depth value at the point (0-255)
        """
        if depth_result['depth_map'] is None:
            return 0.0
        
        depth_map = depth_result['depth_map']
        h, w = depth_map.shape
        
        if 0 <= x < w and 0 <= y < h:
            return float(depth_map[y, x])
        
        return 0.0
    
    def create_3d_point_cloud(self, image: np.ndarray, depth_result: Dict[str, Any]) -> np.ndarray:
        """Create 3D point cloud from image and depth
        
        Args:
            image: Original image
            depth_result: Depth estimation result
            
        Returns:
            3D point cloud as Nx6 array (X, Y, Z, R, G, B)
        """
        if depth_result['depth_map'] is None:
            return np.array([])
        
        depth_map = depth_result['depth_map']
        h, w = image.shape[:2]
        
        try:
            # Create coordinate grids
            u, v = np.meshgrid(np.arange(w), np.arange(h))
            
            # Normalize depth to real units (assuming some scale)
            depth_normalized = depth_map.astype(np.float32) / 255.0 * 10.0  # 0-10 units
            
            # Simple camera projection (assumes camera at origin)
            # In practice, you'd use actual camera calibration parameters
            focal_length = w  # Simplified assumption
            
            # Calculate 3D coordinates
            x = (u - w/2) * depth_normalized / focal_length
            y = (v - h/2) * depth_normalized / focal_length
            z = depth_normalized
            
            # Get color information
            colors = image.reshape(-1, 3) / 255.0
            
            # Flatten coordinates
            points_3d = np.column_stack([
                x.flatten(),
                y.flatten(), 
                z.flatten(),
                colors[:, 2],  # R
                colors[:, 1],  # G
                colors[:, 0]   # B
            ])
            
            # Filter out invalid points
            valid_mask = (points_3d[:, 2] > 0) & (points_3d[:, 2] < 9.0)
            points_3d = points_3d[valid_mask]
            
            return points_3d
            
        except Exception as e:
            print(f"Point cloud creation error: {e}")
            return np.array([])
    
    def save_depth_map(self, depth_result: Dict[str, Any], filename: str) -> bool:
        """Save depth map to file
        
        Args:
            depth_result: Depth estimation result
            filename: Output filename
            
        Returns:
            Success status
        """
        if depth_result['depth_map'] is None:
            return False
        
        try:
            cv2.imwrite(filename, depth_result['depth_map'])
            print(f"Depth map saved to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save depth map: {e}")
            return False 