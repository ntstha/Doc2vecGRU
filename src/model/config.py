
#project configuration
run_count=1000;
table_name='Review_test'
data_path='../data'
output_path='../output'
saved_path='../saved'


#Doc2Vec configuration
Vector_test_data=0.1
doc2vec_file_name="review_doc2vec.d2v"
num_epoch=5 #test
num_workers=18;
doc_vec_dim=300;
context_window_size=10;


#svm configuration
# k=3
log_file_name='svm_classifier'

#GRU configuration

save_after=1

GRU_product_embedding_dim=128
GRU_nepoch=2
GRU_logfile_name='gru'
GRU_input_dropout=0.25
GRU_custom_batch_logfile_name='gru_custom'
GRU_custom_num_epoch=3
GRU_custom_validation_size=0.1
