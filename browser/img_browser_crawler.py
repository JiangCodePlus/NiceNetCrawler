# -*- coding: utf-8 -*-
"""
@author JPlus
@created 2019/3/24
"""

import os
import shutil
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserWebCrawler(object):
    """
    Browser web crawler
    """
    # Used to convert url to html page
    __html_template = """
       <!DOCTYPE html>
       <html lang="en">
       <head>
           <meta charset="UTF-8">
       </head>
       <body>
       <img src={img_url} width="100%">
       </body>
       </html>
       """

    def __init__(self, start_url, dir_path, web_driver_path, wait_time):
        """
        Create new BrowserWebCrawler.

        :param start_url: Initial address.
        :param dir_path: Path to save.
        :param web_driver_path: Headless browser's native address.
        :param wait_time: Wait time.
        """

        self.__driver = self.__initDriver(web_driver_path)
        self.__driver.get(start_url)
        self.__driver.implicitly_wait(wait_time)  # Automatically adjust waiting time.
        self.__dir_path = self.__createDir(dir_path)
        self.__chapter_number = 1
        self.__page_number = 1

    def __createDir(self, dir_path, is_clear=True):
        """
        Create a new directory according to the name.

        :param dir_name: Directory name.
        :param is_clear: Whether to clean up the original data.
        :return: Directory path.
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        else:
            if is_clear:
                shutil.rmtree(dir_path)
                self.__createDir(dir_path)
        return dir_path

    def getDriver(self):
        return self.__driver

    def __initDriver(self, web_driver_path):
        """
        Initialize headless browser.

        :param web_driver_path: Headless browser's native address.
        :return: Headless browser instance.
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Set the browser to headless
        return webdriver.Chrome(chrome_options=chrome_options, executable_path=web_driver_path)

    def __parseImg(self, img, index):
        """
        Parse the src in the parsing element to extract the image url.

        :param img: Image element.
        :param index: Starting page number.
        :return:
        """

        # for img in images:
        href = img.get_attribute("src")
        self.__saveImg(self.__chapter_number, self.__page_number, href, index)

    def __saveImg(self, chapter_number, page_number, url, index):
        """
        Generate the a jpg file.

        :param chapter_number: Chapter number.
        :param page_number: Page number.
        :param url: Network image address.
        :param index: Number of image.
        :return:
        """
        # if BrowserWebCrawler.__html_template.format(img_url=url).encode("utf-8"):
        file_name = ".".join(["C%d-P%d__%d" % (chapter_number, page_number, index), "jpg"])
        urllib.request.urlretrieve(url, os.path.join(self.__dir_path, file_name))  # Save the url as a jpg file.

    def loopCraw(self, index=1):
        """
        Loop crawl.

        :param fun_image: The method of displaying image elements in html (you can reposition the elements after each page refresh)
        :param fun_next_book: The method of clicking in html to reach the next chapter element (ibid.)
        :param fun_next_page: The method of clicking in html to reach the next page element (ibid.)
        :param fun_is_next: It is possible to go to next chapter to judge the conditions(ibid,)
        :param index:  Number of pictures, default initial value is 1.
        :return:
        """
        while (True):  # Avoid tail recursion.
            try:
                self.__toNextPage(self.getImg(self.__driver), self.getNextPage(self.__driver), index)  # Jump to net page each time.
                index += 1
                if (self.isGoNext(self.__driver)):  # Judge if meet the conditions of the next chapter.
                    self.__toNextBook(self.getImg(self.__driver), self.getNextChapter(self.__driver), index)  # Jump to next chapter.
            except Exception as e:
                print("-----------End of Crawl----------")
                print("--Crawled-- %d chapters ,%d pages.--" % (self.__chapter_number, index))
                raise e

        # return self.loopCraw(fun_image, fun_next_book, fun_next_page, fun_is_next, index + 1) # The maximum recursion of the tail recursion is 1000. If it exceeds, the exception is reported.

    def __toNextPage(self, img_element, next_page_element, index):
        """
        The operating of each page.

        :param img_element:
        :param next_page_element:
        :param index:
        :return:
        """
        print(self.__driver.current_url)
        self.__parseImg(img_element, index)  # Parse and save image of each page.
        self.__page_number += 1  # Page number add 1.
        next_page_element.click()  # Click next page.

    def __toNextBook(self, img_element, next_chapter_element, index):
        """
        The beginning of each chapter.
        :param img_element:
        :param next_chapter_element:
        :param index:
        :return:
        """
        print(self.__driver.current_url)

        self.__parseImg(img_element, index)  # Parse and save begin image of each chapter.
        self.__chapter_number += 1  # Chapter number add 1.
        self.__page_number = 1  # Page number restored to 1.
        next_chapter_element.click()  # Click next chapter.

    def isGoNext(self, driver):
        """ Conditions of whether jump to next chapter."""
        raise NotImplementedError

    def getImg(self, driver):
        """ Element of image."""
        raise NotImplementedError

    def getNextChapter(self, driver):
        """ Jump to the elements of the next chapter."""
        raise NotImplementedError

    def getNextPage(self, driver):
        """ Jump to the elements of the next page."""
        raise NotImplementedError


class netcrawler(BrowserWebCrawler):
    def __init__(self, start_url, dir_name, web_driver_path, wait_time):
        super().__init__(start_url, dir_name, web_driver_path, wait_time)

    def isGoNext(self, driver):
        text = driver.find_elements_by_css_selector("[class = 'img_info']")[0].text
        print(text)
        return text.split("/")[0].strip("(") == text.split("/")[1].strip(")")

    def getImg(self, driver):
        return driver.find_element_by_id("images").find_elements_by_tag_name('img')[0]

    def getNextChapter(self, driver):
        return driver.find_elements_by_css_selector("[class = 'nextC']")[0]

    def getNextPage(self, driver):
        return driver.find_elements_by_css_selector("[class = 'nav-pagination']")[1]



if __name__ == "__main__":
    init_url = "https://www.manhualou.com/manhua/4907/312548.html"
    dir_path = r"C:\Users\Administrator.PC-20180314KCTP\Desktop\hyxhn"
    executable_path = r"C:\Users\Administrator.PC-20180314KCTP\AppData\Local\Programs\Python\Python36\selenium\chromedriver.exe"
    wait_time = 30
    net_work = netcrawler(init_url, dir_path, executable_path, wait_time)
    net_work.loopCraw()
