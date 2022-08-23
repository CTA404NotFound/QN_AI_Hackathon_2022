"""
Create variables in Var.py before run code

EMAIL = "hbcqb2k@gmail.com"
PASS = ""
NUM_ITEM = 20
NUM_FIRST_PAGE = 37
# URL = "https://www.foody.vn/binh-dinh/nha-hang?CategoryGroup=food&c=nha-hang"
URL = "https://www.foody.vn/binh-dinh/food/dia-diem?q="
HEADER = [' ','Review', 'nha_hang']
PATH_SAVE = 'data_crawled/data_final_pro_2_crawl_an_uong_1_20.csv'
"""

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

load_dotenv()
PASS = os.getenv('PASS')


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

#Login to Foody
def login(driver):
    login = driver.find_element(By.XPATH, "/html/body/div[2]/header/div[2]/div/div[6]/div[1]/a")
    driver.execute_script('arguments[0].click();',login )
    sleep(random.randint(2,3))

    txt_user = driver.find_element(By.ID, "Email")
    txt_user.send_keys(EMAIL)

    txt_pass = driver.find_element(By.ID, "Password")
    txt_pass.send_keys(PASS)

    txt_pass.send_keys(Keys.ENTER)

    sleep(random.randint(3,5))
    print("---------Login Success!---------")

def load_more(driver, xpath):
    if(xpath):
        driver.execute_script('arguments[0].click();',xpath )
        print("---------Load More Review Success!---------")
        sleep(random.randint(3,5))
    else: print("Xpath not exits")

def save_data(path_save,header,data_list ):
    with open(path_save, 'w', encoding='utf-8-sig',newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write the data
        writer.writerows(data_list)
        print("---------Save Review Success!---------")

def click_to_review(link1, link2):
    if "Bình luận" in link1.text:
        link1.click()
        print("---------Load Review Success!---------")
    elif "Bình luận" in link2.text: 
        link2.click()
        print("---------Load Review Success!---------")
    else: print("---------Can't click to 'Bình luận'!---------")

#Scroll down page till end
def scroll_end_page(driver):
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    # print("---------Scroll Page Success!---------")
    sleep(random.randint(4,6))

#get current window handle
login(driver)
pwd = driver.current_window_handle
print("---------Load Page Success!---------")

for i in  range(PAGE_START, NUM_ITEM+1):
    
    # try:
        # if i == 22:
        #     continue

        #Load more item when end page
        if i%12==0:
            scroll_end_page(driver)
            try:
                load_m = driver.find_element(By.XPATH, "/html/body/div[2]/section/div/div[2]/div/div/div/div/div[2]/div[8]/a")
                # load_m.click()
                load_more(driver, load_m)
                sleep(random.randint(3,5))
                print(f"---------Load time {i}!---------")
            except:
                print("No more Items to show!")
        else: pass

        # scroll_end_page(driver)
        print(f"================== Item {i} ==================")
        #Get review
        place_link = driver.find_element(By.XPATH, f"/html/body/div[2]/section/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div/div[{i}]/div[2]/div[1]/div[2]/h2/a")
        # place_link.click()
        driver.execute_script('arguments[0].click();',place_link )
        print("---------Load Store Success!---------")
        sleep(random.randint(3,5))
        
        #Switch to second windows
        handles = []
        handles = driver.window_handles

        new_handle = handles[1] 
        driver.switch_to.window(new_handle)

        #Get number of review
        try:
            number_cmt = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/section/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[4]/div/div[2]/div[2]")
            number_cmt = int(number_cmt.text)
        except:
            print("---------!Item have no standard!---------")
            driver.close()
            driver.switch_to.window(handles[0])
            sleep(random.randint(2,3))
            continue

        #Find "Binh luan" tag
        review_link1 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div/ul/li[3]/a")
        review_link2 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div/ul/li[4]/a")

        #Click to "Binh luan"
        click_to_review(review_link1,review_link2)
        sleep(random.randint(3,5))

        scroll_end_page(driver)

        #Load more rv
        try:
            
            # # more_rv = driver.find_element(By.CLASS_NAME,"fd-btn-more")
            more_rv = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/div[2]/a")
            # load_more(driver, more_rv)
            while(more_rv):
                driver.execute_script('arguments[0].click();',more_rv )
                print("---------Load More Review Success!---------")
                sleep(random.randint(3,5))
        except:
            print("No more comments to show!")

        #Get last request parameters
        # id = driver.current_url
        # id = id.split("/")
        # # id = id[-2] + "/" + id[-1]
        # id = id[-1]

        #Get review
        for j in tqdm(range(1,number_cmt+1), desc = 'Progress Bar:'):

            #Click to "Xem them" in per review
            try:
                more_content_rv = driver.find_element(By.XPATH,f"/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/ul/li[{j}]/div[2]/div/a")
                if(more_content_rv.text =="Xem thêm"):
                    driver.execute_script('arguments[0].click();',more_content_rv )
                    # print("---------More content of comments to show!---------")
                    sleep(random.randint(1,2))
                else: pass
            except:
                print("No more content of comments to show!")

            comment = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/ul/li[{j}]/div[2]/div/span')
            #check sentiment
            try:
                sentiment = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/ul/li[{j}]/div[1]/div[2]/div[1]/span')
                sentiment = sentiment.text
            except: 
                sentiment = "0"
                print("---------No Rating to crawl!---------")
            review_list.append([count,comment.text,round(float(sentiment)/10*5)])
            count+=1
            time.sleep(0.5)
            # print("---------Get Review Success!---------")

        sleep(random.randint(3,5))
        print("---------Crawl reviews: Done!---------")
        driver.close()
        driver.switch_to.window(handles[0])
        # scroll_end_page(driver)
        sleep(random.randint(3,5))

    # except:
    #     print("---------Can't crawl this item!!---------")
    #     pass
#Close brower
driver.close()

#Save review to csv
save_data(PATH_SAVE, HEADER, review_list)

print("---------Done!---------")