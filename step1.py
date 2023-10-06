from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import pickle

# Danh sách các từ khoá bạn muốn tìm kiếm
search_keywords = ['"roulette" | "nổ hũ" | intext:"casino" | "sex" | "soi-keo" | "gambling" site:*.tphcm.gov.vn | site:*.hochiminhcity.gov.vn']
# Set the download directory
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--ignore-ssl-errors')  # Ignore SSL errors
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')
# options.add_argument("user-data-dir=selenium")
options.add_argument('--disable-gpu')
# options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-download-notification')
# options.add_argument('proxy-server=202.78.224.217:8132')
#For ChromeDriver version 79.0.3945.16 or over
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument("window-size=1280,800")
options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)
driver.maximize_window()
# Tạo một tập hợp để lưu các domain đã ghi
unique_domains = set()
domain_count = 0
# Mở trang Google
driver.get("http://www.google.com")
pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))

# Mở tệp tin để ghi kết quả
with open('domain_results.txt', 'w', encoding='utf-8') as file:
    for keyword in search_keywords:
        # Tạo URL tìm kiếm trên Google
        # search_url = f'https://www.google.co.in/search?q={keyword.replace(" ", "%20")}'
        # print(search_url)
        # time.sleep(60)
        # driver.get(search_url)
        
        # Tìm kiếm keyword
        time.sleep(5)
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(120)
        # Chờ cho trang tải
        driver.implicitly_wait(10)  # Chờ tối đa 10 giây cho trang tải
        
        # Lấy các kết quả
        max_results = 100  # Số kết quả tối đa bạn muốn lấy
        num_results = 0
        scroll_pause_time = 2  # Thời gian chờ giữa mỗi lần cuộn trang (giây)
        
        # Đánh dấu vị trí hiện tại
        previous_scroll_y = driver.execute_script('return window.scrollY')
        print(f'previous_scroll: {previous_scroll_y}')
        
        # Tạo keyword cho lần chạy tiếp theo
        exclude_domain = keyword
        print('exclude_domain')
        no_more_domain = True
        while num_results < max_results:
            search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

            for result in search_results:
                try:
                    url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc
                    if domain not in unique_domains:
                        file.write(f'{domain}\n')
                        unique_domains.add(domain)
                        exclude_domain += f' -site:{domain}'
                        no_more_domain = False
                        domain_count += 1
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
            print(f'current_scroll: {current_scroll_y}')
            if current_scroll_y == previous_scroll_y:
                no_scroll = True
                break
            previous_scroll_y = current_scroll_y
        if (no_scroll == True and  num_results <= max_results and no_more_domain == True) or (domain_count >= 5):
            print('TH1')
            time.sleep(10)
            break
        else:
            print('append_search_keyword')
            search_keywords.append(exclude_domain)
print(search_keywords)
# Đóng trình duyệt
driver.quit()

