import cv2
import pyautogui
import time
import numpy as np

def find_image_location(template_path, threshold=0.8, max_attempts=20, delay=1):
    template = cv2.imread(template_path)
    if template is None:
        raise Exception(f"Unable to read sample image: {template_path}")

    for attempt in range(1, max_attempts + 1):
        screenshot = pyautogui.screenshot()
        screen_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        print(f"[Time {attempt}] max_val = {max_val:.2f}")
        if max_val >= threshold:
            return True

        time.sleep(delay)

    return False
