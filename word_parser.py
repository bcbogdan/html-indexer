#!/usr/bin/env python

from nltk.corpus import wordnet, stopwords
from nltk.corpus.reader import NOUN
from nltk.stem import SnowballStemmer


class WordParser(object):
    def __init__(self, special_words_file, stop_words_file=None, language='english', word_length=3):
        self.stemmer = SnowballStemmer(language)
        if not stop_words_file:
            self.stop_words = set(stopwords.words(language))
        else:
            self.stop_words = self.create_words_list(stop_words_file)

        self.special_words = self.create_words_list(special_words_file)
        self.word_length = word_length

    @staticmethod
    def create_words_list(input_file):
        result = []
        with open(input_file, 'r') as words:
            for word in words:
                result.append(word.strip())
        return result

    def normalize(self, word, noun=True):
        word = str(self.stemmer.stem(word))

        # check if word is noun
        if noun and len(wordnet.synsets(word, NOUN)) > 0:
            return word.lower()
        else:
            return False

    def __call__(self, word):
        if len(word) <= 3:
            return False
        elif word.isdigit():
            return False
        elif word in self.special_words:
            return word
        else:
            word = word.lower()
            if word in self.stop_words:
                return False
            else:
                return self.normalize(word)
