import json
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import *
from sklearn.svm import SVC
from sklearn.tree import *
import time
class Classifier:
    def __init__(self, feature_type):
        self.feature_type = feature_type
        self.feature_vectors = {}
        self.feature_vectors_tuples_for_train = []
        self.feature_vectors_tuples_for_test = []


    def create_word_dict(self):
        self.feature_vectors = self.convert_to_utf(json.load(open(self.feature_type+'.json')))
        word_dict = {}
        i = 0
        for topic,topic_vector in self.feature_vectors.iteritems():
            #print topic
            for doc_id,feature_vector in topic_vector.iteritems():
                i = i+1
                for word,freq in feature_vector['term_frequencies'].iteritems():
                    if word not in word_dict:
                        word_dict[word] = 0 #freq
                    #else:
                        #word_dict[word] = freq

        print i
        s=open('word_dict.json','w')
        json.dump(word_dict, s)
        s.close()

    def prepare_data_for_classify(self):
        self.feature_vectors = self.convert_to_utf(json.load(open(self.feature_type+'.json')))
        print "preparing data"
        self.preprare_train_and_test_set()


    def classify(self, classifier_type):
        classifier = SklearnClassifier(classifier_type)
        print "training"
        classifier.train(self.feature_vectors_tuples_for_train)
        print "testing classifier"
        classified_labels =  classifier.batch_classify([feature_set_tuple[0] for feature_set_tuple in self.feature_vectors_tuples_for_test])
        correct = 0
        wrong = 0
        for i in range(0, len(classified_labels)):
            #print classified_labels[i] +' ' + self.feature_vectors_tuples_for_test[i][1]
            if classified_labels[i] is self.feature_vectors_tuples_for_test[i][1]:
                correct += 1
            else:
                wrong += 1
        print correct, wrong


    def preprare_train_and_test_set(self):
        for topic,topic_vector in self.feature_vectors.iteritems():
            train_data_limit = int(0.8*len(topic_vector))
            i = 0
            for doc_id,feature_vector in topic_vector.iteritems():
                classify_tuple = (feature_vector[self.feature_type], topic)
                i = i+1
                if i <= train_data_limit:
                    self.feature_vectors_tuples_for_train.append(classify_tuple)
                else:
                    self.feature_vectors_tuples_for_test.append(classify_tuple)
        print len(self.feature_vectors_tuples_for_train)
        print len(self.feature_vectors_tuples_for_test)


    def convert_to_utf(self, input):
        if isinstance(input, dict):
            return {self.convert_to_utf(key): self.convert_to_utf(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.convert_to_utf(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input




def main():
    classifier = Classifier('term_frequencies')
    start = time.clock()
    classifier.prepare_data_for_classify()
    classifier.classify(MultinomialNB())
    end = time.clock()
    print end - start, 'seconds to train and classify'

    #classifier.create_word_dict()
if __name__ == "__main__": main()
