from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# usernames
usernames = ["这里填入学号","这里填第二个"]

for user in usernames:
    print("This is " + user + " ready to sign")
    # simulate an inphone X and open the website
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"}) # simulate an iPhone X
    driver = webdriver.Chrome(options=options)
    driver.get("https://xsc-health.wh.sdu.edu.cn/mobile/index.html#/common/office/login")

    # get the username and password
    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
    except:
        print("I can't find username or password")
        driver.quit()

    userstr = user
    passstr = "whsdu@" + userstr 

    username.send_keys(userstr)
    password.send_keys(passstr)

    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "weui_btn_primary"))
        )
        button.click()
    except:
        print("I can't find button")
        driver.quit()

    try:
        button_sign = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swiper-wrapper"))
        )
        button_sign.click()
    except:
        print("I can't go into the sign")
        driver.quit()

    try:
        button_daka = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'提交')]"))
        )
        # I don't have a good idea about the location, just wait for 10 seconds
        time.sleep(10)
        button_daka.click()
    except:
        print("I can't da ka")
        driver.quit()
    finally:
        time.sleep(2)
        print(user + " down")
        driver.quit()

