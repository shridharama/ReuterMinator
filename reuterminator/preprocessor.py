from reuterssgmlparser import *
import nltk
from nltk import *
from nltk import corpus
import sys
import os
import os.path


class Preprocessor:
    def __init__(self, parser):
        self.parser = parser
        self.parsed_data = {}
        #self.data_set_directory = d

    def get_parsed_data(self):
        print 'Retrieving parsed data from datasets'
        self.parser.parse_all_docs()
        self.parsed_data = self.parser.get_parsed_dataset()
        #return self.parsed_data

    def remove_stop_words(self):
        for item,data in self.parsed_data.iteritems():
            body = data['body']
            tokens = nltk.word_tokenize(body)
            JUNK_WORDS = ['<','>',':',"''",'#','CC','',',']
            good_words = [w for w in tokens if w not in nltk.corpus.stopwords.words('english')]
            better_words = [w for w in good_words if w not in JUNK_WORDS]
            self.parsed_data[item]['body_clean'] = better_words

def main():
    preprocessor = Preprocessor(ReutersSGMLParser())
    parsed_data = preprocessor.get_parsed_data()
    preprocessor.remove_stop_words()

if __name__ == "__main__": main()
