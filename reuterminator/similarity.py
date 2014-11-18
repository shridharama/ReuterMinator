from preprocessorhelper import *
import string
import json
import sys
import os
import os.path
import time
import matplotlib
import math
import itertools
import copy
import random
class Similarity:
    def __init__(self, feature_type):

        self.feature_type = feature_type
        self.tryy = True
        self.transformed_feature_vector = {}
        self.jaccard_similarity_matrix = {}
        self.hashed_matrix = {}
        self.word_set = set()

    #Gets feature vector from json file and transforms it into the type {doc_id: [Set of terms/n-grams]}
    def retrieve_and_transform_transactional_feature_vector(self):
        '''
        retrieves dictionary from json file with format
        { doc_id:
            { <feature_type>:{dictionary of features for that doc_id},
              {topics: [list of topics]},
              {places: [list of places]}
            }
        }
        '''
        self.loaded_feature_vector = PreprocessorHelper.convert_to_utf(json.load(open(self.feature_type+'.json')))

        #transforms into dictionary with format {doc_id: [Set of terms/n-grams]}
        for doc_id,value in self.loaded_feature_vector.iteritems():
            self.transformed_feature_vector[doc_id] = set(value[self.feature_type].keys())
            self.word_set = self.word_set.union(value[self.feature_type].keys())
            #printing sample transformed_feature_vector
        #print self.transformed_feature_vector["1"]
        self.document_count = len(self.transformed_feature_vector)

    #initializes sim matrix with matrix(i,i) = 1.0
    def init_jaccard_similarity_matrix(self):
        #self.document_count = len(self.transformed_feature_vector)
        for i in range(self.document_count):
            s = [None]*self.document_count
            s[i] = 1.0
            self.jaccard_similarity_matrix[i] = s
        #PreprocessorHelper.write_to_file(self.jaccard_similarity_matrix,"init_similarity.json",None)

    #initialize hash matrix. m is no of docs and n is no of permutations
    def init_hash_vector(self, m, n):
        for i in range(m):
            s = ['']*n
            self.hashed_matrix[i] = s

    #populate the hash matrix
    '''hash matrix structure
        self.hashed_matrix[i][j] will give hash word for the str(i+1)th doc_id for the jth permutation
    '''
    def populate_document_hashes(self, k):
        self.init_hash_vector(len(self.transformed_feature_vector),k)
        j = 0
        word_list = list(self.word_set)
        while j < k:
            permutation = copy.copy(word_list)
            random.shuffle(permutation)
            for doc_id in self.transformed_feature_vector:
                for word in permutation:
                    if word in self.transformed_feature_vector[doc_id]:
                        self.hashed_matrix[int(doc_id)-1][j] = word
                        break
            j += 1

        PreprocessorHelper.write_to_file(self.hashed_matrix,"hashes.json")


    def populate_jaccard_similarity_matrix(self):
        self.init_jaccard_similarity_matrix()
        for i in range(self.document_count):
            for j in range(i+1,self.document_count):
                #print i,j
                jaccard_sim = self.calculate_jaccard_similarity(self.transformed_feature_vector[str(i+1)],self.transformed_feature_vector[str(j+1)])
                self.jaccard_similarity_matrix[i][j] = jaccard_sim
                self.jaccard_similarity_matrix[j][i] = jaccard_sim
        PreprocessorHelper.write_to_file(self.jaccard_similarity_matrix,"jaccard_similarity.json",None)

    def calculate_jaccard_similarity(self, setA, setB):
        #There are some documents whose term frequencies contain empty set
        if len(setA) == 0 and len(setB) == 0:
            return 0.0
        setC = setA.intersection(setB)
        return float(len(setC)) / (len(setA) + len(setB) - len(setC))


def main():
    sim_tf = Similarity("term_frequencies")

    start = time.clock()
    sim_tf.retrieve_and_transform_transactional_feature_vector()
    end = time.clock()
    print end - start, 'seconds to transform feature vectors into format easier to calculate similarities'

    start = time.clock()
    sim_tf.populate_jaccard_similarity_matrix()
    end = time.clock()
    print end - start, 'seconds to populate baseline jaccard similarity matrix'

    start = time.clock()
    sim_tf.populate_document_hashes(16)
    end = time.clock()
    print end - start, 'seconds to populate hashing matrix'


    #sim_bigram = Similarity("bigrams_pmi")
    #sim_bigram.retrieve_and_transform_transactional_feature_vector()

if __name__ == "__main__": main()
