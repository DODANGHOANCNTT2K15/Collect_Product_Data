import pandas as pd
import csv
import webbrowser
import pyautogui
import time
import csv
import pyperclip
import cv2

from check_temp_on_screen import is_template_on_screen

def match_template(screen_path, template_path, threshold=0.8):
    img = cv2.imread(screen_path)
    template = cv2.imread(template_path)
    if img is None or template is None:
        raise Exception("Unable to read image.")
    
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    attempts = 0
    while max_val < threshold and attempts < 3:
        print(f"Template not found in image (time {attempts+1}). Press Enter...")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.screenshot(screen_path)
        img = cv2.imread(screen_path)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        attempts += 1

    if max_val < threshold:
        print(f"Template not found after 3 tries. Move to next category.")
        return None  # Trả về None khi không tìm thấy sau 3 lần thử

    h, w = template.shape[:2]
    center_x, center_y = max_loc[0] + w // 2, max_loc[1] + h // 2
    return center_x, center_y

def main():
    # Danh sách lưu toàn bộ sản phẩm từ tất cả danh mục
    all_elements = []

    # Lặp qua từng danh mục
    for idx, url in enumerate(category_products):
        print(f"Access the catalog {idx+1}/{len(category_products)}")
        webbrowser.get(chrome_path).open(url)
        time.sleep(1)

        if is_template_on_screen("loaded_element2.png", threshold=0.75):
            print("The image has appeared on the screen..")
        else:
            print("No image after multiple checks.") 

        screen_width, screen_height = pyautogui.size()
        x = screen_width - 50          # Cách mép phải 50px
        y = screen_height // 2         # Giữa chiều cao

        pyautogui.moveTo(x, y, duration=0.2)  # Di chuyển chuột đến vị trí
        time.sleep(1)

        pyautogui.scroll(-5000)  # Mỗi lần khoảng 100px, nên -3 là ~300px
        time.sleep(0.2) 
        
        # Mở DevTools và vào chế độ chọn phần tử
        pyautogui.hotkey('ctrl', 'shift', 'c')
        time.sleep(2)

        # Mở thanh tìm kiếm phần tử
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.typewrite('div.container')  # Tìm kiếm phần tử chứa sản phẩm
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        # Lấy phần tử đầu tiên
        pyautogui.screenshot("screen.png")
        result = match_template("screen.png", "highlight_template_product_container.png")
        
        if result is None:  # Nếu không tìm thấy template, chuyển sang link khác
            print(f"No products found {idx+1}, move to next product.")
            continue  # Chuyển sang danh mục tiếp theo

        center_x, center_y = result
        pyautogui.moveTo(center_x, center_y, duration=0.1)
        pyautogui.rightClick()
        time.sleep(1)

        # Mở menu "Copy"
        pyautogui.screenshot("menu1.png")
        copy_x, copy_y = match_template("menu1.png", "copy_button_template.png")
        pyautogui.moveTo(copy_x, copy_y, duration=0.1)
        time.sleep(0.5)

        # Click "Copy element"
        pyautogui.screenshot("menu2.png")
        copy_element_x, copy_element_y = match_template("menu2.png", "copy_element_template.png")
        pyautogui.moveTo(copy_element_x, copy_element_y, duration=0.1)
        pyautogui.click()
        time.sleep(0.5)

        copied_data = pyperclip.paste()
        all_elements.append([url, copied_data])
        print(f"Product {idx+1}: Copied first product information")
        
        pyautogui.hotkey('ctrl', 'w')  
        time.sleep(1)

    # Ghi toàn bộ vào file CSV
    with open("full_info_detail_product.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Product URL", "Element"])
        writer.writerows(all_elements)

    print("All saved to full_info_detail_product.csv")

if __name__ == "__main__":
    category_products = []

    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

    with open('full_link_product.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            category_products.append(row[0]) 

    main()
