from threading import Thread
import time
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service

from dotenv import dotenv_values
config = dotenv_values(".env")

class Bot(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(service=Service('./geckodriver'), options=opts)
        driver.get(self.url)
        driver.add_cookie({'name' : 'username', 'value' : config["ADMINUSERNAME"]})
        driver.add_cookie({'name' : 'password', 'value' : config["ADMINPASSWORD"]})
        # future admin stuff requires those cookies (to delete bad stuff)
        # will implement AI to check for inappropriate stuff
        driver.get(self.url)
        time.sleep(20)
        driver.quit()