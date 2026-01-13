MIN_AREA = 10000
MAX_OBJECTS = 8

POLY_EPSILON_RATIO = 0.04

MORPH_KERNEL_SIZE = (3, 3)
MORPH_OPEN_ITERATIONS = 0
MORPH_CLOSE_ITERATIONS = 4

SQUARE_RATIO_TOLERANCE = 0.1  # Tolerance for square detection (0 ~ 1)

RECTANGLE_ANGLE_TOLERANCE = 10  # degrees tolerance for rectangle angles

# Real-world dimensions of the image area (in mm)
IMAGE_WIDTH_MM = 240.0   # Physical width of the camera view in mm
IMAGE_HEIGHT_MM = 320.0  # Physical height of the camera view in mm

# Image resolution (in pixels) - will be set dynamically based on actual image
IMAGE_WIDTH_PX = None  # Will be set when image is loaded
IMAGE_HEIGHT_PX = None  # Will be set when image is loaded