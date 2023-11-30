from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from get_all_urls import get_all_urls, login
from selenium.webdriver.common.by import By
import os

program_title_xpath = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[1]/div/article/header/h1"
)
program_organization_xpath = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[1]/div/article/h2"
)
program_description_xpath = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[1]/div/article/div[1]/p"
)
program_type_xpath = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[1]/div/article/div[2]/div[1]"
)
program_disciplines_xpath = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[1]/div/article/div[2]/div[2]"
)
program_keywords_xpath = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[1]/div/article/div[2]/div[3]"
)
program_work_experience_required = (
    "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div/div[2]/ul/li[2]"
)

if __name__ == "__main__":
    options = Options()
    options.add_experimental_option("detach", True)
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    options.add_argument(f"--user-agent={my_user_agent}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    login(driver=driver, password=password, username=username)

    columns = [
        "title",
        "type",
        "description",
        "disciplines",
        "organization",
        "keywords",
        "program_work_experience_required",
        "url",
    ]

    # Load existing data from CSV or create an empty DataFrame if the file doesn't exist
    if os.path.exists("fellowships.csv"):
        df = pd.read_csv("fellowships.csv", usecols=columns)
    else:
        df = pd.DataFrame(columns=columns)

    csv_file = "fellowships.csv"

    # Get all the urls and write to file, instead of running heavy scraper
    # all_urls = get_all_urls(password=password, username=username, driver=driver)
    # with open("urls.txt", "w") as file:
    #     for url in all_urls:
    #         file.write(url + "\n")

    # Read from file
    with open("urls.txt", "r") as file:
        urls = [url.strip() for url in file]

    for url in urls:  # Remove any leading/trailing whitespace or newlines
        driver.get(url)
        try:
            title = driver.find_element(By.XPATH, value=program_title_xpath).text
        except NoSuchElementException:
            title = ""
        try:
            type = driver.find_element(By.XPATH, value=program_type_xpath).text
        except NoSuchElementException:
            type = ""
        try:
            description = driver.find_element(
                By.XPATH, value=program_description_xpath
            ).text
        except NoSuchElementException:
            description = ""
        try:
            disciplines = driver.find_element(
                By.XPATH, value=program_disciplines_xpath
            ).text
        except NoSuchElementException:
            disciplines = ""
        try:
            organization = driver.find_element(
                By.XPATH, value=program_organization_xpath
            ).text
        except NoSuchElementException:
            organization = ""
        try:
            keywords = driver.find_element(By.XPATH, value=program_keywords_xpath).text
        except NoSuchElementException:
            keywords = ""
        try:
            program_work_experience_required = driver.find_element(
                By.XPATH, value='//*[@id="fellowship-details"]/ul/li[2]'
            ).text
        except NoSuchElementException:
            program_work_experience_required = ""
        record_df = pd.DataFrame(
            [
                [
                    title,
                    type,
                    description,
                    disciplines,
                    organization,
                    keywords,
                    program_work_experience_required,
                    url,
                ]
            ],
            columns=columns,
        )
        # Append to CSV file directly, with no index
        record_df.to_csv(
            csv_file,
            mode="a",
            header=not pd.io.common.file_exists(csv_file),
            index=False,
        )

    # Rewrite the URLs file without the processed URL
    processed_urls = set(df["url"])
    remaining_urls = urls - processed_urls

    # Rewrite the urls.txt file with the remaining URLs
    with open("urls.txt", "w") as file:
        for url in remaining_urls:
            file.write(url + "\n")

    df = df.drop_duplicates(subset=columns)

    # Write the DataFrame to CSV
    df.to_csv("fellowships.csv", index=False)
