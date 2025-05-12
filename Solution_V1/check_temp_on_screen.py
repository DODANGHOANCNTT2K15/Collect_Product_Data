import cv2
import pyautogui
import time
import numpy as np

def is_template_on_screen(template_path, threshold=0.8, max_attempts=20, delay=1):
    """
    Kiểm tra xem template có xuất hiện trên màn hình hay không.

    Args:
        template_path (str): Đường dẫn đến ảnh mẫu.
        threshold (float): Ngưỡng độ khớp (default: 0.8).
        max_attempts (int): Số lần thử (default: 10).
        delay (float): Thời gian chờ giữa các lần (default: 1 giây).

    Returns:
        bool: True nếu tìm thấy, False nếu không.
    """
    template = cv2.imread(template_path)
    if template is None:
        raise Exception(f"Unable to read sample image: {template_path}")

    for attempt in range(1, max_attempts + 1):
        # Chụp ảnh toàn màn hình và chuyển từ PIL Image sang numpy array (RGB → BGR)
        screenshot = pyautogui.screenshot()
        screen_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # So khớp ảnh mẫu trong ảnh chụp màn hình
        result = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        print(f"[Time {attempt}] max_val = {max_val:.2f}")
        if max_val >= threshold:
            return True

        time.sleep(delay)

    return False
