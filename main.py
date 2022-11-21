import csv
from pathlib import Path

from selenium.common import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# Init web driver
DRIVER_OPTIONS = Options()
# DRIVER_OPTIONS.headless = True
WEB_DRIVER = Firefox(options=DRIVER_OPTIONS)


def makedir(path: str) -> Path:
    folder = Path(__file__).joinpath(f'../{path}').resolve()
    if not folder.is_dir():
        folder.mkdir(parents=True, exist_ok=True)
        return folder


def read_stores():
    stores: list[str] = []
    with open('stores.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            stores.append(row[0])
    return stores


def find_element_by_xpath(self, xpath):
    try:
        return self.find_element(by=By.XPATH, value=xpath)

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return None


def find_elements_by_xpath(self, xpath):
    try:
        return self.find_elements(by=By.XPATH, value=xpath)

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return list()


def find_element_by_id(self, value):
    try:
        return self.find_elements(by=By.ID, value=value)

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return None


def wait_for_element_by_id(self, value):
    try:
        return WebDriverWait(self, 10).until(ec.presence_of_element_located((By.ID, value)))

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return None


def wait_for_element_by_xpath(self, value):
    try:
        return WebDriverWait(self, 10).until(ec.presence_of_element_located((By.XPATH, value)))

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return None


def find_elements_by_class_name(self, class_name):
    try:
        return self.find_elements(by=By.CLASS_NAME, value=class_name)

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return list()


def get_web_content(url: str):
    headers = {
        "Connection": "keep-alive",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56",
    }
    return httpx.get(url, headers=headers).text


def parse_web_content(content: str):
    print(content)


def main():
    stores = read_stores()
    for url in stores:
        store_id = url.split('/')[-1]
        makedir(f'results/{store_id}')
        WEB_DRIVER.get(url)


if __name__ == '__main__':
    main()
