import cPickle;
import logging as logger;
import os;
import random;
import numpy
from sklearn import svm
from sklearn.metrics import confusion_matrix;
from sklearn.model_selection import KFold
import config as config
from Utils import Utils

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

utils = Utils()

tag_vector_dict={};

with open('../saved/doc2vec_vectors/%s/doc2vec_vectors.pickle'%run_folder, 'r') as fp:
    tag_vector_dict = cPickle.load(fp);

id_rating_dict_list = utils.getIdandClassFromJsonFile(table_name);
id_rating_dict = {}
for _dict in id_rating_dict_list:
    prm_id = _dict.pop('prm_id');
    id_rating_dict["prm_%s"%str(prm_id)] = _dict['class'];

id_vector_rating_dict={key:(tag_vector_dict[key], id_rating_dict[key]) for key in tag_vector_dict}

all_rating_vectors = id_vector_rating_dict.values();

logger.info("Total data :%d"%len(all_rating_vectors));

#create data and labels
X_arrays = numpy.zeros((len(all_rating_vectors),doc_vec_dim));
Y_labels = [None] * len(all_rating_vectors);

#create training data and training labels
for index,tuple in enumerate(all_rating_vectors[:]):
    X_arrays[index] = tuple[0];
    Y_labels[index] = tuple[1];

logger.info("Dimensions of training arrays %d"%X_arrays.shape[1])

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

    print classification_accuracy;

    logger.info("Classification accuracy after %d iteration :%f"%(count,classification_accuracy));

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(test_labels, test_pred)
    logger.info(cnf_matrix);

    logger.info("---------------------End of classification %d iteration-------------------------------"%count);
    count=count+1

logger.info("Mean accuracy :%.4f"%(float(sum(accuracy_array))/len(accuracy_array)))
logger.info("saving trained classifier......")
with open('%s/doc2vec_classifier/classifier.pickle'%saved_path, 'wb') as fid:
    cPickle.dump(classifier, fid)

logger.info("Classifier saved......")
