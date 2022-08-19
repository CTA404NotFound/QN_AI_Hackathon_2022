from tqdm import tqdm
import time
import random
import csv
from lib2to3.pgen2 import driver
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Var import *

url = "https://www.foody.vn/binh-dinh/nha-hang?CategoryGroup=food&c=nha-hang"
header = [' ','Review', 'giai_tri']
review_list = []
count = 0
path_save = 'data_final_pro_2.csv'


options = webdriver.ChromeOptions()
#Add experimental for devtools
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#Open driver full display
options.add_argument("start-maximized")
#Define brower variable
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# brower = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")

#Open the website
driver.get(url)

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

def save_data(path_save,header,data_list ):
    with open(path_save, 'w', encoding='utf-8-sig',newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write the data
        writer.writerows(data_list)
        print("---------Save Review Success!---------")


#get current window handle
login(driver)
pwd = driver.current_window_handle
print("---------Load Page Success!---------")

 #Scroll down page till end
def scroll_end_page(driver):
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    print("---------Scroll Page Success!---------")
    sleep(random.randint(12,15))


# number_rs = driver.find_element(By.XPATH,"/html/body/div[2]/section/div/div[2]/div/div/div/div/div[2]/div[3]/div/div/div/div/span")
# number_rs = int(number_rs.text)

scroll_end_page(driver)

number_pass = round((NUM_ITEM-65)/12)
for i in  range(number_pass):
    try:
        load_m = driver.find_element(By.XPATH, "/html/body/div[2]/section/div/div[2]/div/div/div/div/div[2]/div[8]/a")
        # load_m.click()
        load_more(driver, load_m)
        sleep(random.randint(3,5))
    except:
        print("No more Items to show!")

for i in  range(1, NUM_ITEM+1):
    print(f"================== Item {i} ==================")
    #Get review
    place_link = driver.find_element(By.XPATH, f"/html/body/div[2]/section/div/div[2]/div/div/div/div/div[2]/div[5]/div[1]/div/div/div[{i}]/div[2]/div[1]/div[2]/h2/a")
    # place_link.click()
    driver.execute_script('arguments[0].click();',place_link )
    # driver.execute_script('arguments[0].click();',place_link )
    print("---------Load Store Success!---------")
    sleep(random.randint(3,5))

    handles = []
    handles = driver.window_handles

    # for handle in handles:
    #     print(handle)

    new_handle = handles[1] 
    driver.switch_to.window(new_handle)

    #Get number of review
    number_cmt = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/section/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[4]/div/div[2]/div[2]")
    number_cmt = int(number_cmt.text)

    #Click to "Binh luan"
    review_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div/ul/li[3]/a").click()
    print("---------Load Review Success!---------")
    #Stop 5s
    sleep(random.randint(3,5))

    # flag = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/ul/li[{number_cmt}]/div[2]/div")
    # driver.execute_script("arguments[0].scrollIntoView() ;", flag)
    #Scroll down page till end
    scroll_end_page(driver)

    #Load more rv
    try:
        more_rv = driver.find_element(By.CLASS_NAME,"fd-btn-more")
        load_more(driver, more_rv)
    except:
        print("No more comments to show!")
    
    # try:
    #     more_rv = driver.find_element(By.CLASS_NAME,"fd-btn-more")
    #     if(more_rv):
    #         driver.execute_script('arguments[0].click();',more_rv )
    #         print("---------Load More Review Success!---------")
    #         sleep(random.randint(3,5))
    # except:
    #     print("No more comments to show!")


    #Get review
    for j in tqdm(range(1,number_cmt+1), desc = 'Progress Bar:'):
        comment = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/ul/li[{j}]/div[2]/div/span")
        sentiment = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div/div[1]/div/ul/li[{j}]/div[1]/div[2]/div[1]/span")
        review_list.append([count,comment.text,round(float(sentiment.text)/10*5)])
        count+=1
        # print(comment.text)
        # print(round(float(sentiment.text)/10*5))
        time.sleep(0.5)
        print("---------Get Review Success!---------")

    # content = cmt_list.find_element(By.TAG_NAME,("a"))
    # print(content.text)

    sleep(random.randint(5,10))

    print("---------Done!---------")
    driver.close()
    driver.switch_to.window(handles[0])

#Close brower
driver.close()

#Save review to csv
save_data(path_save, header, review_list)

print("---------Done!---------")