from __future__ import print_function
import os
import mmh3
from glob import glob
import itertools
from collections import defaultdict
from map_reduce import MapReduce


class BSBI(object):
    def __init__(self, directory_name):
        if not os.path.isdir(directory_name):
            raise TypeError('Path is not a valid directory')
        else:
            os.chdir(directory_name)
            self.files_list = glob("*.count")
            files_no = len(self.files_list)
            self.block_size = 5
            i = 0
            self.block_list = []
            for i in range(0, files_no, i+self.block_size):
                if (i + self.block_size) < files_no:
                    size = self.block_size
                else:
                    size = files_no - i - 1
                file_block = []
                for counter in range(0, size, 1):
                    file_block.append(
                        self.files_list[i+counter]
                    )
                self.block_list.append(file_block)
        self.parsed_blocks = []
        self.word_dict = {}
        self.path_dict = {}
        self.merged_bocks = defaultdict(list)

    def create_dict(self, block, create_path_dict=True, create_word_dict=True):
        for file_path in block:
            if create_path_dict:
                self.path_dict[file_path] = self.path_dict.setdefault(file_path, mmh3.hash(file_path))
            if create_word_dict:
                with open(file_path, 'r') as input_file:
                    for line in input_file:
                        items = line.strip().split(' ')
                        self.word_dict[items[0]] = self.word_dict.setdefault(items[0], mmh3.hash(items[0]))

    @staticmethod
    def parse_block(block):
        index_block = []
        for file_path in block:
            file_path_hash = mmh3.hash(file_path)
            with open(file_path, 'r') as input_file:
                for line in input_file:
                    items = line.strip().split(' ')
                    index_block.append(
                        (mmh3.hash(items[0]),
                         [file_path_hash,
                         items[1]])
                    )
        return index_block

    @staticmethod
    def bsbi_invert(block, direct_index=False):
        reverse_index_dict = defaultdict(list)
        direct_index_dict = defaultdict(list)
        # sorting
        block.sort(key=lambda item: (item[0], item[1][0]))

        # creating reverse index
        for word_id, counter_tuple in block:
            file_id = counter_tuple[0]
            counter = counter_tuple[1]
            reverse_index_dict[word_id].append((file_id, counter))

        if direct_index:
            for word_id, counter_tuple in block:
                file_id = counter_tuple[0]
                counter = counter_tuple[1]
                direct_index_dict[file_id].append((word_id, counter))

        return reverse_index_dict, direct_index_dict

    @staticmethod
    def write_to_file(file_path, word_map):
        with open(file_path, 'w') as output_file:
            for key, values in word_map.iteritems():
                output_file.write('%s' % key)
                if type(values) is list:
                    output_file.write('\n')
                    for pairs in values:
                        output_file.write('%s %s\n' % (pairs[0], pairs[1]))
                else:
                    output_file.write(' %s\n' % values)

    def merge_blocks(self):
        pass

    def __call__(self, output_folder, direct_index=True):
        #creating <wordid, docid> list
        index_block = []
        for block in self.block_list:
            self.create_dict(block, create_path_dict=True, create_word_dict=True)
            index_block.append(self.parse_block(block))

        reverse_dict_list = []
        #sorting
        for block in index_block:
            reverse_dict_list.append(self.bsbi_invert(block, True))

        reverse_index_map = defaultdict(list)
        direct_index_map = defaultdict(list)
        for reverse_dict, direct_dict in reverse_dict_list:
            for word_id, file_tuple in reverse_dict.iteritems():
                reverse_index_map[word_id].extend(itertools.chain(file_tuple))
            if direct_index:
                for file_id, word_tuple in direct_dict.iteritems():
                    direct_index_map[file_id].extend(itertools.chain(word_tuple))

        self.write_to_file(
            os.path.join(output_folder, 'word_dictionary.txt'),
            self.word_dict
        )
        self.write_to_file(
            os.path.join(output_folder, 'path_dictionary.txt'),
            self.path_dict
        )
        self.write_to_file(
            os.path.join(output_folder, 'reverse_index.txt'),
            reverse_index_map
        )
        self.write_to_file(
            os.path.join(output_folder, 'direct_index.txt'),
            direct_index_map
        )
