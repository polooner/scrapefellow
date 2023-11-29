import math
import traceback
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
import time

usernameid = "liquidnewsstream@gmail.com"
passwordpin = "random123"
options = Options()
options.add_experimental_option("detach", True)

my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
options.add_argument(f"--user-agent={my_user_agent}")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

driver.get("https://www.profellow.com/log-in/")

program_discipline = ["Engineering", "Technology"]


def login(username: str, password: str):
    driver.find_element(By.NAME, "input_1").send_keys(username)
    driver.find_element(By.NAME, "input_2").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()


def set_filters():
    driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/ul/li/input",
    ).click()
    time.sleep(1)
    driver.find_element(
        By.XPATH,
        value="/html/body/div/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/div/ul/li[10]",
    ).click()
    driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/ul/li/input",
    ).click()
    driver.find_element(
        By.XPATH,
        value="/html/body/div/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/div/ul/li[8]",
    ).click()
    driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[5]/div[2]/ul/li/input",
    ).click()
    driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[5]/div[2]/div/ul/li[4]",
    ).click()
    
    # Set opportunity type
    for i in range(3, 9):
        driver.find_element(
            By.XPATH,
            value="/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[3]/div[2]/ul/li/input",
        ).click()
        driver.find_element(
            By.XPATH,
            value=f'/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[3]/div[2]/div/ul/li[{i}]',
        ).click()

def get_fellowship_url(num: int):
    try:
        return driver.find_element(
            By.XPATH,
            value=f"/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[2]/div[{num}]/h2/a",
        ).get_attribute("href")
    except NoSuchElementException:
        return


def get_listings_number():
    num = driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[1]/div/div[1]/span",
    ).text
    return int(num.strip(","))


def loop_until_no_result(urls):
    curr_idx = 1
    while get_fellowship_url(curr_idx) is not None:
        urls.append(get_fellowship_url(curr_idx))
        curr_idx += 1


def click_next_button():
    try:
        driver.find_element(
            By.XPATH,
            value="/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[3]/ul/li[2]/a",
        ).click()
    except ElementNotInteractableException:
        return


def get_all_urls(arr):
    login(username=usernameid, password=passwordpin)
    set_filters()
    time.sleep(2)
    total_listings = get_listings_number()

    number_of_loops = math.ceil(total_listings / 50)
    print(number_of_loops)
    for i in range(number_of_loops):
        print("--------------loop: ", i)
        loop_until_no_result(urls=arr)
        click_next_button()
        driver.implicitly_wait(5)

    print(urls)


if __name__ == "__main__":
    time.sleep(5)
    driver.quit()
    urls = []
    get_all_urls(urls)
    
    
    
    for i in range(len(urls)):
        
