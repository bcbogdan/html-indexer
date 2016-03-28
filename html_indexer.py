#!/usr/bin/env python

from __future__ import print_function
from html_parser import HtmlParser
import os
from timeit import default_timer as timer
import multiprocessing
from word_counter import WordCounter
import mmh3

ROOT_FOLDER = 'var'
WORKERS = 4
STOP_WORDS = ['a','about','above','after','again','against','all','am','an','and','any','are', 'as']
SPECIAL_WORDS = ['TOM']


def path_hash(root_dir, extension):
    file_list = get_file_list(root_dir, extension)
    hash_list = []
    for file_path in file_list:
        file_name = os.path.split(file_path)[1]
        path_name = os.path.split(file_path)[0]
        hash_list.append("".join([
                         str(mmh3.hash(file_name)),
                         ' ',
                         file_name,
                         ' ',
                         path_name]
        ))
    return hash_list

def create_dictionary():
    pass


def get_file_list(rootdir, extension):
    file_list = []
    for root, subfolders, files in os.walk(rootdir):
        for input_file in files:
            filename_array = os.path.splitext(input_file)
            if filename_array[-1] in extension:
                input_file_path = os.path.join(root, input_file)
                file_list.append(input_file_path)
    return file_list


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


def count_words(input_file_path):
    try:
        counter = WordCounter(input_file_path, SPECIAL_WORDS)
        counter()
    except IOError:
        print("Can not open file %s", input_file_path)

if __name__ == "__main__":
    var = path_hash(ROOT_FOLDER, ['.html'])
    # start = timer()
    # result = get_file_list(ROOT_FOLDER, ['.html', '.htm'])
    # multiprocessing.Pool(WORKERS).map(parse_html, result, chunksize=1)
    # end = timer()
    # print(end-start)
    #
    # start = timer()
    # result = get_file_list(ROOT_FOLDER, ['.content'])
    # # for file_name in result:
    # #     count_words(file_name)
    # multiprocessing.Pool(WORKERS).map(count_words, result, chunksize=1)
    # end = timer()
    # print(end-start)
    print('something')
