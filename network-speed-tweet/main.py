from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

TT_EMAIL = os.getenv("TT_EMAIL")
TT_PW = os.getenv("TT_PW")
TT_USER = os.getenv("TT_USER")
CHROMIUM_DRIVER = os.getenv("CHROMIUM_DRIVER")
PROMISED_DOWN = 200
PROMISED_UP = 10

class InternetSpeedTwitterBot:
	def __init__(self, chromedriver):
		service = Service(chromedriver)
		self.driver = webdriver.Chrome(service=service)
		self.down = 0
		self.up = 0
		self.timestamp = ''

	def get_internet_speed(self):
		url = 'https://www.speedtest.net/'

		self.driver.get(url)
		current_url = self.driver.current_url
		time.sleep(1)
		go_btn = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
		time.sleep(1)
		go_btn.click()
		WebDriverWait(self.driver, 50).until(EC.url_changes(current_url))
		new_url = self.driver.current_url
		# print(new_url)
		if new_url:
			time.sleep(5)
			close_btn = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/a')
			time.sleep(1)
			close_btn.click()
			time.sleep(1)
			dl_speed = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
			time.sleep(1)
			ul_speed = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span')
			print('dl', dl_speed.text)
			print('ul', ul_speed.text)
			timestamp = datetime.now()
			formatted_timestamp = timestamp.strftime("%m/%d/%Y - %H:%M:%S")
			self.timestamp = formatted_timestamp
			self.down = int(float(dl_speed.text))
			self.up = int(float(ul_speed.text))

		# quitting here will throw error & stop webdriver for tweet_at_provider
		# self.driver.quit()

	def tweet_at_provider(self):
		url = 'https://twitter.com/i/flow/login'
		self.driver.get(url)
		time.sleep(2)

		email = self.driver.find_element(By.XPATH,
			'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]')
		time.sleep(1)
		input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]/div/input')
		time.sleep(2)
		email.click()
		time.sleep(2)
		input.click()
		time.sleep(2)
		input.send_keys(TT_EMAIL)
		time.sleep(2)

		# alternative to finding btn + click
		input.send_keys(Keys.ENTER)
		time.sleep(2)

		# button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]')
		# time.sleep(2)
		# button.click()

		username = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]')
		time.sleep(2)
		username.click()
		time.sleep(2)
		username_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
		time.sleep(2)
		username_input.click()
		time.sleep(1)
		username_input.send_keys(TT_USER)
		time.sleep(2)

		username_input.send_keys(Keys.ENTER)
		time.sleep(2)

		# username_btn = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')
		# time.sleep(1)
		# username_btn.click()

		pw_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input')
		time.sleep(1)
		pw_input.click()
		time.sleep(1)
		pw_input.send_keys(TT_PW)
		time.sleep(2)
		pw_input.send_keys(Keys.ENTER)
		time.sleep(3)

		# login_btn = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]')
		# time.sleep(1)
		# login_btn.click()

		tweet_box = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
		time.sleep(2)
		tweet_box.click()
		time.sleep(2)
		tweet_box.send_keys(f"{self.timestamp} : Actual vs Promised \nDownload speed: {self.down} vs {PROMISED_DOWN} \nUpload speed: {self.up} vs {PROMISED_UP}")
		time.sleep(2)
		submit_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
		time.sleep(2)
		submit_tweet.click()
		# self.driver.quit()

bot = InternetSpeedTwitterBot(CHROMIUM_DRIVER)
bot.get_internet_speed()
if bot.down < PROMISED_DOWN or bot.up < PROMISED_UP:
	bot.tweet_at_provider()
else:
	print('As promised.')


