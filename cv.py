import cv2
import io
import numpy as np
import subprocess

from . import inputs

class Clickable:
    def __init__(self, image_path, offset=(0,0), delay=0.5, roi=None):
        self.image_path = image_path
        self.offset = offset
        self.delay = delay
        self.roi = roi

    def set_roi(self, roi):
        self.roi = roi

    def click(self):
        screenshot = take_screenshot()
        x, y = find_image_coordinates(self.image_path, screenshot, self.roi)
        inputs.tap(x+self.offset[0], y+self.offset[1], self.delay)

    def find(self):
        screenshot = take_screenshot()
        x, y = find_image_coordinates(self.image_path, screenshot, self.roi)
        return x, y

def take_screenshot():
    result = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
    screenshot_bytes = io.BytesIO(result.stdout)
    screenshot_arr = np.asarray(bytearray(screenshot_bytes.read()), dtype=np.uint8)
    screenshot = cv2.imdecode(screenshot_arr, cv2.IMREAD_COLOR)
    return screenshot

def find_image_coordinates(image_path, screenshot, roi=None):
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    while True:
        _, _, _, max_loc = cv2.minMaxLoc(result)
        
        if roi:
            if max_loc[0] > roi[0] and max_loc[0] < roi[1] and max_loc[1] > roi[2] and max_loc[1] < roi[3]:
                return max_loc
        else: return max_loc
        
        result[max_loc[1], max_loc[0]] = -1
        if np.amax(result) < 0:
            break

def is_pixel_color(x, y, target_color):
    result = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
    image_stream = io.BytesIO(result.stdout)
    image_np = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    pixel_color = image[y, x]
    return np.array_equal(pixel_color, target_color)