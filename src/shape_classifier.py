import cv2
import numpy as np
from src.config import *
from src.utils import compute_angles, compute_edge_angles
from dataclasses import dataclass

@dataclass(frozen=True)
class Shapes:
    SQUARE = "square"
    RECTANGLE = "rectangle"
    TRAPEZOID = "trapezoid"
    HEXAGON = "hexagon"


class ShapeClassifier:
    @staticmethod
    def is_square(poly):
        x, y, w, h = cv2.boundingRect(poly)
        ratio = w / float(h)

        angles = compute_angles(poly)
        for angle in angles:
            if not (90 - RECTANGLE_ANGLE_TOLERANCE <= angle <= 90 + RECTANGLE_ANGLE_TOLERANCE):
                return False

        if not (1 - SQUARE_RATIO_TOLERANCE <= ratio <= 1 + SQUARE_RATIO_TOLERANCE):
            return False
        
        return True

    @staticmethod
    def is_rectangle(poly):
        angles = compute_angles(poly)
        for angle in angles:
            if not (90 - RECTANGLE_ANGLE_TOLERANCE <= angle <= 90 + RECTANGLE_ANGLE_TOLERANCE):
                return False
        
        return True

    @staticmethod
    def is_trapezoid(poly):
        angles = compute_edge_angles(poly)
        parallel_pairs = 0

        for i in range(len(angles)):
            for j in range(i + 1, len(angles)):

                angle_diff = abs(angles[i] - angles[j])
                angle_diff = min(angle_diff, 180 - angle_diff)
                
                if angle_diff < RECTANGLE_ANGLE_TOLERANCE:
                    parallel_pairs += 1

        return parallel_pairs == 1

    @staticmethod
    def classify_shape(cnt):
        peri = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        poly = cv2.approxPolyDP(cnt, POLY_EPSILON_RATIO * peri, True)
        v = len(poly)

        if v >= 6 and 30000 <= area < 60000:
            return Shapes.HEXAGON, poly

        if ShapeClassifier.is_rectangle(poly):
            if ShapeClassifier.is_square(poly):
                return Shapes.SQUARE, poly
            elif 30000 <= area < 60000:
                return Shapes.RECTANGLE, poly
        elif ShapeClassifier.is_trapezoid(poly) and area < 30000:
            return Shapes.TRAPEZOID, poly
        elif 30000 <= area < 60000:
            return Shapes.RECTANGLE, poly

        return None, None
