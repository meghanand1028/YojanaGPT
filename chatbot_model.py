import pandas as pd
import nltk
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download once
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load dataset
df = pd.read_csv("updated_data.csv")

# Fill nulls
# Fill only text columns
text_cols = df.select_dtypes(include="object").columns
df[text_cols] = df[text_cols].fillna("")


# Combine text columns
df["combined"] = (
    df["scheme_name"] + " " +
    df["details"] + " " +
    df["benefits"] + " " +
    df["eligibility"] + " " +
    df["tags"]
)

# Preprocess function
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words and w not in string.punctuation]
    return " ".join(tokens)

# Create processed column AFTER function defined
df["processed"] = df["combined"].apply(preprocess)

# TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["processed"])

# Intent detection
def detect_intent(query):
    q = query.lower()
    if "eligib" in q or "who can apply" in q:
        return "eligibility"
    elif "benefit" in q or "advantage" in q:
        return "benefits"
    elif "apply" in q or "how to apply" in q:
        return "application"
    elif "document" in q:
        return "documents"
    else:
        return "details"

# Response function
def get_bot_response(user_query):

    processed_query = preprocess(user_query)
    query_vec = vectorizer.transform([processed_query])

    similarity = cosine_similarity(query_vec, X)
    index = similarity.argmax()

    intent = detect_intent(user_query)

    scheme = df.iloc[index]["scheme_name"]

    if intent in df.columns:
        answer = df.iloc[index][intent]
    else:
        answer = df.iloc[index]["details"]

    return f"{scheme}\n\n{answer}"
