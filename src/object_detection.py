# object_detection.py
import cv2
from src.config import *
from src.shape_classifier import ShapeClassifier
from src.coordinate_converter import CoordinateConverter

def get_rotation_angle(contour):
    rect = cv2.minAreaRect(contour)
    angle = rect[2]  # angle range: -90-0
    
    width, height = rect[1]
    if width < height:
        normalized_angle = angle + 90
    else:
        normalized_angle = angle + 180 if angle < 0 else angle
    
    return normalized_angle, rect  # angle range: 0-180

def detect_objects(img, converter=None):
    """
    Detect objects in the image.
    
    Args:
        img: Input image
        converter: Optional CoordinateConverter for pixel-to-mm conversion
        
    Returns:
        tuple: (objects list, threshold image)
    """
    # Create converter if not provided
    if converter is None:
        img_height, img_width = img.shape[:2]
        converter = CoordinateConverter(img_width, img_height)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, th = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    if MORPH_OPEN_ITERATIONS > 0 or MORPH_CLOSE_ITERATIONS > 0 and MORPH_KERNEL_SIZE is not None:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_KERNEL_SIZE)
        
        if MORPH_OPEN_ITERATIONS > 0:
            th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=MORPH_OPEN_ITERATIONS)
        
        if MORPH_CLOSE_ITERATIONS > 0:
            th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=MORPH_CLOSE_ITERATIONS)

    contours, _ = cv2.findContours(
        th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    objects = []
    print(f"Total contours found: {len(contours)}")
    for i, cnt in enumerate(contours):
        hull = cv2.convexHull(cnt)
        area = cv2.contourArea(hull)
        print(f"Contour {i}: area = {area}")
        if area < MIN_AREA:
            continue

        shape, poly = ShapeClassifier.classify_shape(hull)
        if shape is None:
            continue

        x, y, w, h = cv2.boundingRect(poly)
        cx, cy = x + w // 2, y + h // 2
        
        angle, min_area_rect = get_rotation_angle(poly)
        
        # Convert to real-world coordinates
        center_mm = converter.pixel_to_mm(cx, cy)
        width_mm = converter.distance_to_mm(w, 'x')
        height_mm = converter.distance_to_mm(h, 'y')
        area_mm2 = converter.area_to_mm2(area)

        objects.append({
            "shape": shape,
            "area": area,  # in pixels
            "area_mm2": area_mm2,  # in mm2
            "bbox": (x, y, w, h),  # in pixels
            "bbox_mm": (width_mm, height_mm),  # in mm
            "center": (cx, cy),  # in pixels
            "center_mm": center_mm,  # in mm
            "contour": poly,
            "angle": angle,  # from minAreaRect and normalized to 0-180
            "min_area_rect": min_area_rect,  # ((cx, cy), (w, h), angle)
        })

    objects = sorted(objects, key=lambda o: o["area"], reverse=True)
    return objects[:MAX_OBJECTS], th