from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Khởi tạo trình duyệt WebDriver
driver = webdriver.Chrome()

# Mở trang Google
driver.get('https://www.google.com')

# Tìm kiếm keyword
search_box = driver.find_element_by_name('q')
search_keyword = 'casino site:*.tphcm.gov.vn -site:vanphonghvcb.tphcm.gov.vn -site:duongdaynong.tphcm.gov.vn -site:tcip.tphcm.gov.vn -site:gdnn.tphcm.gov.vn'
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)

# Chờ cho trang tải
driver.implicitly_wait(10)  # Chờ tối đa 10 giây cho trang tải

# Lấy các kết quả
search_results = driver.find_elements_by_css_selector('div.g')

for result in search_results:
    try:
        title = result.find_element_by_css_selector('h3').text
        url = result.find_element_by_css_selector('a').get_attribute('href')
        print(f'Title: {title}')
        print(f'URL: {url}')
        print('-' * 30)
    except Exception as e:
        print(f"Error: {str(e)}")

# Đóng trình duyệt
driver.quit()
