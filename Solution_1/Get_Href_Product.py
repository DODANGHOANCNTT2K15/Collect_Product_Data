import pandas as pd
from bs4 import BeautifulSoup

# Đọc file CSV gốc
df = pd.read_csv('element_data_all_products.csv')  # Thay bằng tên file thực tế

# Hàm trích xuất href bằng BeautifulSoup
def extract_href_with_bs(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tag = soup.find('a')
    if a_tag and a_tag.get('href'):
        return "https://shopee.vn" + a_tag['href']
    return None

# Áp dụng hàm lên cột chứa HTML
df['Shopee URL'] = df['Element'].apply(extract_href_with_bs)

# Lưu ra file CSV mới
df[['Shopee URL']].to_csv('full_link_product.csv', index=False)
