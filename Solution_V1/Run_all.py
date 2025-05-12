import subprocess
import time
import datetime

scripts = [
    "Get_URL_Category.py",
    "Get_Href_Category.py",
    "Get_URL_Product.py",
    "Get_Href_Product.py",
    "Get_Info_Detail_Product.py",
    "Extract_Product_Information.py"
]

total_time = 0

for script in scripts:
    print(f"Running: {script}")
    start_time = time.time()  
    
    try:
        result = subprocess.run(['python', script], capture_output=True, text=True, check=True)
        print(f"Result {script}:\n{result.stdout}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error {script}:\n{e.stderr}")
    except FileNotFoundError:
        print(f"No file: {script}")
    
    end_time = time.time() 
    script_time = end_time - start_time  
    total_time += script_time
    
    script_time_formatted = str(datetime.timedelta(seconds=int(script_time)))
    print(f"Time Run {script}: {script_time_formatted}\n")
    
total_time_formatted = str(datetime.timedelta(seconds=int(total_time)))
print(f"All time run all script: {total_time_formatted}")