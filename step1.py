from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import pickle
import random
import os  # Thêm thư viện để làm việc với đường dẫn thư mục

# Tạo đường dẫn đến thư mục /his-backlink/
base_directory = os.path.abspath("/his-backlink/")

# Kiểm tra xem thư mục đã tồn tại chưa, nếu không tồn tại thì tạo mới
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

# Danh sách chứa các ký tự
danh_sach_ky_tu = ['casino', 'sex', 'kqxs', 'porn', 'soi keo', 'football', 'nổ hũ','roulette', 'gambling']  # Thêm các ký tự còn lại vào danh sách
gg_dork = ['', 'intext:']
# Số lượng ký tự bạn muốn lấy ngẫu nhiên
so_luong_ky_tu = random.randint(1, len(danh_sach_ky_tu))  # Lấy một số ngẫu nhiên từ 1 đến độ dài của danh sách
# Lấy ký tự ngẫu nhiên
ky_tu_ngau_nhiens = random.sample(danh_sach_ky_tu, so_luong_ky_tu)
search = ''
# In ra kết quả
for kitu in ky_tu_ngau_nhiens:
    random_intext = random.sample(gg_dork, 1)
    search = search + f'| {random_intext[0]}"{kitu}" '

search_keywords = [f"{search} + 'site:tphcm.gov.vn | site:*.hochiminhcity.gov.vn'"]

# Lưu giá trị "search" vào tệp
with open("search_keyword.txt", "w", encoding='utf-8') as file:
    file.write(search)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-download-notification')
options.add_argument('--disable-blink-features=AutomationControlled')
options.binary_location = "/usr/bin/chromium-browser"

# Sử dụng đường dẫn tới thư mục /his-backlink/ để lưu cookies
cookies_path = os.path.join(base_directory, "cookies.pkl")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

unique_domains = set()
domain_count = 0

driver.get("http://www.google.com")

# Sử dụng đường dẫn tới thư mục /his-backlink/ để lưu cookies
pickle.dump(driver.get_cookies(), open(cookies_path, "wb"))

with open(os.path.join(base_directory, 'domain_results.txt'), 'w', encoding='utf-8') as file:
    for keyword in search_keywords:

        time.sleep(5)
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(120)

        driver.implicitly_wait(10)
        
        max_results = 100 
        num_results = 0
        scroll_pause_time = 2
        
        previous_scroll_y = driver.execute_script('return window.scrollY')
        
        exclude_domain = keyword
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
        if (no_scroll == True and  num_results <= max_results and no_more_domain == True) or (domain_count >= 5):
            time.sleep(10)
            break
        else:
            search_keywords.append(exclude_domain)

# Đóng trình duyệt
driver.quit()
