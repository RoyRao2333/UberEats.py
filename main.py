import csv
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# Init web driver
DRIVER_OPTIONS = webdriver.ChromeOptions()
DRIVER_OPTIONS.headless = True
WEB_DRIVER = webdriver.Chrome(options=DRIVER_OPTIONS)


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


def wait_for_element_by_class_name(self, value):
    try:
        return WebDriverWait(self, 10).until(ec.presence_of_element_located((By.CLASS_NAME, value)))

    except WebDriverException as error:
        print(f"{type(error)}: {error}")
        return None


def find_element_by_class_name(self, class_name):
    try:
        return self.find_element(by=By.CLASS_NAME, value=class_name)

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
    results: list[list[str]] = []
    WEB_DRIVER.get(url)
    try:
        close_btn = wait_for_element_by_xpath(WEB_DRIVER, "//button[contains(@class,'ah cd')]")
        if close_btn:
            close_btn.click()
        store_name = find_element_by_xpath(WEB_DRIVER, '//h1').text
        rating_text = find_element_by_xpath(WEB_DRIVER, "(//div[@class='ah']//div)[3]").text
        address_text = find_element_by_xpath(WEB_DRIVER, "//div[contains(@class,'bx dk')]").text
        print((store_name or 'N/A'))
        results.append(['Store Name:', store_name])
        results.append(['Rating (might be none):', rating_text])
        results.append(['Address:', address_text])
    except BaseException as error:
        print(f"Finding close button failed with error {type(error)}: {error}. Trying next...")

    # TODO: 分类
    # main_menu = find_element_by_xpath(WEB_DRIVER, "//ul[contains(@class,'dh bu')]")
    # sub_menus = find_elements_by_xpath(main_menu, '//li')
    # for sub_menu in sub_menus:
    #     try:
    #         sub_menu_title = find_element_by_xpath(sub_menu, './div[1]').text
    #         sub_menu_content = find_element_by_xpath(sub_menu, '//div[3]')
    #     except BaseException as error:
    #         print(f"Finding item failed with error {type(error)}: {error}. Trying next...")

    items = find_elements_by_xpath(WEB_DRIVER, "(//div[contains(@class,'ah ai ae')])")
    for item in items:
        try:
            item_name = wait_for_element_by_class_name(item, 'ba.c4.bb.c5.ax')
            name = find_element_by_xpath(item_name, './span[1]').text
            item_info = wait_for_element_by_xpath(item, "(./div[contains(@class,'ah eh')])")
            price = find_element_by_xpath(item_info, './span[1]').text
            cal = find_element_by_xpath(item_info, './span[3]').text
            print((name or 'N/A'))
            results.append([name, price, cal])
        except BaseException as error:
            print(f"Finding item failed with error {type(error)}: {error}. Trying next...")
    return results


def write_output(path: Path, data: list[list[str]]):
    with open(path, "w", encoding="utf-8-sig") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)


def main():
    stores = read_stores()
    results_path = makedir('results')
    for url in stores:
        store_id = url.split('/')[-1]
        results = get_web_content(url)
        try:
            write_output(results_path.joinpath(f'{store_id}.csv'), results)
        except BaseException as error:
            print(f'Write output failed with error {type(error)}: {error}')


if __name__ == '__main__':
    main()
