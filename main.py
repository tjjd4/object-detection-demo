# main.py
import cv2
import numpy as np
from src.object_detection import detect_objects
from src.coordinate_converter import CoordinateConverter

def main():
    img = cv2.imread("data/img5.jpg")
    
    # Create coordinate converter
    img_height, img_width = img.shape[:2]
    converter = CoordinateConverter(img_width, img_height)
    
    # Print calibration info
    calib_info = converter.get_calibration_info()
    print("Coordinate Converter Calibration Info:")
    print(f"Image size: {calib_info['image_width_px']} x {calib_info['image_height_px']} pixels")
    print(f"Real-world size: {calib_info['image_width_mm']:.1f} x {calib_info['image_height_mm']:.1f} mm")
    print(f"Resolution: {calib_info['mm_per_px_x']:.4f} mm/px (X), {calib_info['mm_per_px_y']:.4f} mm/px (Y)")
    
    objects, th_img = detect_objects(img, converter)

    result = img.copy()

    for idx, obj in enumerate(objects):
        cv2.drawContours(result, [obj["contour"]], -1, (0, 255, 0), 2)
        
        box = cv2.boxPoints(obj["min_area_rect"])
        box = np.intp(box)
        cv2.drawContours(result, [box], 0, (255, 0, 0), 2)
        

        x, y, w, h = obj["bbox"]
        shape_text = obj["shape"]
        angle_text = f"{obj['angle']:.1f}deg"
        
        cv2.putText(
            result,
            shape_text,
            (x, y - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )
        
        cv2.putText(
            result,
            angle_text,
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 255),
            2
        )
        
        # 標註物件編號
        cx, cy = obj["center"]
        cv2.putText(
            result,
            f"#{idx+1}",
            (cx - 15, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    for idx, o in enumerate(objects):
        print(f"\nObject #{idx+1}:")
        print(f"Shape: {o['shape']}")
        print(f"Angle: {o['angle']:.2f}°")
        print(f"Pixel Measurements:")
        print(f"  Center: ({o['center'][0]}, {o['center'][1]}) px")
        print(f"Real-World Measurements (mm):")
        print(f"  Center: ({o['center_mm'][0]:.2f}, {o['center_mm'][1]:.2f}) mm")

    cv2.imwrite("outputs/output_threshold.jpg", th_img)
    cv2.imwrite("outputs/output_result.jpg", result)



if __name__ == "__main__":
    main()
