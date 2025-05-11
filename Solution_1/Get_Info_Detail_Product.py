import pandas as pd
import csv
import webbrowser
import pyautogui
import time
import csv
import pyperclip
import cv2

from check_temp_on_screen import is_template_on_screen
from Get_URL_Product import match_template

def main():
    all_elements = []

    for idx, url in enumerate(category_products):
        print(f"Access the catalog {idx+1}/{len(category_products)}")
        webbrowser.get(chrome_path).open(url)
        time.sleep(1)

        if is_template_on_screen("loaded_element2.png", threshold=0.75):
            print("The image has appeared on the screen..")
        elif is_template_on_screen("loaded_element1.png", threshold=0.75):
            print("The image has appeared on the screen..")
        else:
            print("No image after multiple checks.") 
            continue

        screen_width, screen_height = pyautogui.size()
        x = screen_width - 50         
        y = screen_height // 2         

        pyautogui.moveTo(x, y, duration=0.2) 
        time.sleep(1)

        pyautogui.scroll(-5000)  
        time.sleep(0.2) 
        
        pyautogui.hotkey('ctrl', 'shift', 'c')
        time.sleep(2)

        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.typewrite('div.container')  
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        pyautogui.screenshot("screen.png")
        result = match_template("screen.png", "highlight_template_product_container.png")
        
        if result is None:  
            print(f"No products found {idx+1}, move to next product.")
            continue  

        center_x, center_y = result
        pyautogui.moveTo(center_x, center_y, duration=0.1)
        pyautogui.rightClick()
        time.sleep(1)

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
        all_elements.append([url, copied_data])
        print(f"Product {idx+1}: Copied first product information")
        
        pyautogui.hotkey('ctrl', 'w')  
        time.sleep(1)

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
