import os
import requests
import pandas as pd
from fake_useragent import UserAgent
import datetime

base_dir = './domain'
results_chung = []
ua = UserAgent()
urls = []

with open('search_results.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    url_info = {}
    
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

for url_info in urls:
    url = url_info['URL']
    try:
        headers = {
            'User-Agent': ua.random,
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            if 'not found' in response.text.lower():
                status = 'Error 404 Not found'
            else:
                status = 'URL còn tồn tại'
        elif response.status_code == 500:
            status = 'Error 500 - Không tồn tại trên Server'
        else:
            status = 'Đã bị chặn'
    
    except requests.ConnectionError:
        status = 'Lỗi kết nối'
    
    except requests.Timeout:
        status = 'Hết thời gian chờ'

    url_extension = os.path.splitext(url_info['URL'])[1].lower()
    
    if url_extension == ".pdf" or url_extension == '.doc':
        url_info['Phương thức'] = 'Upload Files'
    elif status == 'Not found':
        if '</script>' in response.text:
            url_info['Phương thức'] = 'Redirect Backlink'
        else:
            url_info['Phương thức'] = None
    elif status == 'Còn tồn tại' and any(keyword in url.lower() for keyword in ['gopy', 'gop_y', 'gop-y', 'hoidap', 'hoi_dap']):
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
df_chung.to_excel(excel_chung_file, index=False)
