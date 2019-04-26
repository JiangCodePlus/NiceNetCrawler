# -*- coding: utf-8 -*-
"""
@author JPlus
@created 2019/4/25
"""
from NiceNetCrawler.browser.img_crawler import BrowserWebCrawler


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
    init_url = "https://www.manhualou.com/manhua/5926/197640.html"
    dir_path = r"C:\Users\Administrator.PC-20180314KCTP\Desktop\yqcr"
    executable_path = r"C:\Users\Administrator.PC-20180314KCTP\AppData\Local\Programs\Python\Python36\selenium\chromedriver.exe"
    wait_time = 30
    net_work = netcrawler(init_url, dir_path, executable_path, wait_time)
    net_work.loopCraw()
