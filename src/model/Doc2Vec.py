import logging as logger;
import os;
import timeit;
from random import shuffle;

from DbHandler import DbHandler
from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import config as config;
from CleanText import clean_str;

run_folder= config.run_count;
table_name = config.table_name;
workers = config.num_workers;
vec_dim = config.doc_vec_dim;
window = config.context_window_size;

data_path = config.data_path;
output_path = config.output_path;
saved_path = config.saved_path;
doc2vec_filename = config.doc2vec_file_name


if not os.path.exists("%s/%s"%(output_path,run_folder)):
    os.makedirs("%s/%s"%(output_path,run_folder))

logger.basicConfig(filename='%s/%s/doc2vec.log'%(output_path,run_folder),level=logger.INFO)

dbHandler = DbHandler();

review_dict=dbHandler.selectAllFromTable(table_name);

logger.info("Loading of data complete. Data size %d"%len(review_dict));

class LabeledLineSentence(object):

    def __init__(self,review_dict):
        self.review_dict=review_dict;

    def review_to_array(self):
        self.sentences=[];
        for obj_dict in self.review_dict:
            review = clean_str(obj_dict['review']);
            self.sentences.append(TaggedDocument(utils.to_unicode(review).split(),["prm_"+str(obj_dict['prm_id'])]));
        return self.sentences;


    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

sentences = LabeledLineSentence(review_dict);

logger.info("Building model window size=%d, size=%d, workers=%d"%(window,vec_dim,workers));

model = Doc2Vec(min_count=1, window=window, size=vec_dim, sample=1e-4, negative=5, workers=workers)

model.build_vocab(sentences.review_to_array())

logger.info("Starting training.......");

logger.info("Training for %d epoch" % config.num_epoch);

start_time = timeit.default_timer()

for epoch in range(config.num_epoch):
    logger.info('Epoch %d' % epoch)
    model.train(sentences.sentences_perm());
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

logger.info("Training completed.....");

logger.info("Training completed in %s"%str(timeit.default_timer() - start_time));

logger.info("Saving trained model.....")

if not os.path.exists("%s/doc2vec/runs/%s"%(saved_path,run_folder)):
    os.makedirs("%s/doc2vec/runs/%s"%(saved_path,run_folder))

model.save('%s/doc2vec/runs/%s/%s'%(saved_path,run_folder,doc2vec_filename));

logger.info("Saved model successfully......");
