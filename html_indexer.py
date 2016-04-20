#!/usr/bin/env python

from __future__ import print_function
from html_parser import HtmlParser
from word_parser import WordParser
from timeit import default_timer as timer
from word_counter import WordCounter
from config import help_function
from config import BOLD
from config import END
from map_reduce import MapReduce
from bsbi import BSBI
import multiprocessing
import os
import sys

NAME = 'html_indexer'

PARSER = WordParser('special_files/specialwords.txt')


def parse_html(input_file_path):
    result_file_path = "".join([os.path.splitext(input_file_path)[0], '.content'])
    with open(input_file_path, 'r') as html_file:
        doc = HtmlParser(html_file.read(), "lxml")
        doc.write_to_file(result_file_path)


def parse_text(input_file_path):
    parser = WordCounter(input_file_path, PARSER)
    return parser()


def get_file_list(rootdir, extension):
    file_list = []
    for file_name in os.listdir(rootdir):
        if file_name.endswith(extension):
            file_list.append(
                os.path.join(rootdir, file_name)
            )
    return file_list


def parse_arguments(argument_list):
    if len(argument_list) < 3:
        if len(argument_list) == 1 and argument_list[0] == '-h':
            help_function(NAME)
            exit(1)
        else:
            print('Invalid input.\nUse - %spython %s.py -h%s - for usage help.' % (BOLD, NAME, END))
            exit(1)
    index = 0
    if '-' in argument_list[0]:
        workers = argument_list[1]
        index = 2
    else:
        workers = 4

    return argument_list[index:], workers

if __name__ == "__main__":
    start = timer()
    folder_list, workers = parse_arguments(sys.argv[1:])
    if not os.path.exists(folder_list[-1]):
        os.mkdir(folder_list[-1])

    # extract content from html
    multiprocessing.Pool(workers).map(
        parse_html,
        get_file_list(folder_list[0], '.html')
    )

    # parse and count words
    multiprocessing.Pool(workers).map(
        parse_text,
        get_file_list(folder_list[0], '.content')
    )

    # bsbi indexing
    temp_path = os.getcwd()
    index_alg = BSBI(folder_list[0])
    index_alg(
        os.path.join(
            temp_path,
            folder_list[-1]
        )
    )
    end = timer()
    print(end-start)
