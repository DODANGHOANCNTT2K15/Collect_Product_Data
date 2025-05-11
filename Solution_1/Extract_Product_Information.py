import pandas as pd
from bs4 import BeautifulSoup
import csv 

def main():
    csv.field_size_limit(100 * 1024 * 1024)

    with open('full_info_detail_product.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # bỏ header
        for row in reader:
            all_elements.append(row[1])

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

        ## lấy ảnh
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
        ## end láy ảnh

        ## lấy tên
        name = soup.find('h1', class_='vR6K3w').get_text(strip=True)
        if not name:
            name = 'NULL'
        ## end lấy tên

        ## lấy đánh giá
        rate_star = soup.find('div', class_='F9RHbS dQEiAI jMXp4d')
        if not rate_star:
            rate_star = 'NULL'
        else:
            rate_star = rate_star.get_text(strip=True)
        ## end lấy đánh giá

        ## lấy số lượng bán
        sold = soup.find('span', class_='AcmPRb').get_text(strip=True)
        if not sold:
            sold = 'NULL'
        ## end lấy số lượng bán

        ## lấy giá bán
        selling_price = soup.find('div', class_='IZPeQz B67UQ0')
        if not selling_price:
            selling_price = 'NULL'
        else:
            selling_price = selling_price.get_text(strip=True)
        ## end lấy giá bán

        ## lấy giá gốc
        original_price = soup.find('div', class_='ZA5sW5')
        if not original_price:
            original_price = 'NULL'
            
        else:
            original_price = original_price.get_text(strip=True)
        ## end lấy giá gốc
        
        ## lấy số lượng còn lại
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
        ## end lấy số lượng còn lại

        ## lấy mô tả
        description = soup.find('div', class_='e8lZp3')
        if not description:
            description = 'NULL'
            
        else:
            p_elements = description.find_all('p', class_='QN2lPu')
            description_content = ''
            for content in p_elements:
                text = content.get_text(strip=True)
                description_content += text 
        ## end lấy mô tả

        all_products.append([image, name, rate_star, sold, selling_price, original_price, available_product, description_content])

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['Image', 'Name', 'Rate Star', 'Sold', 'Selling Price', 'Original Price', 'Available Product', 'Description'])
        writer.writerows(data)
        print("Extracted product information and saved to 'product_info.csv'")

if __name__ == "__main__":
    all_elements = []    
    all_products = []

    main()

    save_to_csv(all_products, 'product_info.csv')
    