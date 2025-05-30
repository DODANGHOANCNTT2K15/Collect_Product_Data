import pandas as pd
import webbrowser
import pyautogui
import time
import csv
import pyperclip
from bs4 import BeautifulSoup
from check_page_load import check_page_loaded
from locate_image_element import match_template

#define
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
max_wait_time = 10
all_elements = []
all_links = []
data_products = []
skip = 0
complete = 0

def get_elements_product():
    global all_elements, all_links, data_products, skip, complete

    #get all link product
    with open('full_link_product.csv', 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            all_links.append(row[0])

    #access each link product
    for link in all_links:
        webbrowser.get(chrome_path).open(link)
        time.sleep(1)
        for i in range(max_wait_time):
            pyautogui.screenshot("screen.png")
            time.sleep(0.5)
            if check_page_loaded("loaded_element2.png", "screen.png") or check_page_loaded("loaded_element1.png", "screen.png"):
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
        pyautogui.scroll(-5000)  
        time.sleep(0.2) 
        
        #get element product
        pyautogui.hotkey('ctrl', 'shift', 'c')
        for i in range(max_wait_time):
            pyautogui.screenshot("screen.png")
            time.sleep(0.5)
            if check_page_loaded("loaded_devtool.png", "screen.png"): 
                print("Devtool loaded successfully.")
                break
            time.sleep(1)
        else:
            print("Devtool loading timed out.")
            skip += 1
            pyautogui.hotkey('ctrl', 'w')
            continue
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.typewrite('div.container')
        time.sleep(1)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "highlight_template_product_container.png")
        if center_x is None or center_y is None:
            print("Element not found, skipping...")
            skip += 1
            pyautogui.hotkey('ctrl', 'w')
            continue
        pyautogui.moveTo(center_x, center_y)
        pyautogui.rightClick()
        time.sleep(0.1)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "copy_button_template.png")
        if center_x is None or center_y is None:
            print("Element not found, skipping...")
            skip += 1
            pyautogui.hotkey('ctrl', 'w')
            continue
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.screenshot("screen.png")
        center_x, center_y = match_template("screen.png", "copy_element_template.png")
        if center_x is None or center_y is None:
            print("Element not found, skipping...")
            skip += 1
            pyautogui.hotkey('ctrl', 'w')
            continue
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        time.sleep(0.1)
        
        #save element
        all_elements.append(pyperclip.paste())
        time.sleep(1)
        complete += 1
        pyautogui.hotkey('ctrl', 'w')

def extrack_data_product():
    get_elements_product()
    time.sleep(1)
    for idx, html in enumerate(all_elements):
        image = None
        name = None
        rate_star = None
        sold = None
        selling_price = None
        original_price = None
        available_product = None
        description = None

        soup = BeautifulSoup(html, 'html.parser')

        ## picture
        picture = soup.find('picture', class_='UkIsx8')
        if not picture:
            image = 'NULL'
        else:
            source = picture.find('source')
            if not source or not source.has_attr('srcset'):
                image = 'NULL'
            else:
                srcset = source['srcset']
                parts = srcset.split(',')
                if len(parts) < 2:
                    image = 'NULL'
                else:
                    image = parts[1].strip().split(' ')[0]
        ## end picture

        ## get name
        name = soup.find('h1', class_='vR6K3w')
        if not name:
            name = 'NULL'
        else: 
            name = name.get_text(strip=True)
        ## end get name

        ## get rate
        rate_star = soup.find('div', class_='F9RHbS dQEiAI jMXp4d')
        if not rate_star:
            rate_star = 'NULL'
        else:
            rate_star = rate_star.get_text(strip=True)
        ## end get rate

        ## get solded
        sold = soup.find('span', class_='AcmPRb')
        if not sold:
            sold = 'NULL'
        else:
            sold = sold.get_text(strip=True)
        ## end end solded

        ## get selling price
        selling_price = soup.find('div', class_='IZPeQz B67UQ0')
        if not selling_price:
            selling_price = 'NULL'
        else:
            selling_price = selling_price.get_text(strip=True)
        ## end end selling price

        ## get original price
        original_price = soup.find('div', class_='ZA5sW5')
        if not original_price:
            original_price = 'NULL'
        else:
            original_price = original_price.get_text(strip=True)
        ## end get original price
        
        ## get available product
        available_product = soup.find('section', class_='OaFP0p')
        if not available_product:
            available_product = 'NULL'
        else:
            divs = available_product.find_all('div')
            for div in divs:
                text = div.get_text(strip=True)
                if 'sản phẩm có sẵn' in text:
                    available_product = text.split(' ')[0]
                    break
        ## end get available product

        ## description
        description = soup.find('div', class_='e8lZp3')
        if not description:
            description = 'NULL'
        else:
            p_elements = description.find_all('p', class_='QN2lPu')
            description_content = ''
            for content in p_elements:
                text = content.get_text(strip=True)
                description_content += text 
        ## end description

        data_products.append([image, name, rate_star, sold, selling_price, original_price, available_product, description_content])

    #save to csv
    df = pd.DataFrame(data_products, columns=['image', 'name', 'rate_star', 'sold', 'selling_price', 'original_price', 'available_product', 'description'])
    df.to_csv('data_product.csv', index=False)
