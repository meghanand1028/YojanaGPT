from deep_translator import GoogleTranslator

import pandas as pd
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

# download once
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# load dataset
df = pd.read_csv("updated_data.csv")

df = pd.read_csv("updated_data.csv")

# convert required columns to string safely
text_cols = [
    'slug','details','benefits','eligibility',
    'application','documents','level',
    'schemeCategory','tags'
]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).fillna("")

# combine all text columns into one response column
df["Text Response"] = (
    df['slug'] + " " +
    df['details'] + " " +
    df['benefits'] + " " +
    df['eligibility'] + " " +
    df['application'] + " " +
    df['documents'] + " " +
    df['level'] + " " +
    df['schemeCategory'] + " " +
    df['tags']
)

# ---------- TEXT PROCESSING ----------

lemmatizer = WordNetLemmatizer()
stop = set(stopwords.words('english'))

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z ]', ' ', text)
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    words = []
    for word, pos in tagged:
        if word in stop:
            continue
        if pos.startswith('V'):
            pos='v'
        elif pos.startswith('J'):
            pos='a'
        elif pos.startswith('R'):
            pos='r'
        else:
            pos='n'
        words.append(lemmatizer.lemmatize(word,pos))
    return " ".join(words)

# normalize dataset
df["processed"] = df["Text Response"].apply(normalize)

# vectorizer
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df["processed"])

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def extract_relevant_part(question, response):

    q = question.lower()

    if "benefit" in q or "advantage" in q:
        return response.split("Eligibility")[0]

    elif "eligibility" in q or "who can apply" in q:
        parts = response.split("Eligibility")
        return "Eligibility" + parts[1] if len(parts)>1 else response

    elif "apply" in q or "registration" in q:
        parts = response.split("Application")
        return "Application" + parts[1] if len(parts)>1 else response

    elif "document" in q:
        parts = response.split("Documents")
        return "Documents" + parts[1] if len(parts)>1 else response

    else:
        # default short summary
        return response[:500] + "..."


# ---------- CHAT FUNCTION ----------

def get_response(user_text):

    original_question = user_text

    user_text = translate_to_english(user_text)
    processed = normalize(user_text)
    vec = tfidf.transform([processed])

    similarity = 1 - pairwise_distances(X, vec, metric='cosine')
    idx = similarity.argmax()

    full_response = df["Text Response"].iloc[idx]

    final_answer = extract_relevant_part(original_question, full_response)

    return final_answer

    return response
