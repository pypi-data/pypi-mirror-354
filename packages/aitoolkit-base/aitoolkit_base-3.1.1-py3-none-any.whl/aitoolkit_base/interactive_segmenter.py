#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Segmenter Module
Based on MediaPipe Interactive Segmenter
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Optional, Tuple, Dict, Any
from .base_detector import BaseDetector


class InteractiveSegmenter(BaseDetector):
    """Interactive Image Segmenter
    
    Click-based interactive segmentation using MediaPipe
    """
    
    def __init__(self, 
                 model_path: Optional[str] = None,
                 output_confidence_masks: bool = True,
                 output_category_mask: bool = False,
                 **kwargs):
        """Initialize interactive segmenter
        
        Args:
            model_path: Path to custom model file
            output_confidence_masks: Whether to output confidence masks
            output_category_mask: Whether to output category mask
        """
        super().__init__(**kwargs)
        self.model_path = model_path
        self.output_confidence_masks = output_confidence_masks
        self.output_category_mask = output_category_mask
        
        # Store click points
        self.click_points = []
        self.current_image = None
        self.current_mask = None
        
        # Initialize MediaPipe
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize interactive segmentation model"""
        try:
            # Check if MediaPipe tasks API is available
            if hasattr(mp, 'tasks') and hasattr(mp.tasks, 'vision'):
                self.mp_interactive_segmenter = mp.tasks.vision.interactive_segmenter
                self.mp_image = mp.Image
                
                # Create options
                base_options = mp.tasks.BaseOptions()
                if self.model_path:
                    base_options.model_asset_path = self.model_path
                
                options = self.mp_interactive_segmenter.InteractiveSegmenterOptions(
                    base_options=base_options,
                    output_confidence_masks=self.output_confidence_masks,
                    output_category_mask=self.output_category_mask
                )
                
                self.segmenter = self.mp_interactive_segmenter.InteractiveSegmenter.create_from_options(options)
                print("Interactive Segmenter initialized successfully")
            else:
                print("MediaPipe tasks API not available, using fallback implementation")
                self.segmenter = None
                
        except Exception as e:
            print(f"Interactive Segmenter initialization failed: {e}")
            self.segmenter = None
    
    def add_click_point(self, x: int, y: int, is_positive: bool = True):
        """Add click point for segmentation
        
        Args:
            x: X coordinate
            y: Y coordinate
            is_positive: Whether this is a positive sample point
        """
        self.click_points.append({
            'x': x,
            'y': y,
            'positive': is_positive
        })
        print(f"Added {'positive' if is_positive else 'negative'} point at ({x}, {y})")
    
    def clear_points(self):
        """Clear all click points"""
        self.click_points = []
        self.current_mask = None
        print("Cleared all click points")
    
    def _process_image(self, image: np.ndarray) -> List:
        """Process image for interactive segmentation
        
        Args:
            image: Input image
            
        Returns:
            Segmentation results
        """
        self.current_image = image.copy()
        
        if not self.click_points:
            return []
        
        if self.segmenter is None:
            # Fallback implementation using simple region growing
            return self._fallback_segmentation(image)
        
        try:
            # Convert to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = self.mp_image(image_format=self.mp_image.ImageFormat.SRGB, data=rgb_image)
            
            # Create region of interest from click points
            roi = self._create_roi_from_points()
            
            # Run interactive segmentation
            results = self.segmenter.segment(mp_image, roi)
            
            if results.confidence_masks:
                self.current_mask = results.confidence_masks[0].numpy_view()
                return [self.current_mask]
            
            return []
            
        except Exception as e:
            print(f"Interactive segmentation error: {e}")
            return self._fallback_segmentation(image)
    
    def _create_roi_from_points(self):
        """Create region of interest from click points"""
        if not self.click_points:
            return None
        
        # This is a simplified implementation
        # In practice, you would create proper ROI objects
        # based on MediaPipe's API requirements
        
        # For now, return a simple bounding box around all points
        x_coords = [p['x'] for p in self.click_points]
        y_coords = [p['y'] for p in self.click_points]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Expand the region
        margin = 50
        roi_data = {
            'x': max(0, min_x - margin),
            'y': max(0, min_y - margin),
            'width': max_x - min_x + 2 * margin,
            'height': max_y - min_y + 2 * margin
        }
        
        return roi_data
    
    def _fallback_segmentation(self, image: np.ndarray) -> List:
        """Fallback segmentation using simple methods"""
        if not self.click_points:
            return []
        
        try:
            # Simple region growing based on color similarity
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            
            for point in self.click_points:
                if point['positive']:
                    # Use flood fill for positive points
                    seed_point = (point['x'], point['y'])
                    cv2.floodFill(mask, None, seed_point, 255, 
                                 loDiff=(30, 30, 30), upDiff=(30, 30, 30))
            
            # Remove negative regions
            for point in self.click_points:
                if not point['positive']:
                    seed_point = (point['x'], point['y'])
                    cv2.floodFill(mask, None, seed_point, 0)
            
            # Normalize to [0, 1]
            normalized_mask = mask.astype(np.float32) / 255.0
            self.current_mask = normalized_mask
            
            return [normalized_mask]
            
        except Exception as e:
            print(f"Fallback segmentation error: {e}")
            return []
    
    def draw(self, image: np.ndarray, segments: List, 
             background_color: Tuple[int, int, int] = (0, 255, 0),
             threshold: float = 0.5) -> np.ndarray:
        """Draw interactive segmentation results
        
        Args:
            image: Original image
            segments: Segmentation results
            background_color: Background color (BGR format)
            threshold: Segmentation threshold
            
        Returns:
            Image with segmentation visualization
        """
        result_image = image.copy()
        
        # Draw click points
        for point in self.click_points:
            color = (0, 255, 0) if point['positive'] else (0, 0, 255)
            cv2.circle(result_image, (point['x'], point['y']), 8, color, -1)
            cv2.circle(result_image, (point['x'], point['y']), 10, (255, 255, 255), 2)
        
        # Draw segmentation mask if available
        if segments and len(segments) > 0:
            mask = segments[0]
            
            try:
                # Create binary mask
                binary_mask = (mask > threshold).astype(np.uint8)
                
                # Create colored overlay
                overlay = result_image.copy()
                overlay[binary_mask == 1] = background_color
                
                # Blend with original image
                result_image = cv2.addWeighted(result_image, 0.7, overlay, 0.3, 0)
                
                # Draw mask contours
                contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(result_image, contours, -1, (255, 255, 255), 2)
                
            except Exception as e:
                print(f"Error drawing segmentation: {e}")
        
        # Add instructions
        cv2.putText(result_image, "Left click: Add positive point", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(result_image, "Right click: Add negative point", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(result_image, "Press 'c' to clear points", (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return result_image
    
    def get_mask(self, threshold: float = 0.5) -> Optional[np.ndarray]:
        """Get binary segmentation mask
        
        Args:
            threshold: Binarization threshold
            
        Returns:
            Binary mask
        """
        if self.current_mask is None:
            return None
        
        binary_mask = (self.current_mask > threshold).astype(np.uint8) * 255
        return binary_mask
    
    def save_mask(self, filename: str, threshold: float = 0.5) -> bool:
        """Save segmentation mask to file
        
        Args:
            filename: Output filename
            threshold: Binarization threshold
            
        Returns:
            Success status
        """
        mask = self.get_mask(threshold)
        if mask is None:
            return False
        
        try:
            cv2.imwrite(filename, mask)
            print(f"Mask saved to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save mask: {e}")
            return False
    
    def run_interactive_demo(self, image: np.ndarray):
        """Run interactive segmentation demo
        
        Args:
            image: Input image for segmentation
        """
        print("Starting interactive segmentation demo...")
        print("Controls:")
        print("- Left click: Add positive point")
        print("- Right click: Add negative point") 
        print("- Press 'c': Clear all points")
        print("- Press 's': Save mask")
        print("- Press ESC: Exit")
        
        self.current_image = image.copy()
        window_name = "Interactive Segmentation"
        cv2.namedWindow(window_name)
        
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.add_click_point(x, y, True)
                self._update_display(window_name)
            elif event == cv2.EVENT_RBUTTONDOWN:
                self.add_click_point(x, y, False)
                self._update_display(window_name)
        
        cv2.setMouseCallback(window_name, mouse_callback)
        self._update_display(window_name)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                break
            elif key == ord('c'):
                self.clear_points()
                self._update_display(window_name)
            elif key == ord('s'):
                self.save_mask("segmentation_mask.png")
        
        cv2.destroyAllWindows()
    
    def _update_display(self, window_name: str):
        """Update display with current segmentation"""
        if self.current_image is None:
            return
        
        segments = self._process_image(self.current_image)
        result = self.draw(self.current_image, segments)
        cv2.imshow(window_name, result)
    
    def close(self):
        """Release resources"""
        if hasattr(self, 'segmenter') and self.segmenter:
            try:
                self.segmenter.close()
            except:
                pass
        super().close() 