import subprocess
import time
import datetime

# Danh sách các script (giữ nguyên như bạn cung cấp)
scripts = [
    "Get_URL_Category.py",
    "Get_Href_Category.py",
    "Get_URL_Product.py",
    "Get_Href_Product.py",
    "Get_Info_Detail_Product.py",
    "Extract_Product_Information.py"
]

# Biến để lưu tổng thời gian
total_time = 0

# Chạy lần lượt từng script và đo thời gian
for script in scripts:
    print(f"Running: {script}")
    start_time = time.time()  # Thời gian bắt đầu
    
    try:
        # Chạy script bằng subprocess
        result = subprocess.run(['python', script], capture_output=True, text=True, check=True)
        # In kết quả (stdout) từ script nếu cần
        print(f"Result {script}:\n{result.stdout}")
        
    except subprocess.CalledProcessError as e:
        # In lỗi nếu script gặp vấn đề
        print(f"Error {script}:\n{e.stderr}")
    except FileNotFoundError:
        print(f"No file: {script}")
    
    end_time = time.time()  # Thời gian kết thúc
    script_time = end_time - start_time  # Thời gian chạy của script
    total_time += script_time
    
    # Chuyển đổi thời gian sang định dạng h:m:s
    script_time_formatted = str(datetime.timedelta(seconds=int(script_time)))
    print(f"Time Run {script}: {script_time_formatted}\n")

# Chuyển đổi tổng thời gian sang định dạng h:m:s
total_time_formatted = str(datetime.timedelta(seconds=int(total_time)))
print(f"All time run all script: {total_time_formatted}")