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
import math

K_VALUES = [16,32,64,128]
#FEATURES = ["bigrams_frequencies","term_frequencies","shingles_frequencies_5"]
FEATURES = ["shingles_frequencies_3"]
EFFICIENCY = {}
EFFICACY = {}
sum_dimensionality_bigrams = 0
average_dimensionality_bigrams = 0

class Similarity:
    def __init__(self, feature_type):

        self.feature_type = feature_type
        self.transformed_feature_vector = {}
        self.jaccard_similarity_matrix = {}
        self.minhash_similarity_matrix = {}
        self.hashed_matrix = {}
        self.word_set = set()


    def reset(self):
        self.minhash_similarity_matrix = {}
        self.hashed_matrix = {}
        sum_dimensionality_bigrams = 0
        average_dimensionality_bigrams = 0

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
        sum_dimensionality_bigrams = 0
        #transforms into dictionary with format {doc_id: [Set of terms/n-grams]}
        for doc_id,value in self.loaded_feature_vector.iteritems():
            self.transformed_feature_vector[doc_id] = set(value[self.feature_type].keys())
            sum_dimensionality_bigrams += len(self.transformed_feature_vector[doc_id])
            self.word_set = self.word_set.union(value[self.feature_type].keys())
            #printing sample transformed_feature_vector
        #print self.transformed_feature_vector["1"]
        self.document_count = len(self.transformed_feature_vector)
        print 'total number of documents being compared - ', self.document_count
        print 'average_DIMENSIONALITY = ', sum_dimensionality_bigrams/self.document_count

    #initializes sim matrix with matrix(i,i) = 1.0
    def init_similarity_matrix(self,matrix):
        #self.document_count = len(self.transformed_feature_vector)
        for i in range(self.document_count):
            s = [None]*self.document_count
            s[i] = 1.0
            matrix[i] = s
        #PreprocessorHelper.write_to_file(self.jaccard_similarity_matrix,"init_similarity.json",None)

    def populate_jaccard_similarity_matrix(self):
        self.init_similarity_matrix(self.jaccard_similarity_matrix)
        for i in range(self.document_count):
            for j in range(i+1,self.document_count):
                #print i,j, self.transformed_feature_vector["1002"]
                jaccard_sim = self.calculate_jaccard_similarity(self.transformed_feature_vector[str(i+1)],self.transformed_feature_vector[str(j+1)])
                self.jaccard_similarity_matrix[i][j] = jaccard_sim
                self.jaccard_similarity_matrix[j][i] = jaccard_sim
        #PreprocessorHelper.write_to_file(self.jaccard_similarity_matrix,self.feature_type+"_jaccard_similarity.json",None)

    def calculate_jaccard_similarity(self, setA, setB):
        #There are some documents whose term frequencies contain empty set
        if len(setA) == 0 and len(setB) == 0:
            return 0.0
        setC = setA.intersection(setB)
        return float(len(setC)) / (len(setA) + len(setB) - len(setC))

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
        self.k = k
        self.init_hash_vector(len(self.transformed_feature_vector), self.k)
        j = 0
        word_list = list(self.word_set)
        while j < self.k:
            permutation = copy.copy(word_list)
            random.shuffle(permutation)
            for doc_id in self.transformed_feature_vector:
                for word in permutation:
                    if word in self.transformed_feature_vector[doc_id]:
                        self.hashed_matrix[int(doc_id)-1][j] = word
                        break
            j += 1

        #PreprocessorHelper.write_to_file(self.hashed_matrix,self.feature_type+"_hashes.json",None)

    def populate_minhash_similarity_matrix(self):
        self.init_similarity_matrix(self.minhash_similarity_matrix)
        for i in range(self.document_count):
            for j in range(i+1,self.document_count):
                common_word_count_between_i_and_j = 0
                for k in range(self.k):
                    if(self.hashed_matrix[i][k] == self.hashed_matrix[j][k]):
                        common_word_count_between_i_and_j+=1
                similarity_between_i_and_j = float(common_word_count_between_i_and_j/float(self.k))
                self.minhash_similarity_matrix[i][j]=similarity_between_i_and_j
                self.minhash_similarity_matrix[j][i]=similarity_between_i_and_j

        #PreprocessorHelper.write_to_file(self.minhash_similarity_matrix,self.feature_type+"_minhash_similarity.json",None)

    def get_rms_error_between_similarity_matrices(self):
        N = self.document_count
        num_of_comparisons = (N*(N-1))/2
        sum_of_square_of_errors = 0
        for i in range(N):
            for j in range(i+1,N):
                sum_of_square_of_errors += (self.minhash_similarity_matrix[i][j]-self.jaccard_similarity_matrix[i][j])**2
        return math.sqrt(sum_of_square_of_errors/num_of_comparisons)


def calculate_baseline_and_hashes(feature_type):
    sim = Similarity(feature_type)
    EFFICIENCY[feature_type] = {}
    EFFICACY[feature_type] = {}
    print "\n\n"
    print "CALCULATIONS FOR "+feature_type
    start = time.clock()
    sim.retrieve_and_transform_transactional_feature_vector()
    end = time.clock()

    print end - start, 'seconds to transform feature vectors into format easier to calculate similarities'
    start = time.clock()
    sim.populate_jaccard_similarity_matrix()
    end = time.clock()
    print end - start, 'seconds to populate baseline jaccard similarity matrix'
    EFFICIENCY[feature_type]["jaccard"] = end - start

    for k in K_VALUES:
        EFFICACY[feature_type][str(k)+"_minhash"] = {}
        print "For K value of "+str(k)
        start = time.clock()
        sim.populate_document_hashes(k)
        end = time.clock()
        print end - start, 'seconds to populate hashing matrix'

        start = time.clock()
        sim.populate_minhash_similarity_matrix()
        end = time.clock()
        print end - start, 'seconds to populate minhash similarity matrix'
        EFFICIENCY[feature_type][str(k)+"_minhash"] = end - start
        rmsq = sim.get_rms_error_between_similarity_matrices()
        EFFICACY[feature_type][str(k)+"_minhash"]["rmsq"] = rmsq
        print 'Root mean square error == ', rmsq
        print "\n"
        sim.reset()

def main():
    for feature in FEATURES:
        calculate_baseline_and_hashes(feature)
        PreprocessorHelper.write_to_file(EFFICACY,"efficacy.json")
        PreprocessorHelper.write_to_file(EFFICIENCY,"efficiency.json")
if __name__ == "__main__": main()
