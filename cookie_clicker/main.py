from datetime import datetime
from datetime import timedelta
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

# # --- WEBDRIVER SETUP ---
chromium_driver = os.getenv("CHROMIUM_DRIVER")
service = Service(chromium_driver)
driver = webdriver.Chrome(service=service)

url = 'http://orteil.dashnet.org/experiments/cookie/'
driver.get(url)

# --- DATA CONFIG ---
cookie = driver.find_element(By.ID, 'cookie')
inventory = driver.find_elements(By.CSS_SELECTOR, "#store div")
inventory_dict = {}
for n in inventory:
	award = n.text
	if award:
		split_award = award.split(' - ')
		item_id = n.get_attribute('id')
		price = split_award[1].split('\n')[0].replace(',', '')
		inventory_dict[price] = item_id

# --- TIME CONFIG ---
# 5 minutes loop
future_time = datetime.now() + timedelta(minutes=5)
# 5 secs interval - check 'cookie_count' to purchase items
timeout = time.time() + 5

# --- MAIN ---
while datetime.now() < future_time:
	cookie.click()
	if time.time() > timeout:
		money = driver.find_element(By.ID, 'money').text
		if "," in money:
			money = money.replace(",", "")

		cookie_count = int(money)

		highest = max([int(key) for (key, value) in inventory_dict.items() if cookie_count > int(key)])
		retrieved_item = inventory_dict[str(highest)]
		item_to_purchase = driver.find_element(By.ID, retrieved_item)
		item_to_purchase.click()

		timeout = time.time() + 5


cookie_per_sec = driver.find_element(By.ID, "cps").text
print(cookie_per_sec)

driver.quit()
