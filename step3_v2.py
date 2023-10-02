import os
import requests
import pandas as pd
from fake_useragent import UserAgent

# Thư mục chứa các thư mục con chứa các file txt và kết quả
base_dir = 'domain'

# Tạo một bảng để lưu trữ kết quả chung
results_chung = []

# Tạo một đối tượng UserAgent để tạo User-Agent ngẫu nhiên
ua = UserAgent()

# Lặp qua các thư mục con trong thư mục cơ sở
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if os.path.isdir(folder_path):
        # Đọc danh sách URL và thông tin từ tệp văn bản trong thư mục con
        urls = []
        with open(os.path.join(folder_path, 'search_results.txt'), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            title = ''
            url = ''
            des = ''
            for line in lines:
                line = line.strip()
                if line.startswith("Title:"):
                    title = line.split("Title:")[1].strip()
                elif line.startswith("URL:"):
                    url = line.split("URL:")[1].strip()
                    
                elif line.startswith("Descrition:"):
                    url = line.split("Descrition:")[1].strip()
                elif line == '------------------------------':
                    if url:
                        urls.append({'Title Search': title, 'URL': url, 'Mô tả': des})
                    title = ''
                    url = ''
                    des = ''

        # Kiểm tra mỗi URL
        for url_info in urls:
            url = url_info['URL']
            try:
                # Tạo tiêu đề User-Agent ngẫu nhiên cho yêu cầu
                headers = {'User-Agent': ua.random}
                print(f"Đang truy cập {url} :")
                response = requests.head(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    status = 'Còn tồn tại'
                else:
                    status = 'Đã bị chặn'
                print(status)
            except requests.ConnectionError:
                status = 'Lỗi kết nối'
                print(status)
            except requests.Timeout:
                status = 'Hết thời gian chờ'
                print(status)

            results_chung.append({
                'Domain': folder,
                'Title Search': url_info['Title Search'],
                'URL': url_info['URL'],
                'Status': status
            })

        # Tạo DataFrame từ kết quả cho từng domain và lưu nó vào tệp Excel
        df_domain = pd.DataFrame(results_chung)
        domain_excel_file = os.path.join(folder_path, 'results.xlsx')
        df_domain.to_excel(domain_excel_file, index=False)
        print(f"Kết quả cho domain {folder} đã được lưu vào tệp Excel: {domain_excel_file}")

# Tạo DataFrame từ kết quả chung
df_chung = pd.DataFrame(results_chung)

# Lưu DataFrame chung vào tệp Excel chung với mã hóa UTF-8
excel_chung_file = 'results_chung.xlsx'
df_chung.to_excel(excel_chung_file, index=False)

print(f"Kết quả chung đã được lưu vào tệp Excel chung: {excel_chung_file}")
