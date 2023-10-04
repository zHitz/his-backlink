import os
import requests
import pandas as pd
from fake_useragent import UserAgent
import mimetypes

# Thư mục chứa các thư mục con chứa các file txt và kết quả
base_dir = './domain'

# Tạo một bảng để lưu trữ kết quả chung
results_chung = []

# Tạo một đối tượng UserAgent để tạo User-Agent ngẫu nhiên
ua = UserAgent()

# proxy_ip = "proxy_ip"  # Thay thế bằng địa chỉ IP proxy thực tế
# proxy_port = "proxy_port"  # Thay thế bằng cổng proxy thực tế


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
                    
                elif line.startswith("Description:"):
                    des = line.split("Description:")[1].strip()
                elif line == '------------------------------':
                    if url:
                        urls.append({'Title Search': title, 'URL': url, 'Description': des})
                    title = ''
                    url = ''
                    des = ''

        # Lặp qua các URL và kiểm tra
        for url_info in urls:
            url = url_info['URL']
            try:
                # Tạo tiêu đề User-Agent ngẫu nhiên và thêm tiêu đề Authorization
                headers = {
                    'User-Agent': ua.random,
                    'Referer': 'https://www.google.com/'
                }
                # proxies = {
                #     "http": f"http://{proxy_ip}:{proxy_port}",
                #     "https": f"http://{proxy_ip}:{proxy_port}",
                # }
                print(f"Đang truy cập {url} :")
                response = requests.head(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    status = 'Còn tồn tại'
                elif response.status_code == 404:
                    status = 'Not found'
                elif response.status_code == 500:
                    status = 'Không tồn tại trên Server'
                else:
                    status = 'Đã bị chặn'
                print(status)
            except requests.ConnectionError:
                status = 'Lỗi kết nối'
                print(status)
            except requests.Timeout:
                status = 'Hết thời gian chờ'
                print(status)

            # Kiểm tra đuôi URL nếu là pdf thì thêm cột "Phương thức" với giá trị "Upload Files"
            url_extension = os.path.splitext(url_info['URL'])[1].lower()
            if url_extension == ".pdf" or url_extension == '.doc':
                url_info['Phương thức'] = 'Upload Files'
            elif status == 'Not found':
                checksites = requests.get(url, headers=headers, timeout=5)
                if '</script>' in checksites.text:
                    url_info['Phương thức'] = 'Referrer Sites'
                else:
                    url_info['Phương thức'] = None
            elif status == 'Còn tồn tại' and ('gopy' in url.lower() or 'gop_y' in url.lower() or 'hoidap' in url.lower() or 'hoi_dap' in url.lower()):
                url_info['Phương thức'] = 'Upload Form'

            else:
                url_info['Phương thức'] = None

            results_chung.append({
                'Domain': folder,
                'Title Search': url_info['Title Search'],
                'URL': url_info['URL'],
                'Mô tả': url_info['Description'],
                'Status': status,
                'Phương thức': url_info['Phương thức']
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
