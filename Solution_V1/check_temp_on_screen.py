import cv2
import pyautogui
import time
import numpy as np

def is_template_on_screen(template_path, threshold=0.8, max_attempts=20, delay=1):
    """
    Check if the template appears on the screen.

    Args:
        template_path (str): Path to the template image.
        threshold (float): Match threshold (default: 0.8).
        max_attempts (int): Number of attempts (default: 10).
        delay (float): Time to wait between attempts (default: 1 second).

    Returns:
        bool: True if found, False if not.
    """
    template = cv2.imread(template_path)
    if template is None:
        raise Exception(f"Unable to read sample image: {template_path}")

    for attempt in range(1, max_attempts + 1):
        # Take full screen screenshot and convert from PIL Image to numpy array (RGB → BGR)
        screenshot = pyautogui.screenshot()
        screen_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Match sample image in screenshot
        result = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        print(f"[Time {attempt}] max_val = {max_val:.2f}")
        if max_val >= threshold:
            return True

        time.sleep(delay)

    return False
