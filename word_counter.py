#!/usr/bin/env python
import os


class WordCounter(object):
    def __init__(self, file_name, word_parser):
        self.file_name = file_name
        self.word = []
        self.word_dict = {}
        self.parser = word_parser
        self.word_list = []

    def write_to_file(self, file_path=False):
        if not file_path:
            file_path = "".join([
                os.path.splitext(self.file_name)[0],
                '.count'
            ])

        with open(file_path, 'w') as output_file:
            for key, value in self.word_dict.iteritems():
                output_file.write('%s %s\n' % (key, value))

    def __call__(self, write_output=True):
        with open(self.file_name) as input_file:
            while True:
                character = input_file.read(1)
                if not character:
                    break
                elif character.isalnum():
                    self.word.append(character)
                else:
                    self.word = "".join(self.word)
                    word = self.parser(self.word)
                    if word:
                        self.word_dict[word] = self.word_dict.setdefault(word, 0) + 1
                    self.word = []
        # with open(self.file_name) as input_file:
        #     for line in input_file:
        #         for word in line.strip().split():
        #             word = self.parser(word)
        #             if word:
        #                 self.word_dict[word] = self.word_dict.setdefault(word, 0) + 1

        if write_output:
            self.write_to_file()

