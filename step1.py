from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import pickle

search_keywords = ['"roulette" | "nổ hũ" | intext:"casino" | "sex" | "soi-keo" | "gambling" site:*.tphcm.gov.vn | site:*.hochiminhcity.gov.vn']

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--ignore-ssl-errors')  # Ignore SSL errors
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-download-notification')
options.add_argument('--disable-blink-features=AutomationControlled')
options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)
driver.maximize_window()

unique_domains = set()
domain_count = 0

driver.get("http://www.google.com")
pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))


with open('domain_results.txt', 'w', encoding='utf-8') as file:
    for keyword in search_keywords:

        time.sleep(5)
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(120)

        driver.implicitly_wait(10)  # Chờ tối đa 10 giây cho trang tải
        
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

