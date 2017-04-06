import os;

import config as config
import DbHandler as DbHandler

table_name = config.table_name;

review_file_name="../data/amazon10msample.txt";

def convert_rating_text_to_number(rating_text):
    return str(list(filter(str.isdigit,rating_text))[0]);

script_dir = os.path.dirname(os.path.realpath('__file__'));
file_object = open(review_file_name, "r");
all_text = file_object.read();
file_object.close();

dict_list=[];

for line in all_text.splitlines():
    if line.startswith("rating:"):
        obj={};
        obj["rating"]=convert_rating_text_to_number(line);
    elif line.startswith("product_ID:"):
        obj["product_id"]=line.replace("product_ID:","").strip();
    elif line.startswith("helpfulness:"):
        obj["helpfulness"]=line.replace("helpfulness:","").strip();
    elif line.startswith("ID:"):
        obj["id"]=line.replace("ID:","").strip();
    elif line.startswith("review_by:"):
        obj["review_by"] =line.replace("review_by:","").strip();
    elif line.startswith("title:"):
        obj["title"]=line.replace("title:","").strip();
    elif line.startswith("review_time:"):
        obj["review_time"]=line.replace("review_time:","").strip();
    elif line.startswith("review:"):
        obj["review"] = line.replace("review:","").strip();
        dict_list.append(obj);
    else:
        continue;

print "Total Length of Reviews : ",len(dict_list);


#------------Insert Reviews Into Database ------------------------#

dbHandler = DbHandler();
dbHandler.insert_reviews_toDb(dict_list,table_name);
