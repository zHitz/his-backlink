from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import pickle
import random
import os
import logging
import datetime

def setup_logging():
    # Tắt log debug của Selenium
    selenium_logger = logging.getLogger('selenium')
    selenium_logger.setLevel(logging.WARNING)  # Đặt mức độ log cho Selenium là WARNING hoặc cao hơn

    # Cấu hình logging
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = f'/his-backlink/logs/logs_backlink_{current_date}.log'
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')
    logging.info('============================================================================')
    logging.info('Bắt đầu Step 1')

def create_base_directory():
    # Tạo đường dẫn đến thư mục /his-backlink/
    base_directory = os.path.abspath("/his-backlink")

    # Kiểm tra xem thư mục đã tồn tại chưa, nếu không tồn tại thì tạo mới
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    return base_directory

def generate_search_keywords():
    danh_sach_ky_tu = ['casino', 'sex', 'kqxs', 'porn', 'soi kèo', 'soi keo', 'football', 'nổ hũ','roulette', 'gambling', 'crypto', 'eth', 'soxo', 'bongda', 'tài xỉu', 'nhà cái']  # Thêm các ký tự còn lại vào danh sách
    gg_dork = ['', 'intext:']

    lua_chon = input("Bạn muốn tự nhập keyword (1) hay keyword sẽ được tạo random (2)? Nhập 1 hoặc 2: ")

    while lua_chon not in ["1", "2"]:
        lua_chon = input("Nhập sai. Hãy nhập lại 1 hoặc 2: ")

    lua_chon = int(lua_chon)

    search = ""
    if lua_chon == 1:
        so_luong_keywords = int(input("Nhập số lượng keyword bạn muốn (tối đa 5): "))
        if so_luong_keywords > 5:
            so_luong_keywords = 5    
        keywords = []
        for i in range(so_luong_keywords):
            keyword = input(f"Nhập keyword thứ {i + 1}: ")
            search += f"intext:{keyword} "
            if i+1 < so_luong_keywords:
                search += "| "
    else:
        so_luong_keywords = random.randint(2, 5)
        keywords_ngau_nhien = random.sample(danh_sach_ky_tu, so_luong_keywords)
        for i in range(so_luong_keywords):
            random_intext = random.sample(gg_dork, 1)
            search += f'{random_intext[0]}"{keywords_ngau_nhien[i]}" '
            if i+1 < so_luong_keywords:
                search += "| " 
    with open(os.path.join(base_directory, 'search_keyword.txt'), 'w', encoding='utf-8') as file:
        file.write(search)
        
    lua_chon_domain = input("Bạn muốn tìm kiếm cho domain (1) hay site chỉ định(subdomain) (2)? Nhập 1 hoặc 2: ")
    while lua_chon_domain not in ["1", "2"]:
        lua_chon_domain = input("Nhập sai. Hãy nhập lại 1 hoặc 2: ")

    lua_chon_domain = int(lua_chon_domain)

    if lua_chon_domain == 1:
        nhap_domain = input("Nhập Domain bạn muốn: ")
        search_keywords = [f"{search}site:*.{nhap_domain}"]
        run_step_1 = True
    else:
        nhap_subdomain = input("Nhập SubDomain bạn muốn: ")
        search_keywords = f"{search}site:{nhap_subdomain}"
        run_step_1 = False
    
    print(search_keywords)
    return search_keywords, run_step_1

def setup_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-download-notification')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.binary_location = "/usr/bin/chromium-browser"

    return options

def perform_step_1(search_keywords, run_step_1, base_directory):
    while run_step_1 is True:
        cookies_path = os.path.join(base_directory, "cookies.pkl")

        driver = webdriver.Chrome(options=options)
        logging.info('Đã mở Chrome')
        driver.maximize_window()

        unique_domains = set()
        domain_count = 0

        driver.get("http://www.google.com")

        pickle.dump(driver.get_cookies(), open(cookies_path, "wb"))

        with open(os.path.join(base_directory, 'domain_results.txt'), 'w', encoding='utf-8') as file:
            for keyword in search_keywords:
                print(f'sk: {search_keywords}')
                print(f'kw: {keyword}')
                time.sleep(5)
                search_box = driver.find_element(By.NAME, 'q')
                search_box.send_keys(keyword)
                search_box.send_keys(Keys.RETURN)
                logging.info(f'Tìm kiếm keyword: {keyword} trên Chrome (Google)')
                time.sleep(10)
                driver.implicitly_wait(10)
                
                max_results = 100 
                num_results = 0
                scroll_pause_time = 2
                previous_scroll_y = driver.execute_script('return window.scrollY')
                exclude_domain = keyword
                no_more_domain = True
                logging.info('Bắt đầu kiểm tra kết quả tìm kiếm')
                while num_results < max_results:
                    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
                    for result in search_results:
                        try:
                            url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                            parsed_url = urlparse(url)
                            domain = parsed_url.netloc
                            if domain not in unique_domains:
                                logging.info(f'Đã tìm thấy domain mới: {domain}, bắt đầu ghi kết quả vào file domain_results.txt')
                                file.write(f'{domain}\n')
                                unique_domains.add(domain)
                                exclude_domain += f' -site:{domain}'
                                no_more_domain = False
                                domain_count += 1
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
                if (no_scroll == True and  num_results <= max_results and no_more_domain == True) or (domain_count >= 5):
                    time.sleep(10)
                    logging.info('Đã thỏa điều kiện, dừng tìm kiếm')
                    break
                else:
                    search_keywords.append(exclude_domain)

        driver.quit()
        logging.info('Đóng trình duyệt')
        run_step_1 = False

if __name__ == "__main__":
    setup_logging()
    base_directory = create_base_directory()
    search_keywords, run_step_1 = generate_search_keywords()
    options = setup_webdriver()
    perform_step_1(search_keywords, run_step_1, base_directory)
