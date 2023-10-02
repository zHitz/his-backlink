from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
# from keyword import search_keywords


# Đọc danh sách từ khoá từ tệp keyword.txt
with open('domain_results.txt', 'r', encoding='utf-8') as keyword_file:
    search_keywords = keyword_file.read().splitlines()

# Set the download directory
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--ignore-ssl-errors')  # Ignore SSL errors
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-download-notification')

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Mở trang Google
driver.get('https://www.google.com')

time.sleep(5)
# Đường dẫn đến thư mục 'domain'
base_folder = './domain'

# Tạo thư mục để lưu kết quả
for keyword in search_keywords:
    keyword_folder = os.path.join(base_folder, keyword.replace(" ", "_"))  # Thay khoảng trắng bằng _ và tạo đường dẫn đầy đủ    
    os.makedirs(keyword_folder, exist_ok=True)


    # Mở tệp tin để ghi kết quả
    with open(os.path.join(keyword_folder, 'search_results.txt'), 'w', encoding='utf-8') as file:
        
        keyword = f'intext:"lô đề" | intext:"nổ hũ" | intext:"casino" | intext:"sex" | intext:"bắn cá" site:{keyword}'
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.submit()
        
        # chờ search
        time.sleep(20)
        # Chờ cho trang tải
        driver.implicitly_wait(10)  # Chờ tối đa 10 giây cho trang tải

        # Lấy các kết quả
        max_results = 30  # Số kết quả tối đa bạn muốn lấy
        num_results = 0
        scroll_pause_time = 2  # Thời gian chờ giữa mỗi lần cuộn trang (giây)

        # Đánh dấu vị trí hiện tại
        previous_scroll_y = driver.execute_script('return window.scrollY')

        while num_results < max_results:
            search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

            for result in search_results:
                try:
                    title = result.find_element(By.CSS_SELECTOR, 'h3').text
                    url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    # Tạo một WebElement từ đoạn mã HTML
                    description = result.find_element(By.XPATH, './/div[@style="-webkit-line-clamp:2"]').text
                    
                    file.write(f'Number: {num_results}\n')
                    file.write(f'Title: {title}\n')
                    file.write(f'URL: {url}\n')
                    file.write(f"Description: {description}\n")
                    file.write('-' * 30 + '\n')
                    num_results += 1
                except Exception as e:
                    print(f"Error: {str(e)}")

            # Cuộn trang web xuống
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Chờ cho trang tải thêm dữ liệu
            time.sleep(scroll_pause_time)

            no_scroll = False

            # Kiểm tra xem đã đạt được số kết quả tối đa chưa
            if num_results >= max_results:
                break
            
            # Kiểm tra xem đã cuộn xuống cuối trang chưa
            current_scroll_y = driver.execute_script('return window.scrollY')
            if current_scroll_y == previous_scroll_y:
                no_scroll = True
                break
            previous_scroll_y = current_scroll_y
# Đóng trình duyệt
driver.quit()
