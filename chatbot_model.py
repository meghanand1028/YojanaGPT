import pandas as pd
import nltk
import numpy as np
import re
from nltk.stem import wordnet # to perform lemmitization
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer # to perfor bow
from sklearn.feature_extraction.text import TfidfVectorizer # to perfor bow
from nltk import pos_tag # for parts of speech
from sklearn.metrics import pairwise_distances # to perform cosine similarity
from nltk import word_tokenize # to create tokens
from nltk.corpus import stopwords # for stop words

# Download nltk data libraries. All can be downloaded by using nltk.download('all')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
# nltk.download('all')
df = pd.read_csv('updated_data.csv')

df.head(20) # See first 20 lines
df.shape[0] # Returns the number of rows in dataset
df.isnull().sum()
df.ffill(axis = 0,inplace=True) # fills the null value with the previous value.
df.head(20)