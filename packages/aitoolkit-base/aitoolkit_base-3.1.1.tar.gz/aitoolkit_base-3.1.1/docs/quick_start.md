# Quick Start: Running the Examples

This guide will walk you through running the example scripts to see `AIToolkit Base` in action. All examples are located in the `examples/` directory.

Most scripts are designed to run in multiple modes:
1.  **Window Mode**: (`--input window`) Uses your live webcam and displays the output in a local OpenCV window. This is the default for real-time examples.
2.  **Web Mode**: (`--input web`) Uses `aitoolkit-cam` to display the live feed in a web browser. Ideal for Jupyter Notebooks.
3.  **Image Mode**: Processes a static image file by providing its path.

Press the 'q' key to close the display window when running in `window` mode. For `web` mode, stop the process in your terminal or Jupyter cell.

---

## General Usage

The basic command structure is:

```bash
python examples/<script_name>.py --input <source>
```

-   `<script_name>.py`: The example you want to run (e.g., `1_face_detection.py`).
-   `<source>`: Can be `window` (default), `web`, or a path to an image file.

---

## Example Commands

Here are the commands to run each example.

### 1. Face Detection
Detects human faces in an image or webcam stream.

```bash
# Run with local window (default)
python examples/1_face_detection.py --input window

# Run with web browser view
python examples/1_face_detection.py --input web

# Run on a specific image
python examples/1_face_detection.py --input examples/images/face_test.jpg
```

### 2. Face Landmarks
Detects detailed 478 landmarks on a face.

```bash
# Run with local window (default)
python examples/2_face_landmarks.py

# Run with web browser view
python examples/2_face_landmarks.py --input web
```

### 3. Pose Estimation
Estimates human body pose with 33 keypoints.

```bash
# Run with local window (default)
python examples/3_pose_estimation.py

# Run with web browser view
python examples/3_pose_estimation.py --input web
```

### 4. Hand Gesture Recognition
Tracks hand landmarks and recognizes common gestures.

```bash
# Run with local window (default)
python examples/4_hand_gestures.py

# Run with web browser view
python examples/4_hand_gestures.py --input web
```

### 5. Object Detection
Detects common objects using a pre-trained model.

```bash
# Run with local window (default)
python examples/5_object_detection.py

# Run with web browser view
python examples/5_object_detection.py --input web
```

### 6. Image Segmentation
Creates a segmentation mask for the foreground (e.g., a person).

```bash
# Run with local window (default)
python examples/6_image_segmentation.py

# Run with web browser view
python examples/6_image_segmentation.py --input web
```

### 7. OCR & License Plate Recognition
This example only supports image files.

```bash
# Run general OCR on the default image
python examples/7_ocr.py --task ocr

# Run license plate detection on a specific image
python examples/7_ocr.py --task lp --input examples/images/license_plate_test.jpg
```

### 8. Depth Estimation
This example only supports image files.

```bash
# Run on the default image
python examples/8_depth_estimation.py

# Try a different method
python examples/8_depth_estimation.py --method dpt
```

### 9. Style Transfer
This example only supports image files.

```bash
# Apply the default 'impressionist' style
python examples/9_style_transfer.py

# Try the 'cartoon' style on a specific image
python examples/9_style_transfer.py --style cartoon --input examples/images/style_test.jpg
``` 