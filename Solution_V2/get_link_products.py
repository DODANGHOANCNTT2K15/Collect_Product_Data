import pyautogui
import time
import csv
import pyperclip
import pandas as pd
import webbrowser
from bs4 import BeautifulSoup

from check_page_load import check_page_loaded
from locate_image_element import match_template

#define
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
elements = []
full_link_product = []
save_element = []
max_wait_time = 10
limit_product = 13


def get_link_product():
    #open csv
    with open('full_link_category.csv', 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            elements.append(row[0])

    #open category
    for element in elements:
        webbrowser.get(chrome_path).open(element)
        time.sleep(1)
        for i in range(max_wait_time):
            pyautogui.screenshot("screen.png")
            time.sleep(0.5)
            if check_page_loaded("loaded_element2.png", "screen.png"):
                print("Page loaded successfully.")
                break
            time.sleep(1)
        else:
            print("Page loading timed out.")
            continue
        time.sleep(1)

        #calculate position to move and scroll
        screen_width, screen_height = pyautogui.size()
        x = screen_width - 50         
        y = screen_height // 2        
        pyautogui.moveTo(x, y, duration=0.2) 
        time.sleep(1)
        pyautogui.scroll(-5000)  
        time.sleep(0.2) 

        #get element product
        pyautogui.hotkey('ctrl', 'shift', 'c')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        pyautogui.typewrite('shopee-search-item-result__items')
        time.sleep(0.5)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "highlight_template_product.png")
        if center_x is None or center_y is None:
            print("Element not found, skipping...")
            continue
        pyautogui.moveTo(center_x, center_y)
        pyautogui.rightClick()
        time.sleep(0.1)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "copy_button_template.png")
        if center_x is None or center_y is None:
            print("Element not found, skipping...")
            continue
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "copy_element_template.png")
        if center_x is None or center_y is None:
            print("Element not found, skipping...")
            continue
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        time.sleep(0.1)
        save_element.append(pyperclip.paste())
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(1)

def extract_link_product():
    get_link_product()
    time.sleep(1)
    for element in save_element:
        soup = BeautifulSoup(element, 'html.parser')
        # find all links that have class containing 'content'
        links = soup.find_all('a', class_=lambda x: x and 'content' in x, limit=limit_product)
        for link in links:
            href = link.get('href')
            if href:
                full_link_product.append("https://shopee.vn" + href)
            else:
                continue
    
    #save to csv
    df = pd.DataFrame(full_link_product, columns=['link'])
    df.to_csv('full_link_product.csv', index=False)
    print("Extracted links saved to full_link_product.csv")