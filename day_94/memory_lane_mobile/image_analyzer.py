from ultralytics import YOLO
from PIL import Image
import tempfile
import os

def detect_objects(image: Image.Image):
    """
    Detect objects in a PIL image using YOLOv8.
    Returns a list of detected object names.
    """
    # Save image to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        image.save(tmp.name)
        image_path = tmp.name
    
    # Load YOLOv8 model (coco pretrained)
    model = YOLO('yolov8n.pt')
    results = model(image_path)
    
    # Extract detected class names
    detected = set()
    for r in results:
        for c in r.boxes.cls:
            detected.add(model.names[int(c)])
    
    # Clean up temp file
    os.remove(image_path)
    return list(detected) 