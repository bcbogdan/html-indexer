#!/usr/bin/env python

from __future__ import print_function
from html_parser import HtmlParser

if __name__ == "__main__":
    result_file = 'result.txt'
    file_path = 'http/www/riw/about.html'
    try:
        html_file = open(file_path)
        html_content = html_file.read()
        html_file.close()
        doc = HtmlParser(html_content, "lxml")
        doc.write_to_file('result.txt')
    except IOError:
        print("Can not open file %s", file_path)
