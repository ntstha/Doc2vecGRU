import cPickle as pickle;
import config as config
from DbHandler import DbHandler
from gensim.models import Doc2Vec
import cPickle as cPickle
import os
import random
from keras.models import load_model
from keras.models import Model
from keras.utils import np_utils
import numpy
from sklearn.preprocessing import LabelEncoder
import sys

class Utils:

    def __init__(self):
        self.dbHandler = DbHandler();
        self.data_path = config.data_path;
        self.saved_path = config.saved_path
        self.run_count = config.run_count
        self.testVectors = config.Vector_test_data
        self.table_name = config.table_name
        self.doc2vec_filename = config.doc2vec_file_name
        self.doc_vec_dim = config.doc_vec_dim

    def getClassFromRating(self,rating):
        if rating=='4' or rating=='5':
            return 'pos'
        elif rating=='1' or rating=='2':
            return 'neg'
        else:
            return 'neu'

    def getIdandClassFromJsonFile(self,table_name):
        data = self.dbHandler.selectAllFromTable(table_name)
        id_class_data_list=[];
        for review in data:
            id_class_data={};
            id_class_data['prm_id']=review['prm_id'];
            id_class_data['rating']=review['rating'];
            id_class_data['product_id']=review['product_id']
            id_class_data['class']=self.getClassFromRating(review['rating']);
            id_class_data_list.append(id_class_data);
        return id_class_data_list;

    def getReviewGroupedByProductOrderedbyTime(self,table_name):
        data = self.dbHandler.getReviewGroupedByProductOrderByTime(table_name)
        return data;

    def getAllReviewsWithVectors(self,grouped_review):
        with open('%s/doc2vec_vectors/%s/doc2vec_vectors.pickle'%(self.saved_path,self.run_count)) as fp:
            tag_vector_dict = pickle.load(fp)
        grouped_vectors=[]
        for review in grouped_review:
            group_vector=(tag_vector_dict['prm_%s'%review['prm_id']],review['product_id'],self.getClassFromRating(review['rating']))
            grouped_vectors.append(group_vector)

        return grouped_vectors

    def changeYToReshapedArray(self,y_labels):
        y_arrays=self.changeYToArray(y_labels)
        encoder = LabelEncoder()
        encoder.fit(y_arrays)
        encoded_Y_train = encoder.transform(y_arrays)
        Y_train = np_utils.to_categorical(encoded_Y_train,nb_classes=3)
        return numpy.reshape(Y_train, (1, Y_train.shape[0], Y_train.shape[1]))

    def changeXToReshapedArray(self,ls):
        arrays = numpy.zeros((len(ls),self.doc_vec_dim));
        for index,l in enumerate(ls):
            arrays[index] = l
        return numpy.reshape(arrays, (1, arrays.shape[0], arrays.shape[1]))

    def changeYToArray(self,ls):
        arrays = [None] * len(ls);
        for index,l in enumerate(ls):
            arrays[index] = l
        return arrays

    def saveLatestProductIdWithVectors(self,gru_file_name):
        with open('%s/doc2vec_vectors/%s/doc2vec_vectors.pickle'%(self.saved_path,self.run_count)) as fp:
            tag_vector_dict = pickle.load(fp)

        product_embedding_dict={}
        gru_model = load_model('%s/GRU/%s/%s'%(self.saved_path,self.run_count,gru_file_name))
        gru_layer_model = Model(input=gru_model.input,
                                output=gru_model.get_layer('GRU').output)

        unique_product_Xvectors=[]
        unique_product_Ylabels=[]
        current_product_id="-1"

        grouped_review =utils.getReviewGroupedByProductOrderedbyTime(self.table_name)

        for index,review in enumerate(grouped_review):
            if current_product_id=='-1' or review['product_id']==current_product_id:
                current_product_id=review['product_id']
                unique_product_Xvectors.append(tag_vector_dict['prm_%s'%review['prm_id']])
                unique_product_Ylabels.append(self.getClassFromRating(review['rating']))
            else:
                X_predict = self.changeXToReshapedArray(unique_product_Xvectors)
                timestep_predict = gru_layer_model.predict(X_predict)
                timestep_predict = numpy.reshape(timestep_predict,(timestep_predict.shape[1],timestep_predict.shape[2]))
                product_embedding_dict[current_product_id]=timestep_predict[-1]
                unique_product_Xvectors=[]
                unique_product_Ylabels=[]
                unique_product_Xvectors.append(tag_vector_dict['prm_%s'%review['prm_id']])
                unique_product_Ylabels.append(self.getClassFromRating(review['rating']))
                current_product_id=review['product_id']
            if index==len(grouped_review)-1:
                X_predict = self.changeXToReshapedArray(unique_product_Xvectors)
                timestep_predict = gru_layer_model.predict(X_predict)
                timestep_predict = numpy.reshape(timestep_predict,(timestep_predict.shape[1],timestep_predict.shape[2]))
                product_embedding_dict[current_product_id]=timestep_predict[-1]

        if not os.path.exists("%s/product_vectors/%s"%(self.saved_path,self.run_count)):
            os.makedirs("%s/product_vectors/%s"%(self.saved_path,self.run_count))

        saveFileName='%s/product_vectors/%s/product_embeddings_%s.pickle'%(self.saved_path,self.run_count,self.table_name)
        with open(saveFileName, 'w') as fp:
            cPickle.dump(product_embedding_dict, fp)

    def getTrainingVectorsAndLabels(self,grouped_review):
        with open('%s/doc2vec_vectors/%s/doc2vec_vectors.pickle'%(self.saved_path,self.run_count)) as fp:
            tag_vector_dict = pickle.load(fp)

        training_vectors=[]
        training_labels=[]
        unique_product_Xvectors=[]
        unique_product_Ylabels=[]
        current_product_id="-1"
        for index,review in enumerate(grouped_review):
            if current_product_id=='-1' or review['product_id']==current_product_id:
                current_product_id=review['product_id']
                unique_product_Xvectors.append(tag_vector_dict['prm_%s'%review['prm_id']])
                unique_product_Ylabels.append(self.getClassFromRating(review['rating']))
            else:
                # reshape to be [samples, time steps, features]
                training_vectors.append(self.changeXToReshapedArray(unique_product_Xvectors))
                training_labels.append(self.changeYToReshapedArray(unique_product_Ylabels))
                unique_product_Xvectors=[]
                unique_product_Ylabels=[]
                unique_product_Xvectors.append(tag_vector_dict['prm_%s'%review['prm_id']])
                unique_product_Ylabels.append(self.getClassFromRating(review['rating']))
                current_product_id=review['product_id']
            if index==len(grouped_review)-1:
                training_vectors.append(self.changeXToReshapedArray(unique_product_Xvectors))
                training_labels.append(self.changeYToReshapedArray(unique_product_Ylabels))

        print len(training_vectors)
        return training_vectors,training_labels

    def doc2vec_toFile(self):
        model = Doc2Vec.load("%s/doc2vec/runs/%s/%s"%(self.saved_path,self.run_count,self.doc2vec_filename));
        tag_vector_dict={};
        for tag in model.docvecs.doctags:
            tag_vector_dict[tag]=model.docvecs[tag];
        if not os.path.exists("%s/doc2vec_vectors/%s"%(self.saved_path,self.run_count)):
            os.makedirs("%s/doc2vec_vectors/%s"%(self.saved_path,self.run_count))

        with open('%s/doc2vec_vectors/%s/doc2vec_vectors.pickle'%(self.saved_path,self.run_count), 'w') as fp:
            cPickle.dump(tag_vector_dict, fp)


if __name__=='__main__':
    utils = Utils()
    args = sys.argv
    if args[1]=='1':
        utils.doc2vec_toFile()
    elif args[1]=='2':
        gru_file_name=str(args[2])
        utils.saveLatestProductIdWithVectors(gru_file_name)