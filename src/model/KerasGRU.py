import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers.wrappers import TimeDistributed
from keras.layers import GRU
from keras.layers import Activation
import config;
from Utils import Utils
import logging as logger;
import os
import keras
import timeit
from keras.models import load_model
import random

doc_vec_dim=config.doc_vec_dim
table_name = config.table_name
product_embedding_dim = config.GRU_product_embedding_dim
num_epoch = config.GRU_nepoch
saved_path = config.saved_path
run_folder = config.run_count
output_path = config.output_path
log_file_name= config.GRU_logfile_name
input_dropout = config.GRU_input_dropout
save_after= config.save_after;

if not os.path.exists("%s/%s"%(output_path,run_folder)):
    os.makedirs("%s/%s"%(output_path,run_folder))


logger.basicConfig(filename='%s/%s/%s.log'%(output_path,run_folder,log_file_name),level=logger.INFO)


class LoggingCallback(keras.callbacks.Callback):

    def __init__(self,logger):
        self.logger =logger;

    def on_epoch_end(self, epoch, logs={}):
        msg = "{Epoch: %i} %s" % (epoch, ", ".join("%s: %f" % (k, v) for k, v in logs.items()))
        self.logger.info(msg)


random.seed(7000);

utils = Utils()
grouped_review = utils.getReviewGroupedByProductOrderedbyTime(table_name)

logger.info("Training GRU with data of length %d"%len(grouped_review))

training_vectors,training_labels = utils.getTrainingVectorsAndLabels(grouped_review)

#create GRU model

model = Sequential()
model.add(GRU(input_dim=doc_vec_dim,output_dim=product_embedding_dim,name='GRU',dropout_W=input_dropout,return_sequences=True))
model.add(TimeDistributed(Dense(input_dim=product_embedding_dim,output_dim=3)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adagrad', class_mode="categorical",metrics=['accuracy'])


print(model.summary());

if not os.path.exists("%s/GRU/%s"%(saved_path,run_folder)):
    os.makedirs("%s/GRU/%s"%(saved_path,run_folder))

for i in range(num_epoch):
    start_time=timeit.default_timer()
    for index in range(len(training_labels)):
        x_train = training_vectors[index]
        y_train = training_labels[index]
        model.train_on_batch(x_train, y_train)
    logger.info("Epoch %d took %s seconds"%(i,timeit.default_timer()-start_time))
    if (i+1)%int(save_after)==0:
        logger.info("Saving model after training for %d epoch"%num_epoch)
        model.save('%s/GRU/%s/trained_product_GRU_%s.h5'%(saved_path,run_folder,str(i)))
        logger.info("Model saved successfully.......")
