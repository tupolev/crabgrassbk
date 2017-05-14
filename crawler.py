import time
from yaml import load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 3)

    return driver


def login(driver, username: str, password: str):
    driver.get("https://we.riseup.net/")
    driver.wait.until(EC.presence_of_all_elements_located)
    driver.wait.until(EC.presence_of_element_located((By.NAME, 'login'))).send_keys(username)
    driver.wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(password)
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#entry > div.buttons > input'))).click()
    time.sleep(5)

    return driver


def logout(driver):
    driver.get("https://we.riseup.net/me")
    driver.wait.until(EC.presence_of_all_elements_located)
    driver.wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, '#menu > ul.nav.navbar-nav.navbar-right > li > form > input.btn.btn-link.tab'
    ))).click()

    return driver


def gotoPages(driver):
    driver.get("https://we.riseup.net/groups/opb/pages#")
    driver.wait.until(EC.presence_of_all_elements_located)
    # time.sleep(5)

    return driver


def getAllCreatedPagesLinks(driver):
    total_link_list = []
    next_link_container = driver.find_element_by_xpath('//*[@id="search_results"]/section/ul/li[last()]')
    classes = next_link_container.get_attribute("class")
    time.sleep(2)

    while classes.find("disabled") < 0:
        partial_list = driver.find_elements_by_xpath(
            '//*[@id="search_results"]/section/table/tbody/tr/td[contains(@class, "title")]/a'
        )
        for item in partial_list:
            total_link_list.append(item.get_attribute('href'))

        next_link_container = driver.find_element_by_xpath('//*[@id="search_results"]/section/ul/li[last()]')
        classes = next_link_container.get_attribute("class")
        print("a clickear")

        driver.find_element_by_xpath('//*[@id="search_results"]/section/ul/li[last()]/a').click()
        time.sleep(2)
    return total_link_list


def crawlLink(driver, link: str):
    driver.get(link)
    driver.wait.until(EC.presence_of_all_elements_located)
    source = driver.page_source
    #create folder for page
        #create img subfolder for images
        #find images in source
        #download and store images in folder img
        #replace image paths with stored path within page source
    #save page source


if __name__ == "__main__":
    with open('config.yml', 'r') as f:
        init_config = load(f)

    driver = init_driver()
    driver = login(driver, init_config['config']['riseup']['username'], init_config['config']['riseup']['password'])
    # gotoHome(driver)
    gotoPages(driver)
    time.sleep(2)

    links_to_crawl = getAllCreatedPagesLinks(driver)
    for link in links_to_crawl:
        crawlLink(driver, link)

    time.sleep(5)
    logout(driver)
    driver.quit()
