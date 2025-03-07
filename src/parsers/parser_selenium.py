from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from datetime import datetime

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

chrome_options = Options()
#chrome_options.add_argument("--headless")  # не показыватть окно браузера
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path='chromedriver') 
driver = webdriver.Chrome()

def get_page_html():
    try:
        url = "https://zoon.ru/tyumen/fitness/"
        driver.get(url)
        time.sleep(3)

        while True:
            try:
                show_more_button = driver.find_element(By.CSS_SELECTOR, ".js-next-page.button-show-more")
                if show_more_button.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)  # Скроллим к кнопке
                    time.sleep(1)  
                    show_more_button.click()
                    print("Нажата кнопка 'Показать еще'...")
                    time.sleep(1)  
                else:
                    break
            except (NoSuchElementException, ElementClickInterceptedException):
                print("Кнопка 'Показать еще' не найдена или больше неактивна.")
                break
        
        return driver.page_source

    finally:
        driver.quit()

# get_page_hmtl()