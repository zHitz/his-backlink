import requests
import pandas as pd
from fake_useragent import UserAgent

# Đọc danh sách URL từ tệp văn bản
with open('danhsach_url.txt', 'r') as file:
    urls = file.readlines()

# Loại bỏ khoảng trắng và ký tự xuống dòng từ các URL
urls = [url.strip() for url in urls]

# Tạo một bảng để lưu trữ kết quả
results = []

# Tạo một đối tượng UserAgent để tạo User-Agent ngẫu nhiên
ua = UserAgent()

# Kiểm tra mỗi URL
for url in urls:
    try:
        # Loại bỏ số thứ tự và khoảng trắng ở đầu URL
        url = url.split(' ', 1)[-1].strip()
        
        # Tạo tiêu đề User-Agent ngẫu nhiên cho yêu cầu
        headers = {'User-Agent': ua.random}
        print(f"Đang truy cập {url} :")
        response = requests.head(url, headers=headers, timeout=5)
        if response.status_code == 200:
            status = 'Sống'
        else:
            status = 'Không sống'
        print(status)
    except requests.ConnectionError:
        status = 'Lỗi kết nối'
        print(status)
    except requests.Timeout:
        status = 'Hết thời gian chờ'
        print(status)
    
    results.append({
        'URL': url,
        'Trạng thái': status
    })

# Tạo DataFrame từ kết quả và hiển thị bảng
df = pd.DataFrame(results)
print(df)
