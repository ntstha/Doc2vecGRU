import cPickle;
import logging as logger;
import os;
import numpy
from sklearn import svm
from sklearn.metrics import confusion_matrix;
import config as config
import random
from Utils import Utils
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error

run_folder = config.run_count;
table_name = config.table_name;
data_path = config.data_path;
output_path = config.output_path;
saved_path = config.saved_path;
data_dim =config.doc_vec_dim+config.GRU_product_embedding_dim;
log_file_name = config.log_file_name;


if not os.path.exists("%s/%s"%(output_path,run_folder)):
    os.makedirs("%s/%s"%(output_path,run_folder))


logger.basicConfig(filename='%s/%s/product_classifier.log'%(output_path,run_folder),level=logger.INFO)



product_emb_file='%s/product_vectors/%s/product_embeddings_%s.pickle'%(saved_path,run_folder,table_name)

with open(product_emb_file, 'r') as fp:
    product_embedding_dict=cPickle.load(fp)

utils = Utils()
all_id_vectors = utils.getAllReviewsWithVectors(utils.getReviewGroupedByProductOrderedbyTime(table_name))

logger.info("Total data :%d"%len(all_id_vectors));

#create data and labels
X_arrays = numpy.zeros((len(all_id_vectors),data_dim));
Y_labels = [None] * len(all_id_vectors);

#create training data and training labels
for index,tuple in enumerate(all_id_vectors[:]):
    X_arrays[index] = numpy.concatenate((numpy.reshape(tuple[0],300),numpy.reshape(product_embedding_dict[tuple[1]],128)))
    Y_labels[index] = tuple[2]


x_y = list(zip(X_arrays, Y_labels));
random.shuffle(x_y);
x_shuffled, y_shuffled = zip(*x_y);

classifier = svm.LinearSVC();

kfold = KFold(n_splits=5)

count=0
accuracy_array=[0]*5
for train_indices,test_indices in kfold.split(x_shuffled):
    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []

    print("<------------------Operation:",count,"------------------------------>")
    logger.debug("------------------Operation:%d------------------------------"%count)
    for train_index in train_indices:
        train_data.append(x_shuffled[train_index]);
    for test_index in test_indices:
        test_data.append(x_shuffled[test_index]);
    for train_index in train_indices:
        train_labels.append(y_shuffled[train_index]);
    for test_index in test_indices:
        test_labels.append(y_shuffled[test_index]);

    test_pred = classifier.fit(train_data, train_labels).predict(test_data);

    classification_accuracy = classifier.score(test_data, test_labels);

    accuracy_array[count]=classification_accuracy

    print "Accuracy :",classification_accuracy;

    logger.info("Classification accuracy after %d iteration :%f"%(count,classification_accuracy));

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(test_labels, test_pred)
    logger.info(cnf_matrix);

    logger.info("---------------------End of classification %d iteration-------------------------------"%count);
    count=count+1

logger.info("Mean accuracy :%.4f"%(float(sum(accuracy_array))/len(accuracy_array)))


classifier_name='%s/doc2vec_classifier/gru_doc2vec_classifier.pickle'%saved_path

with open(classifier_name, 'wb') as fid:
    cPickle.dump(classifier, fid)

logger.info("Classifier saved......")