import numpy as np

from src.config import *

def compute_mm_per_pixel(distance_mm, focal_length_mm, sensor_width_mm, image_width_pixels):
    return (distance_mm * sensor_width_mm) / (focal_length_mm * image_width_pixels)

def compute_angles(poly):
    angles = []
    pts = poly.reshape(-1, 2)
    n = len(pts)
    
    for i in range(n):
        p1 = pts[(i - 1) % n]
        p2 = pts[i]
        p3 = pts[(i + 1) % n]
        
        v1 = p1 - p2
        v2 = p3 - p2
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.degrees(np.arccos(cos_angle))
        
        angles.append(angle)
    
    return angles

def compute_edge_angles(poly):
    angles = []
    pts = poly.reshape(-1, 2)
    n = len(pts)

    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        
        angle = angle % 180
        
        angles.append(angle)

    return angles