import pandas as pd

def count_products():
    try:
        # Đọc file CSV
        df = pd.read_csv('data_product.csv')
        
        # Đếm số lượng sản phẩm
        total_products = len(df)
        
        # In kết quả
        print("\n----------------------------------------")
        print(f"Tổng số sản phẩm: {total_products:,}")
        print("----------------------------------------")
        
        return total_products
        
    except FileNotFoundError:
        print("Error: File data_product.csv không tồn tại!")
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 0

if __name__ == "__main__":
    count_products()