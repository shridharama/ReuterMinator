from reuterssgmlparser import *
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

##
#   Each element is of the form:
#   'doc_id' = {'title': <title>, 'dateline':<dateline>, 'body': <body>, 'topics': <topics>, 'places': <places>, 'tokenized_body_cleaned': <tokenized_body_cleaned>}
#
##


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

    def get_words_after_stop_word_removal(self, tokens):
        JUNK_WORDS = ['<','>',':',"''",'#','cc','',',','s','reuter','note']
        good_words = [w for w in tokens if w.lower() not in nltk.corpus.stopwords.words('english')]
        better_words = [w for w in good_words if w.lower() not in JUNK_WORDS]
        return better_words

    def get_stemmed_words(self, tokens):
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(w) for w in tokens]
        return stemmed_words

    def clean_data(self):
        i=0
        for doc_id,doc_attributes in self.parsed_data.iteritems():
            body = doc_attributes['body']
            #tokens = nltk.word_tokenize(body.translate(None, string.punctuation))
            tokenizer = RegexpTokenizer(r'[A-Za-z\-]{2,}')
            tokenized_body = tokenizer.tokenize(body)
            words_without_stopwords = self.get_words_after_stop_word_removal(tokenized_body)
            words_stemmed = self.get_stemmed_words(words_without_stopwords)
            self.parsed_data[doc_id]['tokenized_body_cleaned'] = words_stemmed
            #deleting body as we no longer need it as we have tokenized_cleaned_body
            del doc_attributes['body']
            i+=1
            if i%1000 == 0:
                print i, 'documents have been stemmed and cleansed of stop words!'

    #creates dictionary of words
    def create_word_dict(self):
        i=0
        for item,data in self.parsed_data.iteritems():
            tokens = data['tokenized_body_cleaned']
            for word in tokens:
                if word.lower() in self.word_dict.keys():
                    self.word_dict[word.lower()] += 1
                else:
                    self.word_dict[word.lower()] = 1
            i+=1
            if i%1000 == 0:
                print i, ' documents have been checked for words!'
        self.word_dict = OrderedDict(sorted(self.word_dict.items(), key=lambda t: t[1], reverse = True))


    def write_to_file(self, data, filename):
        #Converts to json and dumps the contents to a file
        with open(filename, 'w') as outfile:
            #Removing non-unicode characters from the dataset
            #self.parsed_data = unicode(self.parsed_data, errors='ignore')
            json.dump(data, outfile, indent=4)
        outfile.close()


def main():
    preprocessor = Preprocessor(ReutersSGMLParser())

    start = time.clock()
    parsed_data = preprocessor.get_parsed_data()
    end = time.clock()
    print end - start, 'seconds to parse all documents'

    start = time.clock()

    preprocessor.clean_data()
    end = time.clock()
    print end - start, 'seconds to remove stop words and stem all bodies of documents'
    start = time.clock()
    preprocessor.create_word_dict()
    end = time.clock()
    print end - start, 'seconds to create word dictionary'
    preprocessor.write_to_file(preprocessor.parsed_data, "cleaned.json")
    preprocessor.write_to_file(preprocessor.word_dict, "worddict.json")


if __name__ == "__main__": main()
