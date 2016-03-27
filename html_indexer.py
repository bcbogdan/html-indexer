#!/usr/bin/env python

from __future__ import print_function
from html_parser import HtmlParser
import os
import sys
from timeit import default_timer as timer
import multiprocessing

def navigate_folder(rootdir, parse_function, multiprocessing=False):
    for root, subfolders, files in os.walk(rootdir):
        for input_file in files:
            filename_array = os.path.splitext(input_file)
            # if filename_array[-1] is '.content':
            #     os.remove(os.path.join(root, input_file))
            if filename_array[-1] in ['.html', '.htm']:
                input_file_path = os.path.join(root, input_file)
                result_file_path = os.path.join(root,
                                                "".join([filename_array[0], '.content']))
                parse_function(input_file_path, result_file_path)


def parse_html(input_file_path, result_file_path):
    try:
        html_file = open(input_file_path)
        html_content = html_file.read()
        html_file.close()
        doc = HtmlParser(html_content, "lxml")
        doc.write_to_file(result_file_path)
    except IOError:
        print("Can not open file %s", file_path)


if __name__ == "__main__":
    result_file = 'result.txt'
    file_path = 'http/www/riw/about.html'
    start = timer()
    navigate_folder('var', parse_html)
    end = timer()

    start = timer()
    multiprocessing.Pool(2).

    print(end-start)
