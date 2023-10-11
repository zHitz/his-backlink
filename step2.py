from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pickle

# Kiểm tra xem tệp "domain_results.txt" có tồn tại và không rỗng không
def is_domain_file_valid(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

unique_urls = set()
domain = ''

# Xóa file trước khi thực thi
file_path = 'search_results.txt'

# kiểm tra file xóa
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} has been deleted.")
else:
    print(f"{file_path} does not exist.")

try:
    # Đọc tập hợp từ tệp Python khác (nếu tệp tồn tại)
    with open("list_urls.pkl", "rb") as file:
        list_urls = pickle.load(file)
except FileNotFoundError:
    # Nếu tệp không tồn tại, tạo một tập hợp mới
    list_urls = set()
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
        # options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-download-notification')
        # options.add_argument("user-data-dir=selenium")
        # For ChromeDriver version 79.0.3945.16 or over
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("window-size=1280,800")
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
        options.add_argument("--headless")  # Chạy ẩn danh (không hiển thị giao diện)
        options.add_argument("--no-sandbox")  # Chạy không có sandbox        
        options.binary_location = "/usr/bin/chromium-browser"
        

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        #Remove navigator.webdriver Flag using JavaScript
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        base_folder = './domain'
        
        # # Mở trang Google
        # driver.get("http://www.google.com")
        # Tạo thư mục để lưu kết quả
        for keyword in search_keywords:
            # Mở tệp tin để ghi kết quả
            with open('search_results.txt', 'a', encoding='utf-8') as file:
                domain = keyword
                keyword = f'"roulette" | "nổ hũ" | intext:"casino" | "sex" | "soi-keo" | "gambling" site:{keyword}'
                search_url = f'https://www.google.co.in/search?q={keyword.replace(" ", "%20")}'
                print(keyword)
                time.sleep(240)
                driver.get(search_url)
                # # Tìm kiếm keyword
                # search_box = driver.find_element(By.NAME, 'q')
                # search_box.send_keys(keyword)
                # search_box.send_keys(Keys.RETURN)
                time.sleep(20)
                
                driver.implicitly_wait(10)
                num_results = 0
                max_results = 100
                scroll_pause_time = 3
                previous_scroll_y = driver.execute_script('return window.scrollY')
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
                            print(f"Error: {str(e)}")

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
        driver.quit()
    else:
        print("Tệp 'domain_results.txt' không hợp lệ hoặc không tồn tại.")
except Exception as ex:
    print(f"Lỗi hệ thống: {str(ex)}")

# Chuyển tập hợp thành danh sách
list_urls.update(unique_urls)
# Lưu tập hợp đã được cập nhật vào tệp Python khác
with open("list_urls.pkl", "wb") as file:
    pickle.dump(list_urls, file)
