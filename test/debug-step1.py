from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import pickle
import random
import os

danh_sach_ky_tu = ['sex', 'kqxs', 'porn', 'soi kèo', 'soi keo', 'football', 'nổ hũ','roulette', 'gambling', 'eth', 'soxo', 'bongda', 'tài xỉu', 'nhà cái']
gg_dork = ['intext:']
so_luong_ky_tu = random.randint(1, 5)
ky_tu_ngau_nhiens = random.sample(danh_sach_ky_tu, so_luong_ky_tu)
search = ''

for kitu in ky_tu_ngau_nhiens:
    random_intext = random.sample(gg_dork, 1)
    search = search + f'| {random_intext[0]}"{kitu}" '

search_keywords = [f"{search} site:tphcm.gov.vn | site:hochiminhcity.gov.vn | site:hcmcpv.org.vn | site:thanhuytphcm.vn"]
print(f'Tạo thành công random keyword: {search}')

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

driver = webdriver.Chrome(options=options)
print('Đã mở Chrome')
driver.maximize_window()

driver.get("http://www.google.com")
print('Đã mở Google')

time.sleep(5)
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(search_keywords[0])
search_box.send_keys(Keys.RETURN)
print(f'Tìm kiếm keyword: {search_keywords[0]} trên Google')

time.sleep(10)
driver.implicitly_wait(10)

unique_domains = set()
domain_count = 0
max_results = 100
num_results = 0
scroll_pause_time = 2
previous_scroll_y = driver.execute_script('return window.scrollY')
exclude_domain = search_keywords[0]
no_more_domain = True

print('Bắt đầu kiểm tra kết quả tìm kiếm')
while num_results < max_results:
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    print(f'Số kết quả tìm thấy: {len(search_results)}')
    
    for result in search_results:
        try:
            url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            print(f'URL tìm thấy: {url}')
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            print(f'Domain: {domain}')
            if domain not in unique_domains:
                print(f'Đã tìm thấy domain mới: {domain}')
                unique_domains.add(domain)
                exclude_domain += f' -site:{domain}'
                no_more_domain = False
                domain_count += 1
            num_results += 1
        except Exception as e:
            print(f"Lỗi khi xử lý kết quả tìm kiếm: {str(e)}")
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    if num_results >= max_results:
        break
    
    current_scroll_y = driver.execute_script('return window.scrollY')
    if current_scroll_y == previous_scroll_y:
        print('Không thể cuộn thêm, dừng tìm kiếm')
        break
    previous_scroll_y = current_scroll_y

driver.quit()
print('Đóng trình duyệt')
