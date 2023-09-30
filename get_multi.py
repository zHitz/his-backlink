from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Danh sách các từ khoá bạn muốn tìm kiếm
search_keywords = ['casino site:*.tphcm.gov.vn', 'sổ xố site:*.tphcm.gov.vn', 'lô đề site:*.tphcm.gov.vn', 'sex site:*.tphcm.gov.vn', 'đánh bài site:*.tphcm.gov.vn']

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

# Mở trang Google
driver.get('https://www.google.com')
# Mở tệp tin để ghi kết quả
with open('search_results.txt', 'w', encoding='utf-8') as file:
    # Mở trang Google
    driver.get('https://www.google.com')

    for keyword in search_keywords:
        # Tìm kiếm keyword
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.submit()

        # Chờ cho trang tải
        driver.implicitly_wait(10)  # Chờ tối đa 10 giây cho trang tải

        # Lấy các kết quả
        max_results = 30  # Số kết quả tối đa bạn muốn lấy
        num_results = 0
        scroll_pause_time = 2  # Thời gian chờ giữa mỗi lần cuộn trang (giây)

        while num_results < max_results:
            search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

            for result in search_results:
                try:
                    title = result.find_element(By.CSS_SELECTOR, 'h3').text
                    url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    file.write(f'Title: {title}\n')
                    file.write(f'URL: {url}\n')
                    file.write('-' * 30 + '\n')
                    num_results += 1
                except Exception as e:
                    print(f"Error: {str(e)}")

            # Cuộn trang web xuống
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Chờ cho trang tải thêm dữ liệu
            time.sleep(scroll_pause_time)

            # Kiểm tra xem đã đạt được số kết quả tối đa chưa
            if num_results >= max_results:
                break

# Đóng trình duyệt
driver.quit()
