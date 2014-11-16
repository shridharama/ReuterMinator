import nltk
import string
import json
from nltk import *
from nltk import corpus
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import sys
import os
import os.path
import json
import time


JUNK_WORDS = ['<','>',':',"''",'#','cc','',',','s','reuter','note','said','mln','dlr','pct']


''' Class that contains auxiliary (static) helper methods that are used by other classes '''
class PreprocessorHelper:

    @staticmethod
    def write_to_file(data, filename, indent_val = 4):
        #Converts to json and dumps the contents to a file
        with open(filename, 'w') as outfile:
            #Removing non-unicode characters from the dataset
            #self.parsed_data = unicode(self.parsed_data, errors='ignore')
            json.dump(data, outfile, indent=indent_val)
        outfile.close()

    @staticmethod
    def get_words_after_stop_word_removal(tokens):
        good_words = [w for w in tokens if w.lower() not in nltk.corpus.stopwords.words('english')]
        better_words = [w for w in good_words if w.lower() not in JUNK_WORDS]
        return better_words

    @staticmethod
    def get_stemmed_words(tokens):
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(w) for w in tokens]
        return stemmed_words

    @staticmethod
    def convert_to_utf(input):
        if isinstance(input, dict):
            return {PreprocessorHelper.convert_to_utf(key): PreprocessorHelper.convert_to_utf(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [PreprocessorHelper.convert_to_utf(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
