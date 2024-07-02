from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

# Setup the Chrome driver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open Cookie Clicker website
driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie_id = "bigCookie"
cookies_id = "cookies"
product_price_prefix = "productPrice"
product_prefix = "product"

# Wait for the language selection to be present and click English
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)
language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

# Wait for the cookie element to be present
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)
cookie = driver.find_element(By.ID, cookie_id)

# Function to get the current number of cookies
def get_cookies_count():
    cookies_text = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
    return int(cookies_text.replace(",", ""))

# Function to fetch product price
def get_product_price(index):
    try:
        product_price_element = driver.find_element(By.ID, product_price_prefix + str(index))
        product_price = int(product_price_element.text.replace(",", ""))
        return product_price
    except (ValueError, StaleElementReferenceException):
        return None

# Function to buy a product
def buy_product(index):
    try:
        product = driver.find_element(By.ID, product_prefix + str(index))
        product.click()
    except StaleElementReferenceException:
        pass

# Main loop to click the cookie and buy products
try:
    while True:
        cookie.click()
        cookies_count = get_cookies_count()

        # Iterate over the first 4 products
        for i in range(4):
            product_price = get_product_price(i)
            if product_price is not None and cookies_count >= product_price:
                buy_product(i)
                time.sleep(0.1)  # Small delay after purchase
                break

except KeyboardInterrupt:
    print("Script stopped by user")

finally:
    driver.quit()
