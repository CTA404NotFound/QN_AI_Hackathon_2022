import time
import random
import csv
import os
from Var import *
from time import sleep
from tqdm import tqdm
from dotenv import load_dotenv
from selenium import webdriver
from lib2to3.pgen2 import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

count = 0
review_list = []
# number_pass = round((NUM_ITEM-65)/12)

# load_dotenv()
# PASS = os.getenv('PASS')


options = webdriver.ChromeOptions()
#Add experimental for devtools
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#Open driver full display
options.add_argument("start-maximized")
#Define brower variable
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# driver = webdriver.Chrome(executable_path="chromedriver/chromedriver", options=options)

#Open the website
driver.get(URL)

sleep(random.randint(5,10))

txt = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a")
txt.click()

sleep(random.randint(3,5))

# /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[2]/span[2]/span[2]
# /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[7]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[2]/span[1]
# /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[13]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[2]/span[1]

print(driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[7]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[1]").text)

rv = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button")
rv.click()

# /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{i}]/div/a
# /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[7]/div/a
# /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[9]/div/a

sleep(random.randint(5,10))


print("---------Load Page Success!---------")
