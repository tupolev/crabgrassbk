import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lib.crawler import Crawler
from lib.config import Config


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 3)

    return driver


if __name__ == "__main__":
    config = Config('conf/config.yml')
    driver = init_driver()
    crawler = Crawler(driver, config)
    driver = crawler.login()
    print("====Driver logged in====")
    crawler.gotoPages()
    time.sleep(2)
    print("====Starting backup process====")
    # create folder for backups if it doesnt exist
    backup_dir_for_now = config.dir_backup + os.path.sep + str(int(time.time()))
    if not os.path.exists(config.dir_backup):
        os.makedirs(config.dir_backup)
    if not os.path.exists(backup_dir_for_now):
        os.makedirs(backup_dir_for_now)

    links_to_crawl = crawler.getAllCreatedPagesLinks(backup_dir_for_now)
    for link in links_to_crawl:
        crawler.crawlLink(link, backup_dir_for_now)
    print("====Backup process finished====")
    time.sleep(5)
    crawler.logout()
    print("====Driver logged out====")
    driver.quit()
