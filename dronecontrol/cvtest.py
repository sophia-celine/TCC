import cv2
import numpy as np

img_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)  # Example array
cv2.imshow('Image', img_array)
cv2.waitKey(0)
cv2.destroyAllWindows()