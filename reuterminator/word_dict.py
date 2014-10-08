from reuterssgmlparser import *
from preprocessorhelper import *
#import nltk
import string
import json
from nltk import *
from nltk import corpus
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.collocations import *

#from nltk.book import *
import sys
import os
import os.path
import json
import time
import matplotlib
import math
import itertools
from collections import Counter
##
#   Each parsed_data key-value is of the form:
'''
{
    'doc_id' = #Refers to ID of a News Item
    {
        'title': <title>,
        'dateline':<dateline>,
        'body': <body>, #body gets deleted after cleaning
        'topics': <topics>,
        'places': <places>,
        'tokenized_body_cleaned': <tokenized_body_cleaned>
        'vector': <vector>
    }
}
'''
##
def convert_to_utf(input):
        if isinstance(input, dict):
            return {convert_to_utf(key): convert_to_utf(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [convert_to_utf(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input


total_word_list = []
tokenized_body_cleaned_dict = convert_to_utf(json.load(open('cleaned.json')))
i = 0
for doc_id,tokenized_body_cleaned_list in tokenized_body_cleaned_dict.iteritems():
    total_word_list = total_word_list + tokenized_body_cleaned_list
    i += 1
    if i%1000 is 0:
        print i
print "generating word_dict"
frequency_dist = Counter(total_word_list)
print frequency_dist
s=open('word_dict.json','w')
json.dump({tuple[0]:tuple[1] for tuple in frequency_dist.most_common(3000)}, s)
s.close()
