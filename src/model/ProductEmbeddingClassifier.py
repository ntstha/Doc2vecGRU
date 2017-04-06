import cPickle;
import logging as logger;
import os;
import numpy
from sklearn import svm
from sklearn.metrics import confusion_matrix;

import config as config
from DbHandler import DbHandler;
from Utils import Utils


custom_gru=config.custom_gru
server_run = config.run_server;
run_folder = config.run_count;
table_name = config.table_name;
data_path = config.data_path;
output_path = config.output_path;
saved_path = config.saved_path;
data_dim =config.doc_vec_dim+config.GRU_product_embedding_dim;
log_file_name = config.log_file_name;


if not os.path.exists("%s/%s"%(output_path,run_folder)):
    os.makedirs("%s/%s"%(output_path,run_folder))

if custom_gru:
    logger.basicConfig(filename='%s/%s/custom_gru_product_classifier.log'%(output_path,run_folder),level=logger.INFO)
else:
    logger.basicConfig(filename='%s/%s/product_classifier.log'%(output_path,run_folder),level=logger.INFO)


if custom_gru:
    product_emb_file='%s/product_vectors/%s/custom_gru_product_embeddings_%s.pickle'%(saved_path,run_folder,table_name)
else:
    product_emb_file='%s/product_vectors/%s/product_embeddings_%s.pickle'%(saved_path,run_folder,table_name)

with open(product_emb_file, 'r') as fp:
    product_embedding_dict=cPickle.load(fp)

utils = Utils()
train_id_vector_rating_dict,test_id_vector_rating_dict = utils.getTrainTestIdRatingVector()

train_rating_vectors = train_id_vector_rating_dict.values()
test_rating_vectors = test_id_vector_rating_dict.values()


logger.info("Total train data :%d"%len(train_rating_vectors));
logger.info("Total test data :%d"%len(test_rating_vectors))

#create data and labels
X_train_arrays = numpy.zeros((len(train_rating_vectors),data_dim));
Y_train_labels = [None] * len(train_rating_vectors);

X_test_arrays = numpy.zeros((len(test_rating_vectors),data_dim));
Y_test_labels = [None] * len(test_rating_vectors);

#create training data and training labels
for index,tuple in enumerate(train_rating_vectors[:]):
    X_train_arrays[index] = numpy.concatenate((numpy.reshape(tuple[0],128),numpy.reshape(product_embedding_dict[tuple[2]],56)))
    Y_train_labels[index] = tuple[1]

#create test data and test labels
for index,tuple in enumerate(test_rating_vectors[:]):
    X_test_arrays[index] = numpy.concatenate((numpy.reshape(tuple[0],128),numpy.reshape(product_embedding_dict[tuple[2]],56)))
    Y_test_labels[index] = tuple[1];


classifier = svm.LinearSVC();

test_pred = classifier.fit(X_train_arrays, Y_train_labels).predict(X_test_arrays);

classification_accuracy = classifier.score(X_test_arrays, Y_test_labels);

print classification_accuracy;

logger.info("Classification accuracy :%f"%(classification_accuracy));

# Compute confusion matrix
cnf_matrix = confusion_matrix(Y_test_labels, test_pred)
logger.info(cnf_matrix);

logger.info("---------------------End of classification-------------------------------");

logger.info("saving trained classifier......")

if custom_gru:
    classifier_name='%s/doc2vec_classifier/custom_gru_doc2vec_classifier.pickle'%saved_path
else:
    classifier_name='%s/doc2vec_classifier/gru_doc2vec_classifier.pickle'%saved_path

with open(classifier_name, 'wb') as fid:
    cPickle.dump(classifier, fid)

logger.info("Classifier saved......")