from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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


def get_fellowship_name(num: int):
    print(
        driver.find_element(
            By.XPATH,
            value=f"/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[2]/div[{num}]/h2/a",
        ).text
    )


def get_listings_number():
    elements = driver.find_elements(By.CLASS_NAME, value="listing")
    return len(elements)


def click_next_button():
    driver.find_element(
        By.XPATH,
        value="/html/body/div[1]/div[1]/div[1]/form/div/div[2]/div[3]/ul/li[2]/a",
    ).click()


if __name__ == "__main__":
    login(username=usernameid, password=passwordpin)
    set_filters()
    time.sleep(2)
    for i in range(1, 51):
        get_fellowship_name(i)
    click_next_button()
    time.sleep(1)
    driver.quit()


# progtype: list[str], diciplines: list[str], location: list[str], citizenship: list[str],
# workxp: list[str]
