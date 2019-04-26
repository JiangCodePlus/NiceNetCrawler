import logging
import re

import requests
from bs4 import BeautifulSoup

from NiceNetCrawler.requests.requests_crawler import RequestCrawler

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
option = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10, }
class Test(RequestCrawler):
    def __init__(self, name, start_url, dir_path):
        super().__init__(name, start_url, dir_path)


    def parseUrl(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        ul = soup.find_all(class_= re.compile("(article-content)(.*)"))[0].ul
        for a in ul.find_all('a'):
            yield a.text, a['href']

    def parseContent(self, response):
        try:
            soup = BeautifulSoup(response.content, "lxml")
            body = soup.find_all(class_="article-content")[0]
            code_divs = soup.find_all(class_=re.compile("(crayon-syntax crayon-theme-github)(.*)"))
            for code_div in code_divs:
                code_div.replace_with(code_div.find(class_=re.compile("(crayon-main)(.*)")))

            # 通过字符串进行正则匹配需要注意空格也是包含在内的
            pattern = "(<img.*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith("http"):
                    data = "".join([m.group(1), "http:", m.group(2), m.group(3)])
                else:
                    data = "".join([m.group(1), m.group(2), m.group(3)])
                return data

            modify_img = re.compile(pattern).sub(func, str(body))
            # 利用占位符｛content｝,将读取的信息修改编码方式为utf-8
            html2 = html_template.format(content=modify_img).encode("UTF-8")
            return html2
        except Exception as e:
            logging.error("解析错误", exc_info=True)


if __name__ =="__main__":
    test = Test("Python3网络爬虫开发实战", "https://cuiqingcai.com/5052.html", r"D:\python\project\NetCrawler\file\Python3网络爬虫开发实战")
    test.run(r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe", option, header)
