#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Neural Style Transfer Module
Improved artistic style effects using advanced computer vision techniques
"""

import cv2
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from .base_detector import BaseDetector


class StyleTransfer(BaseDetector):
    """Advanced Style Transfer
    
    Enhanced artistic style effects with better visual quality
    """
    
    def __init__(self, 
                 style_type: str = 'oil_painting',
                 intensity: float = 1.0,
                 **kwargs):
        """Initialize style transfer
        
        Args:
            style_type: Type of style ('oil_painting', 'watercolor', 'pencil_sketch', 'cartoon', 'impressionist', 'abstract')
            intensity: Style intensity (0.0 to 2.0)
        """
        super().__init__(**kwargs)
        self.style_type = style_type
        self.intensity = max(0.0, min(2.0, intensity))
        
        # Enhanced artistic filters with better parameters
        self.artistic_filters = self._create_enhanced_filters()
        
        print(f"Enhanced Style Transfer initialized (style: {style_type}, intensity: {intensity})")
    
    def _create_enhanced_filters(self) -> Dict[str, Any]:
        """Create enhanced artistic filter parameters"""
        filters = {}
        
        # Enhanced oil painting
        filters['oil_painting'] = {
            'bilateral_params': {'d': 15, 'sigmaColor': 60, 'sigmaSpace': 60},
            'quantization_levels': 12,
            'brush_size': 7,
            'edge_threshold': 0.1,
            'color_boost': 1.2
        }
        
        # Enhanced watercolor
        filters['watercolor'] = {
            'blur_strength': 25,
            'quantization_levels': 8,
            'transparency_zones': 3,
            'paper_texture_strength': 0.3,
            'color_bleeding': True,
            'saturation_factor': 0.8
        }
        
        # Enhanced pencil sketch
        filters['pencil_sketch'] = {
            'blur_kernel': (21, 21),
            'line_detail': 2.0,
            'contrast_boost': 1.8,
            'paper_grain': True,
            'sketch_density': 0.7
        }
        
        # Enhanced cartoon
        filters['cartoon'] = {
            'bilateral_params': {'d': 9, 'sigmaColor': 50, 'sigmaSpace': 50},
            'quantization_levels': 6,
            'edge_thickness': 3,
            'saturation_boost': 1.4,
            'brightness_boost': 1.1
        }
        
        # New: Impressionist style
        filters['impressionist'] = {
            'brush_strokes': True,
            'stroke_length': 15,
            'stroke_thickness': 3,
            'color_variation': 0.3,
            'texture_strength': 0.8
        }
        
        # New: Abstract style
        filters['abstract'] = {
            'geometric_shapes': True,
            'color_reduction': 8,
            'edge_distortion': 0.5,
            'shape_simplification': True
        }
        
        return filters
    
    def run(self, image: np.ndarray) -> Dict[str, Any]:
        """Process image with enhanced style transfer"""
        if self.style_type == 'oil_painting':
            return self._apply_enhanced_oil_painting(image)
        elif self.style_type == 'watercolor':
            return self._apply_enhanced_watercolor(image)
        elif self.style_type == 'pencil_sketch':
            return self._apply_enhanced_pencil_sketch(image)
        elif self.style_type == 'cartoon':
            return self._apply_enhanced_cartoon(image)
        elif self.style_type == 'impressionist':
            return self._apply_impressionist(image)
        elif self.style_type == 'abstract':
            return self._apply_abstract(image)
        else:
            return self._apply_enhanced_oil_painting(image)
    
    def _apply_enhanced_oil_painting(self, image: np.ndarray) -> Dict[str, Any]:
        """Enhanced oil painting effect"""
        try:
            params = self.artistic_filters['oil_painting']
            
            # Step 1: Advanced bilateral filtering for painterly smoothness
            smooth = cv2.bilateralFilter(
                image, 
                params['bilateral_params']['d'],
                params['bilateral_params']['sigmaColor'],
                params['bilateral_params']['sigmaSpace']
            )
            
            # Step 2: Multiple pass smoothing for oil texture
            for _ in range(2):
                smooth = cv2.bilateralFilter(smooth, 9, 40, 40)
            
            # Step 3: Enhanced color quantization with better clustering
            quantized = self._enhanced_color_quantization(
                smooth, params['quantization_levels']
            )
            
            # Step 4: Create brush stroke texture
            brush_texture = self._create_brush_texture(
                quantized, params['brush_size']
            )
            
            # Step 5: Enhance colors for oil painting richness
            lab = cv2.cvtColor(brush_texture, cv2.COLOR_BGR2LAB).astype(np.float32)
            lab[:,:,1] *= params['color_boost']  # Enhance 'a' channel
            lab[:,:,2] *= params['color_boost']  # Enhance 'b' channel
            lab = np.clip(lab, 0, 255).astype(np.uint8)
            oil_result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # Step 6: Subtle edge enhancement
            gray = cv2.cvtColor(oil_result, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edges = cv2.dilate(edges, np.ones((2,2), np.uint8))
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # Blend with subtle edges
            oil_result = cv2.addWeighted(oil_result, 0.95, 
                                       (255 - edges_colored) * oil_result // 255, 0.05, 0)
            
            # Step 7: Apply intensity
            oil_result = self._apply_intensity(image, oil_result)
            
            return {
                'styled_image': oil_result,
                'style_type': 'enhanced_oil_painting',
                'intensity': self.intensity,
                'processing_steps': ['multi_bilateral', 'enhanced_quantization', 'brush_texture', 'color_enhancement']
            }
            
        except Exception as e:
            print(f"Error creating empty result: {e}")
            return {'styled_image': image}
    
    def _apply_enhanced_watercolor(self, image: np.ndarray) -> Dict[str, Any]:
        """Enhanced watercolor effect"""
        try:
            params = self.artistic_filters['watercolor']
            
            # Step 1: Create color bleeding effect
            if params['color_bleeding']:
                bled_image = self._create_color_bleeding(image, params['blur_strength'])
            else:
                bled_image = cv2.GaussianBlur(image, (params['blur_strength'], params['blur_strength']), 0)
            
            # Step 2: Advanced color quantization with watercolor palette
            quantized = self._watercolor_quantization(
                bled_image, params['quantization_levels']
            )
            
            # Step 3: Create transparency zones
            transparency_mask = self._create_transparency_zones(
                quantized, params['transparency_zones']
            )
            
            # Step 4: Apply watercolor paper texture
            paper_texture = self._create_enhanced_paper_texture(
                quantized.shape[:2], params['paper_texture_strength']
            )
            
            # Step 5: Reduce saturation for watercolor effect
            hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[:,:,1] *= params['saturation_factor']
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            watercolor_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            # Step 6: Apply transparency and paper texture
            watercolor_result = cv2.addWeighted(watercolor_result, 0.7, paper_texture, 0.3, 0)
            
            # Apply transparency zones
            alpha = transparency_mask.astype(np.float32) / 255.0
            watercolor_result = watercolor_result.astype(np.float32)
            for i in range(3):
                watercolor_result[:,:,i] *= alpha
            watercolor_result = watercolor_result.astype(np.uint8)
            
            # Step 7: Apply intensity
            watercolor_result = self._apply_intensity(image, watercolor_result)
            
            return {
                'styled_image': watercolor_result,
                'style_type': 'enhanced_watercolor',
                'intensity': self.intensity,
                'processing_steps': ['color_bleeding', 'watercolor_quantization', 'transparency_zones', 'paper_texture']
            }
            
        except Exception as e:
            print(f"Enhanced watercolor error: {e}")
            return self._create_empty_result(image)
    
    def _apply_enhanced_pencil_sketch(self, image: np.ndarray) -> Dict[str, Any]:
        """Enhanced pencil sketch effect"""
        try:
            params = self.artistic_filters['pencil_sketch']
            
            # Step 1: Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Step 2: Create detailed sketch lines
            sketch = self._create_detailed_sketch(gray, params['line_detail'])
            
            # Step 3: Enhance contrast for better line definition
            sketch = cv2.convertScaleAbs(sketch, alpha=params['contrast_boost'], beta=0)
            
            # Step 4: Add paper grain texture
            if params['paper_grain']:
                paper_grain = self._create_paper_grain(sketch.shape)
                sketch = cv2.addWeighted(sketch, 0.8, paper_grain, 0.2, 0)
            
            # Step 5: Apply sketch density variation
            density_mask = self._create_sketch_density(sketch, params['sketch_density'])
            sketch = cv2.bitwise_and(sketch, density_mask)
            
            # Step 6: Convert back to color with slight tinting
            sketch_colored = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
            
            # Add subtle color tint from original
            tinted_sketch = cv2.addWeighted(sketch_colored, 0.85, image, 0.15, 0)
            
            # Step 7: Apply intensity
            final_result = self._apply_intensity(image, tinted_sketch)
            
            return {
                'styled_image': final_result,
                'style_type': 'enhanced_pencil_sketch',
                'intensity': self.intensity,
                'processing_steps': ['detailed_lines', 'contrast_enhance', 'paper_grain', 'density_variation']
            }
            
        except Exception as e:
            print(f"Enhanced pencil sketch error: {e}")
            return self._create_empty_result(image)
    
    def _apply_enhanced_cartoon(self, image: np.ndarray) -> Dict[str, Any]:
        """Enhanced cartoon effect"""
        try:
            params = self.artistic_filters['cartoon']
            
            # Step 1: Strong bilateral filtering for flat cartoon areas
            smooth = cv2.bilateralFilter(
                image,
                params['bilateral_params']['d'],
                params['bilateral_params']['sigmaColor'], 
                params['bilateral_params']['sigmaSpace']
            )
            
            # Step 2: Multiple smoothing passes
            for _ in range(3):
                smooth = cv2.bilateralFilter(smooth, 7, 30, 30)
            
            # Step 3: Color quantization for cartoon palette
            quantized = self._enhanced_color_quantization(
                smooth, params['quantization_levels']
            )
            
            # Step 4: Create thick cartoon edges
            edges = self._create_cartoon_edges(image, params['edge_thickness'])
            
            # Step 5: Boost saturation and brightness
            hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[:,:,1] *= params['saturation_boost']  # Saturation
            hsv[:,:,2] *= params['brightness_boost']  # Brightness
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            cartoon_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            # Step 6: Apply thick edges
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            cartoon_result = cv2.bitwise_and(cartoon_result, 255 - edges_colored)
            cartoon_result = cv2.addWeighted(cartoon_result, 0.9, edges_colored, 0.1, 0)
            
            # Step 7: Apply intensity
            cartoon_result = self._apply_intensity(image, cartoon_result)
            
            return {
                'styled_image': cartoon_result,
                'style_type': 'enhanced_cartoon',
                'intensity': self.intensity,
                'processing_steps': ['multi_bilateral', 'quantization', 'thick_edges', 'color_boost']
            }
            
        except Exception as e:
            print(f"Enhanced cartoon error: {e}")
            return self._create_empty_result(image)
    
    def _apply_impressionist(self, image: np.ndarray) -> Dict[str, Any]:
        """Apply impressionist painting effect"""
        try:
            params = self.artistic_filters['impressionist']
            
            # Step 1: Create brush strokes
            if params['brush_strokes']:
                brush_strokes = self._create_brush_strokes(
                    image, 
                    params['stroke_length'],
                    params['stroke_thickness']
                )
            else:
                brush_strokes = image
            
            # Step 2: Add color variation
            color_varied = self._add_color_variation(
                brush_strokes, params['color_variation']
            )
            
            # Step 3: Apply texture
            textured = self._apply_impressionist_texture(
                color_varied, params['texture_strength']
            )
            
            # Step 4: Apply intensity
            final_result = self._apply_intensity(image, textured)
            
            return {
                'styled_image': final_result,
                'style_type': 'impressionist',
                'intensity': self.intensity,
                'processing_steps': ['brush_strokes', 'color_variation', 'texture_application']
            }
            
        except Exception as e:
            print(f"Impressionist style error: {e}")
            return self._create_empty_result(image)
    
    def _apply_abstract(self, image: np.ndarray) -> Dict[str, Any]:
        """Apply abstract art effect"""
        try:
            params = self.artistic_filters['abstract']
            
            # Step 1: Geometric shape simplification
            if params['geometric_shapes']:
                geometric = self._create_geometric_shapes(image)
            else:
                geometric = image
            
            # Step 2: Extreme color reduction
            color_reduced = self._extreme_color_reduction(
                geometric, params['color_reduction']
            )
            
            # Step 3: Edge distortion
            if params['edge_distortion'] > 0:
                distorted = self._apply_edge_distortion(
                    color_reduced, params['edge_distortion']
                )
            else:
                distorted = color_reduced
            
            # Step 4: Apply intensity
            final_result = self._apply_intensity(image, distorted)
            
            return {
                'styled_image': final_result,
                'style_type': 'abstract',
                'intensity': self.intensity,
                'processing_steps': ['geometric_shapes', 'color_reduction', 'edge_distortion']
            }
            
        except Exception as e:
            print(f"Abstract style error: {e}")
            return self._create_empty_result(image)
    
    def _enhanced_color_quantization(self, image: np.ndarray, levels: int) -> np.ndarray:
        """Enhanced color quantization with better clustering"""
        try:
            data = image.reshape((-1, 3))
            data = np.float32(data)
            
            # Use better criteria for k-means
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.1)
            
            # Multiple attempts for better clustering
            best_compactness = float('inf')
            best_result = None
            
            for attempt in range(3):
                _, labels, centers = cv2.kmeans(
                    data, levels, None, criteria, 10, cv2.KMEANS_PP_CENTERS
                )
                
                # Calculate compactness (lower is better)
                compactness = 0
                for i in range(levels):
                    cluster_points = data[labels.flatten() == i]
                    if len(cluster_points) > 0:
                        compactness += np.sum((cluster_points - centers[i])**2)
                
                if compactness < best_compactness:
                    best_compactness = compactness
                    best_result = (labels, centers)
            
            if best_result is not None:
                labels, centers = best_result
                centers = np.uint8(centers)
                quantized_data = centers[labels.flatten()]
                quantized_image = quantized_data.reshape(image.shape)
                return quantized_image
            else:
                return image
                
        except Exception as e:
            print(f"Enhanced quantization error: {e}")
            return image
    
    def _create_brush_texture(self, image: np.ndarray, brush_size: int) -> np.ndarray:
        """Create brush stroke texture effect"""
        try:
            # Create brush kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (brush_size, brush_size))
            
            # Apply morphological operations to simulate brush strokes
            opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
            
            # Blend with original for texture
            textured = cv2.addWeighted(image, 0.7, closed, 0.3, 0)
            
            return textured
            
        except Exception as e:
            print(f"Brush texture error: {e}")
            return image
    
    def _create_color_bleeding(self, image: np.ndarray, strength: int) -> np.ndarray:
        """Create watercolor bleeding effect"""
        try:
            # Multiple blur passes with different kernels
            bleeding = image.copy()
            
            for i in range(3):
                kernel_size = strength + i * 5
                if kernel_size % 2 == 0:
                    kernel_size += 1
                
                bleeding = cv2.GaussianBlur(bleeding, (kernel_size, kernel_size), 0)
                bleeding = cv2.addWeighted(image, 0.3, bleeding, 0.7, 0)
            
            return bleeding
            
        except Exception as e:
            print(f"Color bleeding error: {e}")
            return image
    
    def _watercolor_quantization(self, image: np.ndarray, levels: int) -> np.ndarray:
        """Specialized quantization for watercolor effect"""
        try:
            # Convert to LAB for better color separation
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            
            # Quantize each channel separately
            quantized_lab = lab.copy()
            
            for channel in range(3):
                channel_data = lab[:, :, channel].flatten()
                
                # Create quantization levels
                min_val, max_val = channel_data.min(), channel_data.max()
                step = (max_val - min_val) / levels
                
                # Quantize
                quantized_channel = np.round((channel_data - min_val) / step) * step + min_val
                quantized_lab[:, :, channel] = quantized_channel.reshape(lab.shape[:2])
            
            # Convert back to BGR
            quantized = cv2.cvtColor(quantized_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
            
            return quantized
            
        except Exception as e:
            print(f"Watercolor quantization error: {e}")
            return self._enhanced_color_quantization(image, levels)
    
    def _create_transparency_zones(self, image: np.ndarray, zones: int) -> np.ndarray:
        """Create transparency zones for watercolor effect"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Create multiple transparency levels
            transparency_map = np.ones_like(gray) * 255
            
            for i in range(zones):
                # Create random transparency regions
                threshold = 255 // (zones + 1) * (i + 1)
                mask = gray < threshold
                
                # Apply transparency with smooth transitions
                transparency = 255 - (i + 1) * (255 // (zones + 1))
                transparency_map[mask] = transparency
            
            # Smooth transitions
            transparency_map = cv2.GaussianBlur(transparency_map, (15, 15), 0)
            
            return transparency_map
            
        except Exception as e:
            print(f"Transparency zones error: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def _create_enhanced_paper_texture(self, shape: Tuple[int, int], strength: float) -> np.ndarray:
        """Create enhanced paper texture"""
        try:
            h, w = shape
            
            # Generate multiple noise layers
            noise1 = np.random.randint(0, 50, (h, w), dtype=np.uint8)
            noise2 = np.random.randint(0, 30, (h//2, w//2), dtype=np.uint8)
            noise2 = cv2.resize(noise2, (w, h))
            
            # Combine noises
            combined_noise = cv2.addWeighted(noise1, 0.6, noise2, 0.4, 0)
            
            # Apply Gaussian blur for paper fiber effect
            paper = cv2.GaussianBlur(combined_noise, (3, 3), 0)
            
            # Create paper color (warm tone)
            paper_colored = cv2.cvtColor(paper, cv2.COLOR_GRAY2BGR)
            paper_colored[:, :, 0] = np.clip(paper_colored[:, :, 0] + 15, 0, 255)  # Blue
            paper_colored[:, :, 1] = np.clip(paper_colored[:, :, 1] + 20, 0, 255)  # Green
            paper_colored[:, :, 2] = np.clip(paper_colored[:, :, 2] + 25, 0, 255)  # Red
            
            # Apply strength
            base_color = np.ones((h, w, 3), dtype=np.uint8) * 240
            paper_textured = cv2.addWeighted(base_color, 1.0 - strength, paper_colored, strength, 0)
            
            return paper_textured
            
        except Exception as e:
            print(f"Enhanced paper texture error: {e}")
            return np.ones((shape[0], shape[1], 3), dtype=np.uint8) * 240
    
    def _create_detailed_sketch(self, gray: np.ndarray, detail_level: float) -> np.ndarray:
        """Create detailed pencil sketch lines"""
        try:
            # Multiple edge detection approaches
            edges1 = cv2.Canny(gray, 50, 150)
            edges2 = cv2.Canny(gray, 30, 100)
            
            # Sobel edges for different orientations
            sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
            sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
            
            # Combine all edge information
            combined_edges = cv2.addWeighted(edges1, 0.4, edges2, 0.3, 0)
            combined_edges = cv2.addWeighted(combined_edges, 0.7, sobel_combined, 0.3, 0)
            
            # Apply detail level
            enhanced = cv2.convertScaleAbs(combined_edges, alpha=detail_level, beta=0)
            
            # Invert for pencil effect (dark lines on light paper)
            sketch = 255 - enhanced
            
            return sketch
            
        except Exception as e:
            print(f"Detailed sketch error: {e}")
            return 255 - cv2.Canny(gray, 50, 150)
    
    def _create_paper_grain(self, shape: Tuple[int, int]) -> np.ndarray:
        """Create paper grain texture"""
        try:
            h, w = shape
            
            # Fine grain noise
            grain = np.random.randint(0, 20, (h, w), dtype=np.uint8)
            
            # Apply directional blur for paper fiber effect
            grain_blurred = cv2.GaussianBlur(grain, (1, 3), 0)  # Slight vertical blur
            
            # Enhance contrast
            grain_enhanced = cv2.convertScaleAbs(grain_blurred, alpha=2.0, beta=240)
            
            return grain_enhanced
            
        except Exception as e:
            print(f"Paper grain error: {e}")
            return np.ones(shape, dtype=np.uint8) * 245
    
    def _create_sketch_density(self, sketch: np.ndarray, density: float) -> np.ndarray:
        """Create varying sketch density"""
        try:
            # Create density variation mask
            h, w = sketch.shape
            
            # Generate smooth density map
            density_map = np.random.rand(h//10, w//10)
            density_map = cv2.resize(density_map, (w, h))
            density_map = cv2.GaussianBlur(density_map, (51, 51), 0)
            
            # Normalize and apply density factor
            density_map = (density_map * density + (1 - density)) * 255
            density_mask = density_map.astype(np.uint8)
            
            return density_mask
            
        except Exception as e:
            print(f"Sketch density error: {e}")
            return np.ones(sketch.shape, dtype=np.uint8) * 255
    
    def _create_cartoon_edges(self, image: np.ndarray, thickness: int) -> np.ndarray:
        """Create thick cartoon-style edges"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Multiple edge detection for completeness
            edges1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            edges2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 7)
            
            # Combine edges
            combined_edges = cv2.bitwise_or(255 - edges1, 255 - edges2)
            
            # Thicken edges
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness, thickness))
            thick_edges = cv2.morphologyEx(combined_edges, cv2.MORPH_DILATE, kernel)
            
            return thick_edges
            
        except Exception as e:
            print(f"Cartoon edges error: {e}")
            return cv2.Canny(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 50, 150)
    
    def _create_brush_strokes(self, image: np.ndarray, length: int, thickness: int) -> np.ndarray:
        """Create impressionist brush strokes"""
        try:
            # Create directional kernels for brush strokes
            kernels = [
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (length, thickness)),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness, length)),
                np.ones((thickness, length), np.uint8),
                np.ones((length, thickness), np.uint8)
            ]
            
            results = []
            for kernel in kernels:
                # Apply morphological opening
                stroke = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
                results.append(stroke)
            
            # Combine brush strokes
            brush_strokes = results[0]
            for result in results[1:]:
                brush_strokes = cv2.addWeighted(brush_strokes, 0.5, result, 0.5, 0)
            
            return brush_strokes
            
        except Exception as e:
            print(f"Brush strokes error: {e}")
            return image
    
    def _add_color_variation(self, image: np.ndarray, variation: float) -> np.ndarray:
        """Add color variation for impressionist effect"""
        try:
            # Convert to HSV for easier manipulation
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
            
            # Add random hue variation
            h, w = hsv.shape[:2]
            hue_noise = (np.random.rand(h, w) - 0.5) * variation * 180
            hsv[:, :, 0] = np.clip(hsv[:, :, 0] + hue_noise, 0, 179)
            
            # Add saturation variation
            sat_noise = (np.random.rand(h, w) - 0.5) * variation * 100
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] + sat_noise, 0, 255)
            
            # Convert back to BGR
            varied = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            
            return varied
            
        except Exception as e:
            print(f"Color variation error: {e}")
            return image
    
    def _apply_impressionist_texture(self, image: np.ndarray, strength: float) -> np.ndarray:
        """Apply impressionist painting texture"""
        try:
            # Create canvas texture
            h, w = image.shape[:2]
            texture = np.random.randint(0, 30, (h, w), dtype=np.uint8)
            texture = cv2.GaussianBlur(texture, (3, 3), 0)
            texture_colored = cv2.cvtColor(texture, cv2.COLOR_GRAY2BGR)
            
            # Apply texture
            textured = cv2.addWeighted(image, 1.0 - strength * 0.3, texture_colored, strength * 0.3, 0)
            
            return textured
            
        except Exception as e:
            print(f"Impressionist texture error: {e}")
            return image
    
    def _create_geometric_shapes(self, image: np.ndarray) -> np.ndarray:
        """Create geometric abstraction"""
        try:
            # Simplify image using superpixels approximation
            h, w = image.shape[:2]
            
            # Create simplified regions
            simplified = cv2.pyrDown(image)
            simplified = cv2.pyrUp(simplified)
            
            # Find contours for geometric shapes
            gray = cv2.cvtColor(simplified, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Create geometric version
            geometric = np.zeros_like(image)
            
            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    # Approximate to polygon
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    # Fill with average color from original region
                    mask = np.zeros(gray.shape, dtype=np.uint8)
                    cv2.fillPoly(mask, [approx], 255)
                    avg_color = cv2.mean(image, mask)[:3]
                    
                    cv2.fillPoly(geometric, [approx], avg_color)
            
            return geometric
            
        except Exception as e:
            print(f"Geometric shapes error: {e}")
            return image
    
    def _extreme_color_reduction(self, image: np.ndarray, levels: int) -> np.ndarray:
        """Extreme color reduction for abstract effect"""
        try:
            # Use K-means with very few clusters
            data = image.reshape((-1, 3))
            data = np.float32(data)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, levels, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Use posterization effect
            centers = np.uint8(centers)
            reduced_data = centers[labels.flatten()]
            reduced_image = reduced_data.reshape(image.shape)
            
            return reduced_image
            
        except Exception as e:
            print(f"Color reduction error: {e}")
            return image
    
    def _apply_edge_distortion(self, image: np.ndarray, distortion: float) -> np.ndarray:
        """Apply edge distortion for abstract effect"""
        try:
            h, w = image.shape[:2]
            
            # Create distortion maps
            map_x = np.zeros((h, w), dtype=np.float32)
            map_y = np.zeros((h, w), dtype=np.float32)
            
            for y in range(h):
                for x in range(w):
                    # Sinusoidal distortion
                    offset_x = distortion * 10 * np.sin(2 * np.pi * y / 30)
                    offset_y = distortion * 10 * np.sin(2 * np.pi * x / 30)
                    
                    map_x[y, x] = x + offset_x
                    map_y[y, x] = y + offset_y
            
            # Apply distortion
            distorted = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)
            
            return distorted
            
        except Exception as e:
            print(f"Edge distortion error: {e}")
            return image
    
    def _apply_intensity(self, original: np.ndarray, styled: np.ndarray) -> np.ndarray:
        """Apply intensity blending between original and styled image"""
        try:
            if self.intensity <= 0.0:
                return original
            elif self.intensity >= 1.0:
                return styled
            else:
                # Blend based on intensity
                return cv2.addWeighted(original, 1.0 - self.intensity, styled, self.intensity, 0)
        except:
            return styled
    
    def _create_empty_result(self, image: np.ndarray) -> Dict[str, Any]:
        """Create empty result for error cases"""
        return {
            'styled_image': image.copy(),
            'style_type': self.style_type,
            'intensity': self.intensity,
            'processing_steps': ['error']
        }
    
    def draw(self, image: np.ndarray, style_result: Dict[str, Any] = None) -> np.ndarray:
        """Draws the styled image, typically for direct display
        
        Args:
            image: The original input image (often ignored, but kept for API consistency)
            style_result: The result from the run() method
            
        Returns:
            The styled image from the result, or the original if styling failed.
        """
        if style_result and 'styled_image' in style_result:
            return style_result['styled_image']
        return image
    
    def apply_multiple_styles(self, image: np.ndarray, styles: List[str]) -> Dict[str, np.ndarray]:
        """Apply multiple styles to the same image
        
        Args:
            image: Input image
            styles: List of style names to apply
            
        Returns:
            Dictionary mapping style names to styled images
        """
        results = {}
        original_style = self.style_type
        
        for style in styles:
            try:
                self.style_type = style
                style_result = self.run(image)
                results[style] = style_result['styled_image']
            except Exception as e:
                print(f"Error applying style {style}: {e}")
                results[style] = image.copy()
        
        # Restore original style
        self.style_type = original_style
        
        return results
    
    def create_style_grid(self, image: np.ndarray, styles: List[str] = None) -> np.ndarray:
        """Create a grid showing multiple style effects
        
        Args:
            image: Input image
            styles: List of styles to show (default: all available)
            
        Returns:
            Grid image showing all styles
        """
        if styles is None:
            styles = ['oil_painting', 'watercolor', 'pencil_sketch', 'cartoon']
        
        styled_images = self.apply_multiple_styles(image, styles)
        
        try:
            # Calculate grid dimensions
            n_styles = len(styles)
            cols = 2
            rows = (n_styles + 1) // cols  # +1 for original
            
            h, w = image.shape[:2]
            grid_h = h * rows
            grid_w = w * cols
            
            # Create grid image
            grid = np.zeros((grid_h, grid_w, 3), dtype=np.uint8)
            
            # Add original image
            grid[:h, :w] = image
            cv2.putText(grid, "Original", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Add styled images
            for i, style in enumerate(styles):
                row = (i + 1) // cols
                col = (i + 1) % cols
                
                y_start = row * h
                y_end = y_start + h
                x_start = col * w
                x_end = x_start + w
                
                if style in styled_images:
                    grid[y_start:y_end, x_start:x_end] = styled_images[style]
                    
                    # Add style name
                    style_name = style.replace('_', ' ').title()
                    cv2.putText(grid, style_name, (x_start + 10, y_start + 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return grid
            
        except Exception as e:
            print(f"Style grid creation error: {e}")
            return image.copy()
    
    def save_styled_image(self, style_result: Dict[str, Any], filename: str) -> bool:
        """Save styled image to file
        
        Args:
            style_result: Style transfer result
            filename: Output filename
            
        Returns:
            Success status
        """
        try:
            cv2.imwrite(filename, style_result['styled_image'])
            print(f"Styled image saved to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save styled image: {e}")
            return False 