from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

options = webdriver.ChromeOptions()

#chrome headless option
options.add_argument('headless')

# set the window size
options.add_argument('window-size=1200x600')

# initialize the driver
driver = webdriver.Chrome(options=options)

#to to url
driver.get('https://en.wikipedia.org/wiki/HMAC')
#driver.get('https://en.wikipedia.org/wiki/Donald_Trump')

total_width = driver.execute_script("return document.body.offsetWidth")
total_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(total_width, total_height)

#take a screenshot of the page
driver.get_screenshot_as_file('full-page.png')

driver.close()
