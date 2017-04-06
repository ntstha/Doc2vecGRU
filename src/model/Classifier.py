import cPickle;
import logging as logger;
import os;
import random;
import matplotlib.pyplot as plt
import numpy
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix;
from sklearn.model_selection import KFold
from PlotHelper import plot_confusion_matrix

import config as config
from DbHandler import DbHandler;
from Utils import Utils

server_run = config.run_server;
run_folder = config.run_count;
table_name = config.table_name;
data_path = config.data_path;
output_path = config.output_path;
saved_path = config.saved_path;
doc_vec_dim =config.doc_vec_dim;
log_file_name = config.log_file_name;

if not os.path.exists("%s/%s"%(output_path,run_folder)):
    os.makedirs("%s/%s"%(output_path,run_folder))

logger.basicConfig(filename='%s/%s/%s.log'%(output_path,run_folder,log_file_name),level=logger.INFO)

use_SVM=True;

utils = Utils()
train_id_vector_rating_dict,test_id_vector_rating_dict = utils.getTrainTestIdRatingVector()

train_rating_vectors = train_id_vector_rating_dict.values()
test_rating_vectors = test_id_vector_rating_dict.values()


logger.info("Total train data :%d"%len(train_rating_vectors));
logger.info("Total test data :%d"%len(test_rating_vectors))

#create data and labels
X_train_arrays = numpy.zeros((len(train_rating_vectors),doc_vec_dim));
Y_train_labels = [None] * len(train_rating_vectors);

X_test_arrays = numpy.zeros((len(test_rating_vectors),doc_vec_dim));
Y_test_labels = [None] * len(test_rating_vectors);

#create training data and training labels
for index,tuple in enumerate(train_rating_vectors[:]):
    X_train_arrays[index] = tuple[0];
    Y_train_labels[index] = tuple[1];

#create test data and test labels
for index,tuple in enumerate(test_rating_vectors[:]):
    X_test_arrays[index] = tuple[0];
    Y_test_labels[index] = tuple[1];

if use_SVM:
    classifier = svm.LinearSVC();
else:
    classifier = LogisticRegression();

test_pred = classifier.fit(X_train_arrays, Y_train_labels).predict(X_test_arrays);

classification_accuracy = classifier.score(X_test_arrays, Y_test_labels);

print classification_accuracy;

logger.info("Classification accuracy :%f"%(classification_accuracy));

# Compute confusion matrix
cnf_matrix = confusion_matrix(Y_test_labels, test_pred)
logger.info(cnf_matrix);

logger.info("---------------------End of classification-------------------------------");

logger.info("saving trained classifier......")
with open('%s/doc2vec_classifier/classifier.pickle'%saved_path, 'wb') as fid:
    cPickle.dump(classifier, fid)

logger.info("Classifier saved......")
