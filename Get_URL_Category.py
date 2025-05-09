import webbrowser
import pyautogui
import time
import cv2
import csv
import pyperclip
import numpy as np

def match_template(screen_path, template_path, threshold=0.8):
    img = cv2.imread(screen_path)
    template = cv2.imread(template_path)
    if img is None or template is None:
        raise Exception("Không thể đọc ảnh.")
    
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    attempts = 0
    while max_val < threshold and attempts < 3:
        print(f"Không tìm thấy template trong ảnh (lần {attempts+1}). Nhấn Enter...")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.screenshot(screen_path)
        img = cv2.imread(screen_path)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        attempts += 1

    if max_val < threshold:
        raise Exception(f"Không tìm thấy template phù hợp sau {attempts} lần (max_val={max_val:.2f})")

    h, w = template.shape[:2]
    center_x, center_y = max_loc[0] + w // 2, max_loc[1] + h // 2
    return center_x, center_y

def main():
    # Mở trình duyệt và truy cập trang
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    url = "https://www.shopee.vn/"
    webbrowser.get(chrome_path).open(url)
    time.sleep(4)

    # Tạo danh sách lưu các element
    elements = []

    # Mở DevTools và vào chế độ chọn phần tử
    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(2)

    # Mở thanh tìm kiếm phần tử
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.typewrite('home-category-list__category-grid')
    time.sleep(0.5)

    pyautogui.screenshot("screen.png")
    center_x, center_y = match_template("screen.png", "highlight_template.png")
    pyautogui.moveTo(center_x, center_y, duration=0.1)
    pyautogui.rightClick()
    time.sleep(1)

    # Bước 2: Mở menu "Copy"
    pyautogui.screenshot("menu1.png")
    copy_x, copy_y = match_template("menu1.png", "copy_button_template.png")
    pyautogui.moveTo(copy_x, copy_y, duration=0.1)
    time.sleep(1)

    # Bước 3: Click "Copy element"
    pyautogui.screenshot("menu2.png")
    copy_element_x, copy_element_y = match_template("menu2.png", "copy_element_template.png")
    pyautogui.moveTo(copy_element_x, copy_element_y, duration=0.1)
    pyautogui.click()
    time.sleep(0.5)

    # Bước 4: Lấy dữ liệu và lưu
    copied_data = pyperclip.paste()
    elements.append([copied_data])
    print(f"✅ Đã sao chép phần tử 1")

    for i in range(1, 27):
        print(f"🌀 Đang xử lý phần tử thứ {i+1}...")

        # Bước 1: Highlight phần tử
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        for i in range(i+1):
            pyautogui.press('enter')  # chọn phần tử tiếp theo
            time.sleep(0.5)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "highlight_template.png")
        pyautogui.moveTo(center_x, center_y, duration=0.1)
        pyautogui.rightClick()
        time.sleep(0.5)

        # Bước 2: Mở menu "Copy"
        pyautogui.screenshot("menu1.png")
        copy_x, copy_y = match_template("menu1.png", "copy_button_template.png")
        pyautogui.moveTo(copy_x, copy_y, duration=0.1)
        time.sleep(0.5)

        # Bước 3: Click "Copy element"
        pyautogui.screenshot("menu2.png")
        copy_element_x, copy_element_y = match_template("menu2.png", "copy_element_template.png")
        pyautogui.moveTo(copy_element_x, copy_element_y, duration=0.1)
        pyautogui.click()
        time.sleep(0.5)

        # Bước 4: Lấy dữ liệu và lưu
        copied_data = pyperclip.paste()
        elements.append([copied_data])
        print(f"✅ Đã sao chép phần tử {i+1}")

    # Ghi toàn bộ vào file CSV
    with open("element_data_category.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Element"])
        writer.writerows(elements)

    print("🎉 Đã lưu toàn bộ vào element_data.csv")

if __name__ == "__main__":
    main()
