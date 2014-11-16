import json
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import *
from sklearn.svm import SVC
from sklearn.tree import *
import time
from sklearn.feature_extraction import DictVectorizer
from nltk.classify import DecisionTreeClassifier
import numpy as np
from preprocessorhelper import *

class Classifier:
    TRAINING_TESTING_SPLIT_FRACTION = 0.8
    def __init__(self, feature_type):
        self.feature_type = feature_type
        self.feature_vectors = {}
        self.feature_vectors_tuples_for_train = []
        self.feature_vectors_tuples_for_test = []



    def prepare_data_for_classify(self):
        self.feature_vectors = PreprocessorHelper.convert_to_utf(json.load(open(self.feature_type+'.json')))
        self.preprare_train_and_test_set()


    def classify_naive_bayes(self, classifier_type):
        #classifier = SklearnClassifier(classifier_type)
        clf = classifier_type

        #Feature_vector_tuples consist of (feature_type, topic) tuples
        #X contains a list of feature_types for all tuples, and Y a list of topics for all tuples
        X = np.array([feature_vector_tuple[0] for feature_vector_tuple in self.feature_vectors_tuples_for_train])
        Y = np.array([feature_vector_tuple[1] for feature_vector_tuple in self.feature_vectors_tuples_for_train])
        print "training"
        vectorizer = DictVectorizer(dtype=float, sparse=True)
        X = vectorizer.fit_transform(X)
        clf.fit(X,Y)
        #classifier.train(self.feature_vectors_tuples_for_train)
        print "testing classifier"
        X_test = vectorizer.transform(np.array([feature_vector[0] for feature_vector in self.feature_vectors_tuples_for_test]))
        classified_labels = clf.predict(X_test)
        #for i in range(0,len(predicted_list)):
         #   print predicted_list[i] == self.feature_vectors_tuples_for_test[i][1]
        #classified_labels =  classifier.batch_classify([feature_set_tuple[0] for feature_set_tuple in self.feature_vectors_tuples_for_test])
        correct = 0
        wrong = 0
        for i in range(0, len(classified_labels)):
            #print classified_labels[i] +' ' + self.feature_vectors_tuples_for_test[i][1]
            if classified_labels[i] == self.feature_vectors_tuples_for_test[i][1]:
                correct += 1
            else:
                wrong += 1
        print correct, wrong

    def classify_decision_tree(self):

        print "training decision tree"
        classifier = DecisionTreeClassifier.train(self.feature_vectors_tuples_for_train, depth_cutoff=200, entropy_cutoff=0.1)
        print "testing classifier"
        classified_labels =  classifier.batch_classify([feature_set_tuple[0] for feature_set_tuple in self.feature_vectors_tuples_for_test])
        correct = 0
        wrong = 0
        for i in range(0, len(classified_labels)):
            if classified_labels[i] is self.feature_vectors_tuples_for_test[i][1]:
                correct += 1
            else:
                wrong += 1
        print correct, wrong


    #separates train and test data
    def preprare_train_and_test_set(self):
        print 'preparing training and test sets from the datasets. Ratio of Training to Test = ', Classifier.TRAINING_TESTING_SPLIT_FRACTION, ':' 1-Classifier.TRAINING_TESTING_SPLIT_FRACTION
        for topic,topic_vector in self.feature_vectors.iteritems():
            #Within each topic, choose a fraction of the key-values as training set
            train_data_limit = int(Classifier.TRAINING_TESTING_SPLIT_FRACTION*len(topic_vector))
            i = 0
            for doc_id,feature_vector in topic_vector.iteritems():
                classify_tuple = (feature_vector[self.feature_type], topic)
                i = i+1
                if i <= train_data_limit:
                    self.feature_vectors_tuples_for_train.append(classify_tuple)
                else:
                    self.feature_vectors_tuples_for_test.append(classify_tuple)
        print 'Number of training set tuples: ', len(self.feature_vectors_tuples_for_train)
        print 'Number of test set tuples: ', len(self.feature_vectors_tuples_for_test)


    #Function not used anywhere
    def create_word_dict(self):
        self.feature_vectors = PreprocessorHelper.convert_to_utf(json.load(open(self.feature_type+'.json')))
        word_dict = {}
        i = 0
        for topic,topic_vector in self.feature_vectors.iteritems():
            #print topic
            for doc_id,feature_vector in topic_vector.iteritems():
                i = i+1
                for word,freq in feature_vector['term_frequencies'].iteritems():
                    if word not in word_dict:
                        word_dict[word] = 1 #freq
                    else:
                        word_dict[word] += 1

        print i
        s=open('word_dict.json','w')
        json.dump(word_dict, s)
        s.close()


def main():
    classifier = Classifier('term_frequencies')
    classifier.prepare_data_for_classify()
    start = time.clock()
    classifier.classify_naive_bayes(MultinomialNB())
    end = time.clock()
    print end - start, 'seconds to train and classify with naive_bayes'

    #code for decision tree. Not sure it works well yet
    #start = time.clock()
    #classifier.classify_decision_tree()
    #end = time.clock()
    #print end - start, 'seconds to train and classify with decision tree'
    #classifier.create_word_dict()
if __name__ == "__main__": main()
