import os
import re
import time
import requests
from typing import Dict
from slugify import slugify
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lib.config import Config


class Crawler:
    def __init__(self, driver, config: Config):
        self.driver = driver
        self.config = config
        self.cookies = {}

    def login(self):
        self.driver.get(self.config.url)
        self.driver.wait.until(EC.presence_of_all_elements_located)
        self.driver.wait.until(EC.presence_of_element_located((By.NAME, 'login'))).send_keys(self.config.username)
        self.driver.wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(self.config.password)
        self.driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#entry > div.buttons > input'))).click()
        time.sleep(3)
        self.cookies = self.get_cookies()

        return self.driver

    def logout(self):
        self.driver.get(self.config.url + self.config.uri_me)
        self.driver.wait.until(EC.presence_of_all_elements_located)
        self.driver.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#menu > ul.nav.navbar-nav.navbar-right > li > form > input.btn.btn-link.tab'
        ))).click()

        return self.driver

    def goto_pages(self):
        self.driver.get(self.config.url + self.config.uri_pages)
        self.driver.wait.until(EC.presence_of_all_elements_located)

        return self.driver

    def get_all_created_pages_links(self):
        total_link_list = []
        next_link_container = self.driver.find_element_by_xpath('//*[@id="search_results"]/section/ul/li[last()]')
        classes = next_link_container.get_attribute("class")
        time.sleep(2)
        counter = 1
        while classes.find("disabled") < 0:
            partial_list = self.driver.find_elements_by_xpath(
                '//*[@id="search_results"]/section/table/tbody/tr/td[contains(@class, "title")]/a'
            )
            for item in partial_list:
                total_link_list.append(item.get_attribute('href'))

            next_link_container = self.driver.find_element_by_xpath('//*[@id="search_results"]/section/ul/li[last()]')
            classes = next_link_container.get_attribute("class")
            print("Fetching result page ", str(counter))
            counter += 1
            self.driver.find_element_by_xpath('//*[@id="search_results"]/section/ul/li[last()]/a').click()
            time.sleep(2)

        return total_link_list

    def crawl_link(self, link: str, output_dir: str):
        self.driver.get(link)
        self.driver.wait.until(EC.presence_of_all_elements_located)
        self.dump_page(output_dir)

    def dump_page(self, output_dir: str):
        title_start = re.search(r"<title>", self.driver.page_source[1:1500])
        title_end = re.search(r"</title>", self.driver.page_source[1:1500])
        page_title = self.driver.page_source[(title_start.start(0)+8):title_end.start(0)-1].strip()
        safe_folder_name = slugify(page_title)
        safe_file_name = slugify(page_title) + '.html'
        #create folder for page if not exists
        current_page_path = output_dir + os.sep + safe_folder_name
        if not os.path.exists(current_page_path):
            os.makedirs(current_page_path)
        #save page source
        page_source = self.dump_page_images(current_page_path + os.sep + 'images', self.driver.page_source)
        page_source = self.dump_page_attachments(current_page_path + os.sep + 'files', page_source)
        with open(current_page_path + os.sep + safe_file_name, 'w') as f:
            f.write(page_source)
        print('Dumping page ', page_title)

    def dump_page_attachments(self, output_dir: str, page_source: str) -> str:
        return page_source

    def dump_page_images(self, output_dir: str, page_source: str) -> str:
        print('--Dumping images')
        processed_page_source = page_source
        try:
            # create img subfolder for images
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # find images in source
            image_nodes = self.driver.find_elements_by_xpath("//img")
            # download and store images in folder img
            for image in image_nodes:
                src = str(image.get_attribute('src'))
                image_file_name = os.path.basename(src)
                print('Dumping image ', image_file_name)
                response = requests.get(src, cookies=self.cookies)
                output = open(output_dir + os.sep + image_file_name, "wb")
                output.write(response.content)
                output.close()

                # replace image paths with stored path within page source
                processed_page_source = processed_page_source.replace(src, 'images' + os.sep + image_file_name)
        except Exception as e:
            print(str(e))

        return processed_page_source

    def get_cookies(self) -> Dict:
        cookies = {}
        for s_cookie in self.driver.get_cookies():
            cookies[s_cookie["name"]] = s_cookie["value"]

        return cookies
