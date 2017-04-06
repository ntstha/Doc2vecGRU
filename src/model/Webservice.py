import web
import cPickle as pickle
from gensim.models import Doc2Vec
import numpy
import json
urls = (
    '/check', 'Index'
)


app = web.application(urls, globals())

class Index(object):
    def __init__(self):
        with open('../data/classifier.pickle') as fp:
            self.svm = pickle.load(fp)
        self.model = Doc2Vec.load("../data/doc2vec.d2v");
        with open('../data/product_embeddings.pickle') as fp:
            self.product_embeddings = pickle.load(fp)


    def GET(self):
        form = web.input(review=None,product_id=None,rating=None)
        review_text = form.review
        rating= form.rating
        rating_class='neu'
        if int(rating)==4 or int(rating)==5:
            rating_class='pos'
        elif int(rating)==1 or int(rating)==2:
            rating_class='neg'
        elif int(rating)==3:
            rating_class='neu'

        product_id = form.product_id

        print self.product_embeddings.keys()
        product_embedding = self.product_embeddings[product_id]
        print len(product_embedding)

        self.model.random.seed(0)
        review_embedding = self.model.infer_vector(review_text.split())
        print len(review_embedding)

        final_embed = numpy.concatenate((numpy.reshape(review_embedding,128),numpy.reshape(product_embedding,128)))
        rating_class_pred = self.svm.predict(final_embed)

        data={}
        warn=False
        msg=""

        if rating_class_pred=='pos':
            if rating_class=='neg':
                warn=True
                msg="Our system detects that the review is Positive. Your rating is Negative. Do you want to correct it?"
            else:
                warn=False
                msg=""
        elif rating_class_pred=='neg':
            if rating_class=='pos':
                warn=True
                msg="Our system detects that the review is Negative. Your rating suggest is Positive. Do you want to correct it?"
            else:
                warn=False
                msg=""
        else:
            warn=False
            msg=""

        data['warn']=warn
        data['message']=msg
        json_data = json.dumps(data)
        print rating_class_pred

        return json_data

if __name__ == "__main__":
    app.run()