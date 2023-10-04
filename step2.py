from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Kiểm tra xem tệp "domain_results.txt" có tồn tại và không rỗng không
def is_domain_file_valid(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

try:
    # Kiểm tra và chạy code nếu tệp "domain_results.txt" hợp lệ
    if is_domain_file_valid('domain_results.txt'):
        # Đọc danh sách từ khoá từ tệp "domain_results.txt"
        with open('domain_results.txt', 'r', encoding='utf-8') as keyword_file:
            search_keywords = keyword_file.read().splitlines()

        # Cấu hình trình duyệt
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-download-notification')
        options.add_argument("--headless")  # Chạy ẩn danh (không hiển thị giao diện)
        options.add_argument("--no-sandbox")  # Chạy không có sandbox        
        options.binary_location = "/usr/bin/chromium-browser"
        

        driver = webdriver.Chrome(options=options)
        # driver.maximize_window()

        base_folder = './domain'

        # Tạo thư mục để lưu kết quả
        for keyword in search_keywords:
            keyword_folder = os.path.join(base_folder, keyword.replace(" ", "_"))
            os.makedirs(keyword_folder, exist_ok=True)

            # Mở tệp tin để ghi kết quả
            with open(os.path.join(keyword_folder, 'search_results.txt'), 'w', encoding='utf-8') as file:
                keyword = f'intext:"lô đề" | intext:"nổ hũ" | intext:"casino" | intext:"sex" | intext:"bắn cá" site:{keyword}'
                search_url = f'https://www.google.com/search?q={keyword.replace(" ", "%20")}&as_qdr=d1'
                print(search_url)
                driver.get(search_url)
                time.sleep(20)

                num_results = 0
                scroll_pause_time = 2
                previous_scroll_y = driver.execute_script('return window.scrollY')

                while num_results < 30:
                    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

                    for result in search_results:
                        try:
                            title = result.find_element(By.CSS_SELECTOR, 'h3').text
                            url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                            description = result.find_element(By.XPATH, './/div[@style="-webkit-line-clamp:2"]').text

                            file.write(f'Number: {num_results}\n')
                            file.write(f'Title: {title}\n')
                            file.write(f'URL: {url}\n')
                            file.write(f"Description: {description}\n")
                            file.write('-' * 30 + '\n')
                            num_results += 1
                        except Exception as e:
                            print(f"Error: {str(e)}")

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause_time)

                    no_scroll = False

                    if num_results >= 30:
                        break

                    current_scroll_y = driver.execute_script('return window.scrollY')
                    if current_scroll_y == previous_scroll_y:
                        no_scroll = True
                        break
                    previous_scroll_y = current_scroll_y

        driver.quit()
    else:
        print("Tệp 'domain_results.txt' không hợp lệ hoặc không tồn tại.")
except Exception as ex:
    print(f"Lỗi hệ thống: {str(ex)}")
