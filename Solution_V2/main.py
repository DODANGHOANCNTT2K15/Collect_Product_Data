from get_link_categorys import extract_category_data
from get_link_products import extract_link_product
from extract_data_products import extrack_data_product
import time
from datetime import datetime, timedelta

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

if __name__ == "__main__":
    total_start_time = time.time()
    
    # Extract category links
    print("\n1. Extracting category links...")
    start_time = time.time()
    extract_category_data()
    end_time = time.time()
    print(f"-> Time taken: {format_time(end_time - start_time)}")
    time.sleep(1)
    
    # Extract product links 
    print("\n2. Extracting product links...")
    start_time = time.time()
    extract_link_product()
    end_time = time.time()
    print(f"-> Time taken: {format_time(end_time - start_time)}")
    time.sleep(1)
    
    # Extract product data
    print("\n3. Extracting product data...")
    start_time = time.time()
    extrack_data_product()
    end_time = time.time()
    print(f"-> Time taken: {format_time(end_time - start_time)}")
    
    # Calculate and display total time
    total_time = time.time() - total_start_time
    print("\n----------------------------------------")
    print(f"Total execution time: {format_time(total_time)}")
    print("Data extraction completed successfully.")