import pyautogui
import time
import webbrowser
import csv
import pyperclip
import pandas as pd
from bs4 import BeautifulSoup

from check_page_load import check_page_loaded
from locate_image_element import match_template

def get_href_category(url):
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    max_wait_time = 10

    #open shopee
    webbrowser.get(chrome_path).open(url)
    time.sleep(1)
    for i in range(max_wait_time):
        pyautogui.screenshot("screen.png")
        time.sleep(0.5)
        if check_page_loaded("loaded_element.png", "screen.png"):
            print("Page loaded successfully.")
            break
        time.sleep(1)
    else:
        print("Page loading timed out.")
    time.sleep(1)

    #get element category
    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.typewrite('home-category-list')
    time.sleep(0.5)
    pyautogui.screenshot("screen.png")
    center_x, center_y = match_template("screen.png", "highlight_template.png")
    pyautogui.moveTo(center_x, center_y)
    pyautogui.rightClick()
    time.sleep(0.1)
    pyautogui.screenshot("screen.png")
    center_x, center_y = match_template("screen.png", "copy_button_template.png")
    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.screenshot("screen.png")
    center_x, center_y = match_template("screen.png", "copy_element_template.png")
    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'w')
    
    return pyperclip.paste()

def extract_category_data():
    category_data = get_href_category("https://shopee.vn")
    time.sleep(1)
    soup = BeautifulSoup(category_data, 'html.parser')
    category_link_list = []
    for a_tag in soup.find_all('a', class_='home-category-list__category-grid'):
        if a_tag and a_tag.get('href'):
            category_link_list.append("https://shopee.vn" + a_tag['href'])

    with open('full_link_category.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category Shopee URL'])
        for link in category_link_list:
            writer.writerow([link])
    print("Extracted href and saved to file full_link_category.csv")