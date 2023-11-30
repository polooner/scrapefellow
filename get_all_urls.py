import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
import time


# XPaths
original_website_atag_xpath = "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div/a[1]"
program_discipline_filter_xpath = (
    "/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/ul/li/input"
)


# Credentials
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)

# XPaths
program_discipline_filter_xpath = (
    "/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/ul/li/input"
)


def login(username: str, password: str, driver: webdriver.Chrome):
    driver.get("https://www.profellow.com/log-in/")
    driver.find_element(By.NAME, "input_1").send_keys(username)
    driver.find_element(By.NAME, "input_2").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()


def set_filters(driver: webdriver.Chrome):
    driver.find_element(
        By.XPATH,
        value=program_discipline_filter_xpath,
    ).click()
    time.sleep(1)
    driver.find_element(
        By.XPATH,
        value="/html/body/div/div[1]/div[1]/form/div/div[1]/div[3]/div[4]/div[2]/div/ul/li[10]",
    ).click()
    driver.find_element(
        By.XPATH,
        value=program_discipline_filter_xpath,
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
            value=f"/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div[3]/div[2]/div/ul/li[{i}]",
        ).click()


def get_fellowship_url(num: int, driver: webdriver.Chrome):
    try:
        return driver.find_element(
            By.XPATH,
            value=f"/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[2]/div[{num}]/h2/a",
        ).get_attribute("href")
    except NoSuchElementException:
        return


def get_organization_url(driver: webdriver.Chrome):
    try:
        return driver.find_element(
            By.XPATH, value="/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div/a[1]"
        ).get_attribute("href")
    except NoSuchElementException:
        return


def get_listings_number(driver: webdriver.Chrome):
    num = driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[1]/div/div[1]/span",
    ).text
    return int(num.strip(","))


def loop_until_no_result(urls, driver: webdriver.Chrome):
    curr_idx = 1
    while get_fellowship_url(curr_idx, driver) is not None:
        urls.append(get_fellowship_url(curr_idx, driver))
        curr_idx += 1


def click_next_button(driver: webdriver.Chrome):
    try:
        driver.find_element(
            By.XPATH,
            value="/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[3]/ul/li[2]/a",
        ).click()
    except ElementNotInteractableException:
        return


def get_all_urls(username: str, password: str, driver: webdriver.Chrome):
    arr = []

    login(username=username, password=password, driver=driver)
    set_filters(driver=driver)
    time.sleep(2)
    total_listings = get_listings_number(driver=driver)

    # because a page shows 50 listings, number_of_loops determined by dividing total
    number_of_loops = math.ceil(total_listings / 50)
    print(number_of_loops)
    for i in range(6):
        # FIXME: running hardcoded 6 times because the number of
        # total results only updates on page 2 for some reason
        print("--------------loop: ", i)
        loop_until_no_result(urls=arr, driver=driver)
        click_next_button(driver=driver)
        driver.implicitly_wait(5)

    return arr
