from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pickle
import logging

# Cấu hình logging
log_file = 'logs-backlink.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')
logging.info('------------------------------')
logging.info('Bắt đầu Step 2')
# Kiểm tra xem tệp "domain_results.txt" có tồn tại và không rỗng không
def is_domain_file_valid(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

# Đường dẫn tới thư mục /his-backlink/
base_directory = os.path.abspath("/his-backlink/")
logging.info('Đọc keyword từ file search_keyword.txt')
with open(os.path.join(base_directory, 'search_keyword.txt'), 'r', encoding='utf-8') as file:
    search = file.read()

unique_urls = set()
domain = ''

# Đường dẫn tới tệp search_results.txt trong thư mục /his-backlink/
file_path = os.path.join(base_directory, 'search_results.txt')

if os.path.exists(file_path):
    os.remove(file_path)
    logging.info('Xóa file search_reuslts.txt cũ')
try:
    with open(os.path.join(base_directory, 'list_urls.pkl'), 'rb') as file:
        list_urls = pickle.load(file)
except FileNotFoundError:
    list_urls = set()
try:
    if is_domain_file_valid(os.path.join(base_directory, 'domain_results.txt')):
        with open(os.path.join(base_directory, 'domain_results.txt'), 'r', encoding='utf-8') as keyword_file:
            search_keywords = keyword_file.read().splitlines()
        logging.info('Đọc file domain_results.txt')
        # Cấu hình trình duyệt
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-download-notification')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("window-size=1280,800")
        options.add_argument("--headless")  # Chạy ẩn danh (không hiển thị giao diện)
        options.add_argument("--no-sandbox")  # Chạy không có sandbox        
        options.binary_location = "/usr/bin/chromium-browser"
        

        driver = webdriver.Chrome(options=options)
        logging.info('Đã mở Chrome')
        driver.maximize_window()
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        for keyword in search_keywords:
            with open(file_path, 'a', encoding='utf-8') as file:
                domain = keyword
                keyword = f'{search} site:{keyword}'
                logging.info(f'Tìm kiếm keyword: {keyword} trên Chrome (Google)')
                search_url = f'https://www.google.co.in/search?q={keyword.replace(" ", "%20")}'
                time.sleep(240)
                driver.get(search_url)
                time.sleep(20)
                driver.implicitly_wait(10)
                num_results = 0
                max_results = 100
                scroll_pause_time = 3
                previous_scroll_y = driver.execute_script('return window.scrollY')
                logging.info('Bắt đầu kiểm tra kết quả tìm kiếm')
                while num_results < max_results:
                    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
                    for result in search_results:
                        try:
                            title = result.find_element(By.CSS_SELECTOR, 'h3').text
                            url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                            description = result.find_element(By.XPATH, './/div[@style="-webkit-line-clamp:2"]').text
                            if url not in unique_urls and url not in list_urls:
                                unique_urls.add(url)
                                file.write(f'Domain: {domain}\n')
                                file.write(f'Title: {title}\n')
                                file.write(f'URL: {url}\n')
                                file.write(f"Description: {description}\n")
                                file.write('-' * 30 + '\n')
                            num_results += 1
                        except Exception as e:
                            logging.error(f" {str(e)}")

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause_time)

                    no_scroll = False

                    if num_results >= max_results:
                        break

                    current_scroll_y = driver.execute_script('return window.scrollY')
                    if current_scroll_y == previous_scroll_y:
                        no_scroll = True
                        break
                    previous_scroll_y = current_scroll_y     
                logging.info('Đã thỏa điều kiện, dừng tìm kiếm')   
        driver.quit()
        logging.info('Đóng Chrome')   
    else:
        logging.error("Tệp 'domain_results.txt' không hợp lệ hoặc không tồn tại.")
except Exception as ex:
    logging.error(f"Lỗi hệ thống: {str(ex)}")

list_urls.update(unique_urls)
with open(os.path.join(base_directory, "list_urls.pkl"), "wb") as file:
    pickle.dump(list_urls, file)
logging.info('lưu kết quả tìm kiếm vào list_urls.pkl')   
