import csv

with open("product_info.csv", "r", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    first_row = next(reader)  # Lấy dòng đầu tiên
    print(first_row['Description'])  # In cột Description
