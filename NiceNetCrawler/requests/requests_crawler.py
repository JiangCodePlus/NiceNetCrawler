# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
from urllib.parse import urlparse

import pdfkit
import requests


class RequestCrawler(object):
    """Use requests to request and save the page as pdf."""

    def __init__(self, name, start_url, dir_path):
        """
        Initialize RequestCrawler.

        :param name: The name of the file to save as a pdf.
        :param init_url: Get url of the url list.
        :param dir_path: The path to save html.
        """

        self.__name = name
        self.__start_url = start_url
        self.__dir_path = dir_path
        self.domain = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(start_url))

    def request(self, url, **kwargs):
        """
        Initiate a network request.

        :param url: Get content of the url .
        :param kwargs:
        :return Response of request.
        """
        return requests.get(url, **kwargs)

    def parseUrl(self, response):
        """
        Parsing the url in the url list.

        :param response:
        """
        raise NotImplementedError

    def parseContent(self, response):
        """
        Parsing the content in hte response.

        :param response:
        """
        raise NotImplementedError

    def run(self, wkhtmltopdf_path, option, header):
        """
        Run the crawler.

        :param wkhtmltopdf_path: The path where the wkhtmltopdf program is located.
        :param option: The option of pdfkit.
        :param header: Request header.
        """
        try:
            start = time.time()
            if not os.path.exists(self.__dir_path):
                os.mkdir(self.__dir_path)
            html_list = []
            url_response = self.request(self.__start_url, headers=header)
            for name, url in self.parseUrl(url_response):
                html = self.parseContent(self.request(url, headers=header))
                html_file = os.path.join(self.__dir_path, ".".join([str(name), "html"]))
                with open(html_file, "wb") as file:
                    file.write(html)
                    print("write %s: %s --> %s" % (name, url, html_file))
                if url =="https://cuiqingcai.com/5678.html":
                    break
                html_list.append(html_file)

            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            pdfkit.from_file(html_list, os.path.join(self.__dir_path, self.__name + ".pdf"), configuration=config, options= option)
            exit(0)
        except Exception as e:
            raise e
        finally:
            print(u"-------end-------\n loaded %d page，time : %.2f second " % (len(html_list), time.time() - start))
            for html in html_list:
                html_list.remove(html)
