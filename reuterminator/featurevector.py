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


def create_feature_vectors(datafile, dictfile):
    parsed_data = load_and_convert_files(datafile)
    word_dict = load_and_convert_files(dictfile)
    vector = dict.fromkeys(word_dict,0)
    for item,data in parsed_data.iteritems():
        tokens = data['tokenized_body_cleaned']
        for word in tokens:
            vector[word.lower()] += 1
        parsed_data[item]['vector'] = vector





def load_and_convert_files(filename):
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    data = convert_to_utf(data)
    return data

def convert_to_utf(input):
    if isinstance(input, dict):
        return {convert_to_utf(key): convert_to_utf(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert_to_utf(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def main():
    create_feature_vectors("cleaned.json","worddict.json")

if __name__ == "__main__": main()

