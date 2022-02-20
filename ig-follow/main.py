from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

CHROMIUM_DRIVER = os.getenv("CHROMIUM_DRIVER")
IG_USER = os.getenv('IG_USER')
IG_PW = os.getenv('IG_PW')
IG_TARGET = os.getenv('IG_TARGET')

class InstaFollower:
	def __init__(self, chromedriver):
		service = Service(chromedriver)
		self.driver = webdriver.Chrome(service=service)

	def findXPath(self, xpath):
		return self.driver.find_element(By.XPATH, xpath)


	def login(self):
		url = 'https://www.instagram.com/'
		self.driver.get(url)
		time.sleep(2)
		username = self.findXPath('//*[@id="loginForm"]/div/div[1]/div/label/input')
		time.sleep(2)
		username.send_keys(IG_USER)
		time.sleep(2)
		pw = self.findXPath('//*[@id="loginForm"]/div/div[2]/div/label/input')
		time.sleep(2)
		pw.send_keys(IG_PW)
		time.sleep(2)
		pw.send_keys(Keys.ENTER)

	def find_followers(self):
		time.sleep(5)
		self.driver.get(f"https://www.instagram.com/{IG_TARGET}")
		time.sleep(2)
		followers = self.findXPath('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]/a/div')
		time.sleep(1)
		followers.click()

	def follow(self):
		time.sleep(5)
		follow_count = 0
		modal = self.findXPath('/html/body/div[6]/div/div/div/div[2]')
		time.sleep(1)
		for i in range(2):
			self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
			time.sleep(3)

		follow_btn_li_list = self.driver.find_elements(By.CSS_SELECTOR, '.PZuss li button')
		print(len(follow_btn_li_list))
		for btn in follow_btn_li_list:
			try:
				btn.click()
				time.sleep(2)
				follow_count += 1
				print(follow_count)
			except ElementClickInterceptedException:
				cancel_unfollow = self.findXPath('/html/body/div[7]/div/div/div/div[3]/button[2]')
				cancel_unfollow.click()
				print('has followed')
				# time.sleep(2)

	def unfollow_all(self):
		time.sleep(5)
		self.driver.get(f"https://www.instagram.com/{IG_USER}")
		time.sleep(3)
		following = self.findXPath('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[3]/a')
		time.sleep(2)
		following.click()
		time.sleep(5)
		modal = self.findXPath('/html/body/div[6]/div/div/div/div[2]')
		time.sleep(1)
		#fixed at 2 scrolls for now
		for i in range(2):
			self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
			time.sleep(3)

		unfollow_count = 0
		follow_btn_li_list = self.driver.find_elements(By.CSS_SELECTOR, '.PZuss li button')
		print(len(follow_btn_li_list))
		for idx, btn in enumerate(follow_btn_li_list):
			print('idx:', idx)
			try:
				print('idx in try:', idx)
				btn.click()
				time.sleep(1)
			except ElementClickInterceptedException:
				print('idx in Except:', idx)
				unfollow = self.findXPath('/html/body/div[7]/div/div/div/div[3]/button[1]')
				unfollow.click()
				unfollow_count += 1
				print('unfollowed:', unfollow_count)
				time.sleep(2)




bot = InstaFollower(CHROMIUM_DRIVER)
bot.login()
bot.find_followers()
bot.follow()
# bot.unfollow_all()