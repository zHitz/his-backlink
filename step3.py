import os
import requests
import pandas as pd
from fake_useragent import UserAgent
import datetime
import logging

# Cấu hình logging
log_file = 'logs-backlink.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')
logging.info('------------------------------')
logging.info('Bắt đầu Step 3')

# Đường dẫn tới thư mục /his-backlink/
base_directory = os.path.abspath("./")

results_chung = []
ua = UserAgent()
urls = []

with open(os.path.join(base_directory, 'search_results.txt'), 'r', encoding='utf-8') as file:
    lines = file.readlines()
    logging.info('Đọc kết quả tìm kiếm từ file search_results.txt')
    url_info = {}
    logging.info('Parse kết quả')
    for line in lines:
        line = line.strip()
        if line.startswith("Domain:"):
            url_info['Domain'] = line.split("Domain:")[1].strip()
        elif line.startswith("Title:"):
            url_info['Title Search'] = line.split("Title:")[1].strip()
        elif line.startswith("URL:"):
            url_info['URL'] = line.split("URL:")[1].strip()
        elif line.startswith("Description:"):
            url_info['Description'] = line.split("Description:")[1].strip()
        elif line == '------------------------------':
            if 'URL' in url_info:
                urls.append(url_info)
            url_info = {}
logging.info('Bắt đầu kiểm tra URL và nhận diện phương thức tấn công ...')
for url_info in urls:
    url = url_info['URL']
    try:
        headers = {
            'User-Agent': ua.random,
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print(response.text.lower())
            if 'not found' in response.text.lower():
                status = 'Error 404 Not found'
            elif 'the requested url was rejected. please consult with your administrator.' in response.text.lower():
                status = 'URL bị chặn bởi F5'   
            elif "this page can't be displayed. contact support for additional information." in response.text.lower():
                status = 'URL bị chặn bởi Imperva'
            else:    
                status = 'URL còn tồn tại'
        elif response.status_code == 500:
            status = 'Error 500 - Không tồn tại trên Server'
        elif response.status_code == 404:
            status = 'Error 404 Not found'
        print(response.text.lower())
    except requests.ConnectionError:
        status = 'Lỗi kết nối'
    
    except requests.Timeout:
        status = 'Hết thời gian chờ'

    url_extension = os.path.splitext(url_info['URL'])[1].lower()
    
    if url_extension == ".pdf" or url_extension == '.doc':
        url_info['Phương thức'] = 'Upload Files'
    elif status == 'Error 404 Not found':
        if '</script>' in response.text:
            url_info['Phương thức'] = 'Redirect Backlink'
        else:
            url_info['Phương thức'] = None
    elif status == 'URL còn tồn tại' and any(keyword in url.lower() for keyword in ['gopy', 'gop_y', 'gop-y', 'hoidap', 'hoi_dap']):
        url_info['Phương thức'] = 'Upload Form'
    else:
        url_info['Phương thức'] = None

    results_chung.append({
        'Domain': url_info['Domain'],
        'Title Search': url_info['Title Search'],
        'URL': url_info['URL'],
        'Mô tả': url_info['Description'],
        'Status': status,
        'Phương thức': url_info['Phương thức']
    })

df_chung = pd.DataFrame(results_chung)

current_date = datetime.datetime.now().strftime('%Y-%m-%d')

excel_chung_file = f'results_backlink_{current_date}.xlsx'

logging.info(f'Tạo datafame và lưu vào file: {excel_chung_file}')
df_chung.to_excel(os.path.join(base_directory, f"{excel_chung_file}"), index=False)
