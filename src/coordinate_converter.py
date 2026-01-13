from src.config import IMAGE_WIDTH_MM, IMAGE_HEIGHT_MM, IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX


class CoordinateConverter:

    def __init__(self, image_width_px, image_height_px):
        self.image_width_px = image_width_px
        self.image_height_px = image_height_px
        
        # Calculate pixels per mm ratios
        self.px_per_mm_x = image_width_px / IMAGE_WIDTH_MM
        self.px_per_mm_y = image_height_px / IMAGE_HEIGHT_MM
        
        # Calculate mm per pixel ratios
        self.mm_per_px_x = IMAGE_WIDTH_MM / image_width_px
        self.mm_per_px_y = IMAGE_HEIGHT_MM / image_height_px
        
    def pixel_to_mm(self, x_px, y_px):
        x_mm = x_px * self.mm_per_px_x
        y_mm = y_px * self.mm_per_px_y
        return (x_mm, y_mm)
    
    def mm_to_pixel(self, x_mm, y_mm):
        x_px = int(x_mm * self.px_per_mm_x)
        y_px = int(y_mm * self.px_per_mm_y)
        return (x_px, y_px)
    
    def distance_to_mm(self, distance_px, axis=''):
        if axis.lower() == 'x':
            return distance_px * self.mm_per_px_x
        elif axis.lower() == 'y':
            return distance_px * self.mm_per_px_y
    
    def area_to_mm2(self, area_px):
        return area_px * self.mm_per_px_x * self.mm_per_px_y
    
    def get_calibration_info(self):
        return {
            'image_width_px': self.image_width_px,
            'image_height_px': self.image_height_px,
            'image_width_mm': IMAGE_WIDTH_MM,
            'image_height_mm': IMAGE_HEIGHT_MM,
            'mm_per_px_x': self.mm_per_px_x,
            'mm_per_px_y': self.mm_per_px_y,
            'px_per_mm_x': self.px_per_mm_x,
            'px_per_mm_y': self.px_per_mm_y,
        }
