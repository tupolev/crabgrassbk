import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lib.crawler import Crawler
from lib.config import Config


def init_driver(config: Config):
    driver = webdriver.PhantomJS(executable_path=config.phantomjs_bin_path)
    driver.wait = WebDriverWait(driver, 1)

    return driver


if __name__ == "__main__":
    config = Config('conf/config.yml')
    driver = init_driver(config)
    crawler = Crawler(driver, config)
    crawler.login()
    print("====Driver logged in====")
    print("====Starting backup process====")
    crawler.goto_pages()
    time.sleep(2)
    # create folder for backups if it doesnt exist
    backup_dir_for_now = config.dir_backup + os.path.sep + str(int(time.time()))
    if not os.path.exists(config.dir_backup):
        os.makedirs(config.dir_backup)
    if not os.path.exists(backup_dir_for_now):
        os.makedirs(backup_dir_for_now)

    links_to_crawl = crawler.get_all_created_pages_links()
    for link in links_to_crawl:
        crawler.crawl_link(link, backup_dir_for_now)
    print("====Backup process finished====")
    time.sleep(1)
    crawler.logout()
    print("====Driver logged out====")
    driver.quit()
