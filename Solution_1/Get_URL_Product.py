import webbrowser
import pyautogui
import time
import csv
import pyperclip
import numpy as np
import cv2
from check_temp_on_screen import is_template_on_screen  
from Get_URL_Category import match_template

def main():
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    category_links = []
    all_elements = []
    pyautogui.FAILSAFE = False  
    
    # read the category links from CSV file
    with open('full_link_category.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            category_links.append(row[0])  
            
    # loop through each category link, open it in the browser, and extract product links
    for idx, url in enumerate(category_links):
        print(f"Access the catalog {idx+1}/{len(category_links)}")
        webbrowser.get(chrome_path).open(url)
        time.sleep(1)

        # Check if the page is loaded
        if is_template_on_screen("loaded_element1.png", threshold=0.75):
            print("The image has appeared on the screen..")
        else:
            print("No image after multiple checks.")
            continue
        # end check page loaded
        
        # find the position of the scroll bar, scroll to load more scripts
        screen_width, screen_height = pyautogui.size()
        x = screen_width - 50          
        y = screen_height // 2         

        pyautogui.moveTo(x, y, duration=0.2) 
        pyautogui.scroll(-5000)  
        time.sleep(0.2) 
        # end scroll

        # open the developer tools, find the element, and copy product link
        pyautogui.hotkey('ctrl', 'shift', 'c')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.typewrite('a.contents') 
        time.sleep(1)
        pyautogui.screenshot("screen.png")
        result = match_template("screen.png", "highlight_template_product_link.png")
        
        if result is None:  
            print(f"No products found in the category {idx+1}, move to next category.")
            continue 

        center_x, center_y = result
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
        all_elements.append([url, copied_data])
        print(f"Category {idx+1}: Copied first product")
        # end find the element, and copy product link

        # Lấy thêm sản phẩm tiếp theo
        for i in range(1, 12):  
            print(f"Category {idx+1} - product {i+1}")
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            for j in range(i+1):
                pyautogui.press('enter')
                time.sleep(0.5)

            pyautogui.screenshot("screen.png")
            result = match_template("screen.png", "highlight_template_product_link.png")
            
            if result is None:  
                print(f"No product found {i+1} in the category {idx+1}, move to next category.")
                break  

            center_x, center_y = result
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
            all_elements.append([url, copied_data])
            print(f"Category {idx+1}: Copied product {i+1}")
        
        pyautogui.hotkey('ctrl', 'w')  
        time.sleep(0.5)

    # Save to CSV
    with open("element_data_all_products.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Product URL", "Element"])
        writer.writerows(all_elements)

    print("All saved to element_data_all_products.csv")

if __name__ == "__main__":
    main()
