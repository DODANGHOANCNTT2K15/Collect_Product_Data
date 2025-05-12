import cv2
import pyautogui
import time

# Comepare screenshot with template. Then find location to move mouse to
def match_template(screen_path, template_path, threshold=0.8):
    img = cv2.imread(screen_path)
    template = cv2.imread(template_path)
    if img is None or template is None:
        raise Exception("Unable to read image.")
    
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    attempts = 0
    while max_val < threshold and attempts < 3:
        print(f"Template image not found in image (time {attempts+1}). Press Enter...")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.screenshot(screen_path)
        img = cv2.imread(screen_path)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        attempts += 1

    if max_val < threshold:
        raise Exception(f"No matching template found after {attempts} time (max_val={max_val:.2f})")

    h, w = template.shape[:2]
    center_x, center_y = max_loc[0] + w // 2, max_loc[1] + h // 2
    return center_x, center_y