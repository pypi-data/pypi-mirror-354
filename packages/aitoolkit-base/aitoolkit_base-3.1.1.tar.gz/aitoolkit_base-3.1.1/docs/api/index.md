# API Reference Overview

Welcome to the API reference for `AIToolkit Base`. This section provides detailed documentation on the classes and methods available in the toolkit.

All core modules are designed with a consistent API. For most modules, you will interact with a primary class (e.g., `FaceDetector`, `PoseLandmarker`). These classes share a common structure:

1.  **`__init__(...)`**: The constructor to initialize the model, where you can configure parameters like model paths or confidence thresholds.
2.  **`run(image)`**: The core inference method. It takes an image (as a NumPy array) and returns a structured data object containing the results (e.g., bounding boxes, landmarks).
3.  **`draw(image, results)`**: A utility method that takes the original image and the results from `run()` to produce a visualized output.
4.  **`close()`**: Releases any resources held by the object, like models or webcam captures.

## Navigation

Use the navigation on the left to explore the detailed documentation for each module category:

-   **Detectors**: For tasks that find the location of objects (faces, general objects, text).
-   **Landmarkers**: For tasks that find keypoints on objects (face landmarks, pose landmarks, hand landmarks).
-   **Segmentation**: For creating pixel-level masks to separate foreground from background.
-   **Image Effects**: For artistic and analytical image processing like style transfer and depth estimation.
-   **Utilities**: For helper functions, such as visualization tools. 