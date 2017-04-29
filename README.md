# Doc2vecGRU

This project was done as part of my Master's in Computer Science thesis. The first part of the project converts 3 million Amazon product reviews to 300 dimensional vector using "Paragraph Vector" (see class "Doc2Vec.py"). We using "Genism" to do that cuz it is awesome and easy. The next part of the project learns information hidden in sequence of product reviews using Recurrent Neural Network with Gated Recurrent Unit. We group our review vectors by product and sort them by their posted time and make a sequence of that and feed them to a GRU. Our GRU then learns product information inform of 128 dimensional vectors.

To check if learning product information helps in increasing classification accuracy, we use review vector alone and combination of review vector and product vector to train two SVM. 81.30% accuracy is achieved by review vector alone while with the combination of two vectors we get an accuracy of 81.88%.
 
We also show a real life use of sentiment analysis. Our model will be used to identify and prevent issues of review and rating mismatch i.e giving incorrect sentiment rating to a review.

Inspired from http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7515294

# How to run this project

Download dataset from http://www.ilabsite.org/datacenter/communitynetworks/amazontotal.rar and place it in src/data folder.

Set paths in src/model/config.py. The file is self explanatory.




