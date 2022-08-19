from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from Var import PASS,EMAIL
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import random


login = driver.find_element(By.XPATH, "/html/body/div[2]/header/div[2]/div/div[6]/div[1]/a")
driver.execute_script('arguments[0].click();',login )
sleep(random.randint(3,5))

txt_user = driver.find_element(By.ID, "Email")
txt_user.send_keys(EMAIL)

txt_pass = driver.find_element(By.ID, "Password")
txt_pass.send_keys(PASS)

txt_pass.send_keys(Keys.ENTER)

sleep(random.randint(3,5))

driver.close()



