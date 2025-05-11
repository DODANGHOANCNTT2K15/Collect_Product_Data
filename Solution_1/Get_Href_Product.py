import pandas as pd
from bs4 import BeautifulSoup

def extract_href_with_bs(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tag = soup.find('a')
    if a_tag and a_tag.get('href'):
        return "https://shopee.vn" + a_tag['href']
    return None

if __name__ == "__main__":
    df = pd.read_csv('element_data_all_products.csv') 

    df['Shopee URL'] = df['Element'].apply(extract_href_with_bs)

    df[['Shopee URL']].to_csv('full_link_product.csv', index=False)

    print("Extracted href and saved to 'full_link_product.csv'")
