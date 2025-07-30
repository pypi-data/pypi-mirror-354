# Welcome to AIToolkit Base

**AIToolkit Base** is a comprehensive, high-performance Python toolkit designed to simplify computer vision tasks. It provides a unified, clean, and easy-to-use API for a wide range of functionalities, from face detection and pose estimation to advanced style transfer.

This toolkit is built on top of robust libraries like MediaPipe and OpenCV, but abstracts away the complexities, allowing you to focus on building applications rather than wrestling with boilerplate code. All core modules follow a consistent `run`/`draw` API design pattern, making it incredibly intuitive to get started and integrate into your projects.

## Key Features

- **Unified API**: A consistent `run` (for inference) and `draw` (for visualization) pattern across all modules.
- **Comprehensive Functionality**: Covers face detection, landmark extraction (face, pose, hands), object detection, image segmentation, OCR, depth estimation, and more.
- **Real-time & Static Processing**: Most modules seamlessly support both live webcam feeds and static images/videos.
- **Extensible**: Built with a clear base class structure, making it easy to add your own custom detectors or processors.
- **Ready for Production**: Clean code, proper dependency management, and ready to be packaged for PyPI.

## Quick Glimpse

Here's a quick example of how simple it is to perform face detection:

```python
import cv2
from aitoolkit_base import FaceDetector

# Initialize the detector
detector = FaceDetector()

# Read an image
image = cv2.imread("path/to/your/image.jpg")

# Run detection
faces = detector.run(image)

# Draw the results
vis_image = detector.draw(image, faces)

# Display the output
cv2.imshow("Face Detection", vis_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Getting Started

Ready to dive in? Head over to the **[Installation](installation.md)** guide to get set up, and then check out the **[Quick Start](quick_start.md)** section to run the included examples. 