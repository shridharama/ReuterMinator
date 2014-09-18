from reuterssgmlparser import *
import nltk
import string
import json
from collections import OrderedDict
from nltk import *
from nltk import corpus
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import sys
import os
import os.path


class Preprocessor:
    def __init__(self, parser):
        self.parser = parser
        self.parsed_data = {}
        self.word_dict = {}
        #self.data_set_directory = d

    def get_parsed_data(self):
        print 'Retrieving parsed data from datasets'
        self.parser.parse_all_docs()
        self.parsed_data = self.parser.get_parsed_dataset()
        #return self.parsed_data

    def remove_stop_words(self, tokens):
        JUNK_WORDS = ['<','>',':',"''",'#','cc','',',','s','reuter','note']
        good_words = [w for w in tokens if w.lower() not in nltk.corpus.stopwords.words('english')]
        better_words = [w for w in good_words if w.lower() not in JUNK_WORDS]
        return better_words

    def stem_words(self, tokens):
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(w) for w in tokens]
        return stemmed_words

    def clean_data(self):
        for item,data in self.parsed_data.iteritems():
            print "cleaning "+ item
            body = data['body']
            body = body.replace("-", " ")
            #tokens = nltk.word_tokenize(body.translate(None, string.punctuation))
            tokenizer = RegexpTokenizer(r'[A-Za-z\-]{2,}')
            tokens = tokenizer.tokenize(body)
            words_without_stopwords = self.remove_stop_words(tokens)
            words_stemmed = self.stem_words(words_without_stopwords)
            #print better_words
            self.parsed_data[item]['body_clean'] = words_stemmed
            self.parsed_data[item]['body'] = ''

    #creates dictionary of words
    def create_word_dict(self):
        for item,data in self.parsed_data.iteritems():
            print "Updating words from "+item
            tokens = data['body_clean']
            for word in tokens:
                if word.lower() in self.word_dict.keys():
                    self.word_dict[word.lower()] += 1
                else:
                    self.word_dict[word.lower()] = 1
        print "sorting dict"
        self.word_dict = OrderedDict(sorted(self.word_dict.items(), key=lambda t: t[1], reverse = True))




def main():
    preprocessor = Preprocessor(ReutersSGMLParser())
    parsed_data = preprocessor.get_parsed_data()
    preprocessor.clean_data()
    preprocessor.create_word_dict()
    file = open("docdatadump.json", "w")
    file.write(json.dumps(preprocessor.parsed_data, indent=4))
    file.close()
    file = open("worddumplist.json", "w")
    file.write(json.dumps(preprocessor.word_dict.items(), indent=4))
    file.close()
    file = open("worddumpdict.json", "w")
    file.write(json.dumps(preprocessor.word_dict, indent=4))
    file.close()


if __name__ == "__main__": main()
