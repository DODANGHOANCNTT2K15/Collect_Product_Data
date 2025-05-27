# 🛍️ Collect Product Data from Shopee
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

## 🎯 Purpose
- The purpose of this repo is to collect at least 300 products from shopee
- Then clean the data and save it to a csv file
- Use BeautifulSoup
- Finally, output a csv file containing data for at least 300 products.

## 📚 Required Libraries
    - webbrowser
    - pyautogui
    - time
    - cv2
    - csv
    - pyperclip
    - subprocess
    - datetime
    - pandas
    - BeautifulSoup

Command to install all: 
```bash
pip install pyautogui opencv-python pyperclip pandas beautifulsoup4
```

## ⚠️ Project Limitations
- Because shopee blocks data retrieval. So I can't use BeautifulSoup or Selenium to extract html as usual. So I will use pyautogui to automatically control the mouse to manually copy elements from Devtools. This also avoids shopee detecting me as a robot and asking for captcha.
- Because of using pyautogui, during the program running. Therefore, you will not be able to perform other tasks on your computer. End it will take a lot of time because you have to copy elements manually like that.

## ✨ Solution V1 (Very BAD - You should skip to next solution)
### ⏱️ Performance
- With high nextwork speed
- Data collection completion time: 02:33:37 (hh:mm:ss)

### 📁 File Structure
```
├── Get_URL_Category.py
├── Get_Href_Category.py
├── Get_URL_Product.py
├── Get_Href_Product.py
├── Get_Info_Detail_Product.py
├── Extract_Product_Information.py
├── Run_all.py
└── README.md
```
### 📁 Output Files
- element_data_category.csv
- full_link_category.csv
- full_link_product.csv
- full_info_detail_product.csv
- product_info.csv

### 🔄 Process Flow
1. Step 1 - "Get_URL_Category.py"
    - First access "https://www.shopee.vn/""
    - Open Devtools find element have class "home-category-list__category-grid". Detail:
        + Use pyautogui open Devtools Elements by hotkey 'ctrl', 'shift', 'c' - shortcut open Devtools element.
        + Then hotkey 'ctrl', 'f' - Open search box in Elements.
        + Then type "home-category-list__category-grid" by pyautogui - To find element
        + Take a screenshot and compare it with the sample image - the sample image is the highline image of "home-category-list__category-grid" - then calculate its position on the screen.
        + Move mouse to this postion.
        + Pyautogui right click.
        + Take a screenshot and compare it with the sample image - the sample image is the highline image of button "Copy" - then left click.
        + Take a screenshot and compare it with the sample image - the sample image is the highline image of button "Element" - then left click.
        + Save this element to array
    - Copy element(27 element) save to element_data_category.csv 
2. Step 2 - "Get_Href_Category.py"
    - Use BeautifullSoup to extract url category.
    - Then append it with "https://shopee.vn".
    - Save to "full_link_category.csv".
3. Step 3 - "Get_URL_Product.py"
    - Read file "full_link_category.csv".
    - Loop through the links and access it.
    - Each loop:
        + Check web is loaded.
        + Scroll down to bottom to load full page.
        + Then find element and copy like "Get_URL_Category.py".
    - Save to "element_data_all_products.csv".
4. Step 4 - "Get_Href_Product.py"
    - Use BeautifullSoup to extract url category.
    - Then append it with "https://shopee.vn".
    - Save to "full_link_product.csv".
5. Step 5 - "Get_Info_Detail_Product.py"
    - This step is same step 1, 3. But with a little improvement. That is copy parent element containing product information. I will use this method to improve in Solution 2 .
    - NOTE: I don't want to modify directly on Step 1, 2 because at this step I just thought of that solution. So I will rewrite it into a Solution V2, the code will be cleaner and shorter in V2. I want to keep this V1 for historical comparison as small changes can greatly improve performance.
    - Save to "full_info_detail_product.csv"
6. Step 6 - "Extract_Product_Information.py"
    - Use BeautifullSoup to extract product data fields.
    - Save to "product_info.csv". 
    
### 🚀 How to run it?
- Command to install all: 
```bash
pip install pyautogui opencv-python pyperclip pandas beautifulsoup4
```
- python Run_all.py

## ✨ Solution V2 (Better - Improved from V1 )
### ⏱️ Performance
- With high nextwork speed
- Data collection completion time: ..:..:.. (hh:mm:ss)

### 📁 File Structure
```
├── check_page_load.py
├── extract_data_products.py
├── get_link_category.py
├── get_link_products.py
├── load_image_element.py
└── main.py
```
### 📁 Output Files
- full_link_category.csv
- full_link_product.csv
- data_product.csv 

### 🔄 Process Flow

    
### 🚀 How to run it?
- Command to install all: 
```bash
pip install pyautogui opencv-python pyperclip pandas beautifulsoup4
```
- python main.py

