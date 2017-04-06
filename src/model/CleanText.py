import numpy as np
import re
import itertools
from collections import Counter
import string as str
from nltk import PorterStemmer;

def clean_str(string):
    string = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', string)
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " is", string)
    string = re.sub(r"\'ve", " have", string)
    string = re.sub(r"n\'t", " not", string)
    string = re.sub(r"\'re", " are", string)
    string = re.sub(r"\'d", " would", string)
    string = re.sub(r"\'ll", " will", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower();


test_string="I live in MN... so when the mailman dropped this off, it was frozen. I was eager to use it, but couldn't. But the smell of it is out of this world!Once I was able to use this product, I used it in my hair as an over night mask. It added shine and vibrancy     to my hair instantly.I've used it on my feet as well, and not sure where I've been, but this product is well worth your money.I don't use it for cooking, but strictly for bathroom (hair, skin, etc.) use.";
print clean_str(test_string);