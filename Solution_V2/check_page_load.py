import time
import cv2

# Check if a pattern exists in another pattern
def check_page_loaded(template, screenshot,threshold=0.8):
    template_img = cv2.imread(template)
    screenshot_img = cv2.imread(screenshot)

    if template_img is None or screenshot_img is None:
        raise Exception("Unable to read image.")
    
    result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return  True        
    return False