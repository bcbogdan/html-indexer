#!/usr/bin/env python

from __future__ import print_function
from html_parser import HtmlParser
import os
from timeit import default_timer as timer
import multiprocessing

ROOT_FOLDER = 'var'
WORKERS = 4


def get_file_list(rootdir):
    html_list = []
    for root, subfolders, files in os.walk(rootdir):
        for input_file in files:
            filename_array = os.path.splitext(input_file)
            if filename_array[-1] in ['.html', '.htm']:
                input_file_path = os.path.join(root, input_file)
                html_list.append(input_file_path)
    return html_list


def parse_html(input_file_path):
    result_file_path = "".join([os.path.splitext(input_file_path)[0], '.content'])
    try:
        html_file = open(input_file_path)
        html_content = html_file.read()
        html_file.close()
        doc = HtmlParser(html_content, "lxml")
        doc.write_to_file(result_file_path)
    except IOError:
        print("Can not open file %s", input_file_path)


if __name__ == "__main__":
    start = timer()
    result = get_file_list(ROOT_FOLDER)
    multiprocessing.Pool(WORKERS).map(parse_html, result, chunksize=1)
    end = timer()

    print(end-start)
