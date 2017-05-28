#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lib.crawler import Crawler
from lib.config import Config
from lib.zip import Zip


def init_driver(config_instance: Config):
    drv = webdriver.PhantomJS(executable_path=config_instance.phantomjs_bin_path)
    drv.wait = WebDriverWait(drv, 1)

    return drv


if __name__ == "__main__":
    # init config object and driver
    config = Config('conf/config.yml')
    driver = init_driver(config)
    crawler = Crawler(driver, config)

    print("====Driver logging in====")
    crawler.login()
    print("====Driver logged in====")

    print("====Starting backup process====")
    # head driver to pages section
    crawler.goto_pages()
    time.sleep(2)

    # create folder for backups if it doesnt exist
    current_datetime = time.strftime('%d%m%Y%H%M%S')
    backup_dir_for_now = config.dir_backup + os.path.sep + current_datetime
    if not os.path.exists(config.dir_backup):
        os.makedirs(config.dir_backup)
    if not os.path.exists(backup_dir_for_now):
        os.makedirs(backup_dir_for_now)

    # navigate through paginated results and retrieve all page links to fetch
    links_to_crawl = crawler.get_all_created_pages_links()

    # fetch pages
    max_iterations = config.max_iterations_in_demo_mode
    counter = 0
    for link in links_to_crawl:
        if config.demo_mode and counter == max_iterations:
            print("====DEMO MODE. Stopping at 5 links====")
            break
        crawler.crawl_link(link, backup_dir_for_now)
        counter += 1
    print("====Backup process finished====")
    time.sleep(1)

    # logout driver
    print("====Driver logging out====")
    crawler.logout()
    print("====Driver logged out====")

    # close driver connection
    driver.quit()

    # dump backup in a zip file
    print("====Packing backup in ", backup_dir_for_now + os.extsep + 'zip', " ====")
    Zip.zipdir(backup_dir_for_now, backup_dir_for_now + os.extsep + Zip.ZIP_EXTENSION)
    print("====Packed backup====")

    # delete backup folder and leave only zip file in backup root folder
    print("====Deleting backup source folder ", backup_dir_for_now, " ====")
    shutil.rmtree(backup_dir_for_now)
    print("====Deleted backup source folder ", backup_dir_for_now, " ====")
