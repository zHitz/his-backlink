from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# Chrome driver path
chrome_driver_path = "C:\\Users\\PC\\Downloads\\chromedriver-win64\\"



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

# Mở trang web
driver.get('https://www.hissc.com.vn')


# Chờ cho trang web tải trong khoảng thời gian cố định (3 giây)
time.sleep(3)

# Chụp hình toàn bộ trang web và lưu vào tệp tin
driver.save_screenshot('full_page_screenshot.png')

# Đóng trình duyệt
driver.quit()
