#!/usr/bin/env python
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.corpus.reader import NOUN
from nltk.stem import SnowballStemmer


class WordCounter(object):
    def __init__(self, file_name, special_words, stop_words=False, language='english'):
        self.file_name = file_name
        if not stop_words:
            self.stop_words = set(stopwords.words('english'))
        else:
            self.stop_words = stop_words
        self.stemmer = SnowballStemmer(language)
        self.special_words = special_words
        self.word = []
        self.word_dict = {}

    def filter_word(self, word_length=3):
        if self.word.isdigit():
            return False
        elif len(self.word) <= word_length:
            return False
        elif self.word in self.special_words:
            return True
        else:
            self.word = self.word.lower()
            if self.word in self.stop_words:
                return False
            elif self.normalize(noun=True):
                return True
            else:
                return False

    def normalize(self, noun=False):
        """
        Word stemming
        - wordnet implementation
        wnl = WordNetLemmatizer()
        self.word = str(wnl.lemmatize(self.word))
        - stemmer implementation
        !!! not working for all words - example: apples
        """
        self.word = str(self.stemmer.stem(self.word))
        if noun and len(wordnet.synsets(self.word, NOUN)) > 0:
            return True
        else:
            return False

    def write_to_file(self, file_path=False):
        if not file_path:
            file_path = "".join([
                os.path.splitext(self.file_name)[0],
                '.count'
            ])

        with open(file_path, 'w') as output_file:
            for key, value in self.word_dict.iteritems():
                output_file.write('%s - %s\n' % (key, value))

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
                    if self.filter_word():
                        self.word_dict[self.word] = self.word_dict.setdefault(self.word, 0) + 1
                    self.word = []
        if write_output:
            self.write_to_file()
