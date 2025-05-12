import webbrowser
import pyautogui
import time
import cv2
import csv
import pyperclip
from check_temp_on_screen import is_template_on_screen

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

def main():
    elements = []

    # Open your browser and go to the page
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    url = "https://www.shopee.vn/"
    webbrowser.get(chrome_path).open(url)
    time.sleep(1)
    
    # Check if the page is loaded
    if is_template_on_screen("loaded_element.png", threshold=0.75):
        print("The image has appeared on the screen..")
    else:
        print("No image after multiple checks.")
        return 

    # Start the process 
    print("processing element number 1...")

    # open the developer tools
    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.typewrite('home-category-list__category-grid')
    time.sleep(1)

    # Find hignlight element, copy it and save
    pyautogui.screenshot("screen.png")
    center_x, center_y = match_template("screen.png", "highlight_template.png")
    pyautogui.moveTo(center_x, center_y, duration=0.1)
    pyautogui.rightClick()
    time.sleep(0.5)

    pyautogui.screenshot("menu1.png")
    copy_x, copy_y = match_template("menu1.png", "copy_button_template.png")
    pyautogui.moveTo(copy_x, copy_y, duration=0.1)
    time.sleep(0.5)

    pyautogui.screenshot("menu2.png")
    copy_element_x, copy_element_y = match_template("menu2.png", "copy_element_template.png")
    pyautogui.moveTo(copy_element_x, copy_element_y, duration=0.1)
    pyautogui.click()
    time.sleep(0.5)
    
    copied_data = pyperclip.paste()
    elements.append([copied_data])
    print(f"Element copied 1")
    # End Find hignlight element, copy it and save

    # Find next elements 
    for i in range(1, 27):
        print(f"Processing element number {i+1}...")

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

        pyautogui.screenshot("menu1.png")
        copy_x, copy_y = match_template("menu1.png", "copy_button_template.png")
        pyautogui.moveTo(copy_x, copy_y, duration=0.1)
        time.sleep(0.5)

        pyautogui.screenshot("menu2.png")
        copy_element_x, copy_element_y = match_template("menu2.png", "copy_element_template.png")
        pyautogui.moveTo(copy_element_x, copy_element_y, duration=0.1)
        pyautogui.click()
        time.sleep(0.5)

        copied_data = pyperclip.paste()
        elements.append([copied_data])
        print(f"Element copied {i+1}")
    # End all process

    # Save to CSV
    with open("element_data_category.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Element"])
        writer.writerows(elements)
    print("All saved to element_data.csv")

if __name__ == "__main__":
    main()
