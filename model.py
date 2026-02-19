import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- LOAD DATA ----------------
df = pd.read_csv("updated_data.csv")
df = df.fillna("")

# ---------------- TEXT COLUMNS ----------------
text_cols = [
    'slug','details','benefits','eligibility',
    'application','documents','level',
    'schemeCategory','tags'
]

df["combined"] = df[text_cols].agg(" ".join, axis=1)

# ---------------- NORMALIZE TEXT ----------------
def normalize(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\u0900-\u097f\u0a80-\u0aff\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["processed"] = df["combined"].apply(normalize)

# ---------------- TFIDF MODEL ----------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["processed"])

# ---------------- INTENT KEYWORDS ----------------
benefit_words = ["benefit","benefits","फायदे","लाभ","फायदा"]
doc_words = ["document","documents","कागदपत्र","दस्तऐवज","papers"]
elig_words = ["eligibility","eligible","पात्रता","योग्यता"]
apply_words = ["apply","application","अर्ज","process","apply kaise"]

# ---------------- POLITE FALLBACKS ----------------
fallbacks = [
    "😊 Sorry, I couldn't find information about that.\nPlease ask me about government schemes like benefits, eligibility, documents or application process.",
    "🙏 I may not have data for this topic.\nTry asking about any government scheme and I’ll help you.",
    "🤖 I am trained only on government schemes.\nPlease ask something related to schemes, benefits, or documents."
]

# ---------------- RESPONSE FUNCTION ----------------

def get_response(user_query):
    

    # Greeting detection
    greetings = ["hi","hello","hey","namaste","नमस्कार"]
    if any(g in user_query.lower() for g in greetings):
        return "Hello 👋 I can help you with government schemes. Ask me about benefits, eligibility, documents or application process."

    query = normalize(user_query)
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X).flatten()
    idx = np.argmax(scores)

    # -------- OUT OF TOPIC DETECTION --------
    if scores[idx] < 0.18:
        return np.random.choice(fallbacks)

    row = df.iloc[idx]

    # -------- INTENT BASED ANSWER --------
    if any(w in query for w in benefit_words):
        ans = row["benefits"]

    elif any(w in query for w in doc_words):
        ans = row["documents"]

    elif any(w in query for w in elig_words):
        ans = row["eligibility"]

    elif any(w in query for w in apply_words):
        ans = row["application"]

    else:
        ans = row["details"]

    # -------- CLEAN RESPONSE --------
    ans = str(ans).strip()

    if len(ans) < 5:
        return "Information not available for this scheme."

    # limit to first few sentences (avoid paragraph dumping)
    ans = ans.split(". ")
    ans = ". ".join(ans[:3])

    return ans
