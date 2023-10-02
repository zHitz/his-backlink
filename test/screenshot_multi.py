from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import io 
from PIL import Image

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


driver = webdriver.Chrome(options=options)
driver.maximize_window()
# Đọc danh sách liên kết từ tệp tin .txt
with open('links.txt', 'r') as file:
    links = file.readlines()

# Xóa khoảng trắng và ký tự xuống dòng từ mỗi liên kết
links = [link.strip() for link in links]

# Kích thước mới cho ảnh (độ phân giải thấp)
new_width = 800
new_height = 600

# Lặp qua danh sách liên kết và chụp hình
for index, link in enumerate(links):
    # Mở liên kết
    driver.get(link)
    
    # Chờ 3 giây trước khi chụp hình
    time.sleep(3)

    # Chụp hình toàn bộ trang web
    screenshot = driver.get_screenshot_as_png()
    
    # Chuyển đổi ảnh từ dạng bytes sang đối tượng Image của Pillow
    img = Image.open(io.BytesIO(screenshot))
    
    # Điều chỉnh kích thước ảnh
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    # Lưu ảnh với độ phân giải thấp
    screenshot_filename = f'screenshot_{index + 1}.png'
    img.save(screenshot_filename, optimize=True, quality=10)  # quality 10 để giảm chất lượng hình ảnh
    
# Đóng trình duyệt
driver.quit()





