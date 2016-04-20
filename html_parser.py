#!/usr/bin/env python
# *-* coding: UTF-8 *-*

from __future__ import print_function
from bs4 import BeautifulSoup
import re


FILTER = ['style', 'script', '[document]', 'head', 'title']


class HtmlParser(object):
    def __init__(self, html_content, parser_type="lxml"):
        self.html = BeautifulSoup(html_content.decode('utf-8', 'ignore'), parser_type)
        self.text_content = []
        self.links = []
        self.meta = []

    def get_links(self):
        for link in self.html.find_all('a'):
            print(link.get('href'))

    def get_meta(self):
        for meta in self.html.find_all('meta'):
            print(meta.get('name'))

    def get_text_content(self, output_file=False):
        text = self.html.findAll(text=True)
        for item in text:
            if self.filter_content(item, FILTER):
                if output_file:
                    output_file.write(item.encode('utf-8'))
                else:
                    self.text_content.append(item)

    def write_to_file(self, file_name):
        try:
            output_file = open(file_name, 'w+')
            self.get_text_content(output_file)
            output_file.close()
        except IOError:
            print('cannot open file')

    @staticmethod
    def filter_content(element, filter_list):
        if element.parent.name in filter_list:
            return False
        elif re.match('<!--.*-->', element):
            return False
        elif element == '\n':
            return False
        return True
