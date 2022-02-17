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

CHROMIUM_DRIVER = os.getenv("CHROMIUM_DRIVER")
IG_USER = os.getenv('IG_USER')
IG_PW = os.getenv('IG_PW')
IG_TARGET = os.getenv('IG_TARGET')

class InstaFollower:
	def __init__(self, chromedriver):
		service = Service(chromedriver)
		self.driver = webdriver.Chrome(service=service)

	def login(self):
		print('login')

	def find_followers(self):
		pass

	def follow(self):
		pass


bot = InstaFollower(CHROMIUM_DRIVER)
bot.login()