from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import io 
import os
from PIL import Image, ImageDraw, ImageFont

# Set the download directory
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--ignore-ssl-errors')  # Ignore SSL errors
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless=new')
# options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-download-notification')

# Thư mục chứa các thư mục con chứa các file txt và kết quả
base_dir = 'E:/Lab/his-backlink/domain'

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Kích thước mới cho ảnh (độ phân giải thấp)
new_width = 800
new_height = 600

# Lặp qua các thư mục con trong thư mục gốc
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if os.path.isdir(folder_path):
        # Tạo đường dẫn đến tệp tin search_results.txt trong thư mục con
        search_results_file_path = os.path.join(folder_path, 'search_results.txt')

        # Kiểm tra xem tệp tin search_results.txt có tồn tại trong thư mục con không
        if os.path.exists(search_results_file_path):
            # Đọc danh sách liên kết (URL) từ tệp tin search_results.txt
            with open(search_results_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                urls = []

                for line in lines:
                    line = line.strip()
                    if line.startswith("URL:"):
                        url = line.split("URL:")[1].strip()
                        urls.append(url)

                # Lặp qua danh sách liên kết (URL) và chụp hình
                for index, link in enumerate(urls):
                    # Mở liên kết (URL)
                    driver.get(link)
                    
                    # Chờ 3 giây trước khi chụp hình
                    time.sleep(3)

                    # Chụp hình toàn bộ trang web
                    screenshot = driver.get_screenshot_as_png()
                    
                    # Chuyển đổi ảnh từ dạng bytes sang đối tượng Image của Pillow
                    img = Image.open(io.BytesIO(screenshot))
                    
                    # # Điều chỉnh kích thước ảnh
                    # img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    
                    # Thêm đường dẫn vào ảnh
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()  # Sử dụng font mặc định
                    text = link
                    draw.text((10, 10), text, fill=(255, 255, 255), font=font)
                    
                    # Lưu ảnh với độ phân giải thấp
                    screenshot_filename = os.path.join(folder_path, f'screenshot_{index + 1}.png')
                    img.save(screenshot_filename, optimize=True, quality=10)  # quality 10 để giảm chất lượng hình ảnh

# Đóng trình duyệt
driver.quit()
