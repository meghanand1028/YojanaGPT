import pandas as pd
import numpy as np
import re
import os
import requests
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
benefit_words = ["benefit","benefits","फायदे","लाभ","फायदा","advantage","profit"]
doc_words = ["document","documents","कागदपत्र","दस्तऐवज","papers","require","required"]
elig_words = ["eligibility","eligible","पात्रता","योग्यता","qualify","criteria","age","income"]
apply_words = ["apply","application","अर्ज","process","apply kaise","how to apply","registration","register"]
scheme_words = ["yojana","योजना","scheme","program","ministry","government","subsidy","pension","ration"]

# ---------------- SCHEME INTENT DETECTOR ----------------
def is_scheme_query(query):
    q = query.lower()
    return any(word in q for word in scheme_words)

# ---------------- POLITE FALLBACKS ----------------
fallbacks = [
    "😊 Sorry, I couldn't find information about that.\nPlease ask me about government schemes like benefits, eligibility, documents or application process.",
    "🙏 I may not have data for this topic.\nTry asking about any government scheme and I’ll help you.",
    "🤖 I am trained mainly on government schemes.\nPlease ask something related to schemes, benefits, or documents."
]

# ---------------- OPENAI CONFIG ----------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def get_ai_response(user_query):
    """Call OpenAI when dataset cannot answer"""
    if not OPENAI_API_KEY:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system",
                 "content": "You are a helpful assistant. Answer clearly and accurately in simple language."},
                {"role": "user", "content": user_query}
            ],
            "temperature": 0.7,
            "max_tokens": 400
        }

        response = requests.post(
            OPENAI_API_URL,
            json=payload,
            headers=headers,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("OpenAI error:", e)

    return None


# ---------------- RESPONSE FUNCTION ----------------
def get_response(user_query):

    # Greeting detection
    greetings = ["hi","hello","hey","namaste","नमस्कार"]
    if any(g in user_query.lower() for g in greetings):
        return "Hello 👋 I can help you with government schemes. Ask me about benefits, eligibility, documents or application process."

    query = normalize(user_query)

    # 👉 If NOT scheme related → directly use AI
    if not is_scheme_query(query):
        ai_response = get_ai_response(user_query)
        if ai_response:
            return ai_response
        return np.random.choice(fallbacks)

    # 👉 Search dataset
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X).flatten()
    idx = np.argmax(scores)
    best_score = scores[idx]

    # 👉 If match is weak → use AI
    if best_score < 0.35:
        ai_response = get_ai_response(user_query)
        if ai_response:
            return ai_response
        return np.random.choice(fallbacks)

    row = df.iloc[idx]

    # 👉 Intent-based answer extraction
    ans = ""

    if any(w in query for w in benefit_words):
        ans = str(row.get("benefits", "")).strip()
    elif any(w in query for w in doc_words):
        ans = str(row.get("documents", "")).strip()
    elif any(w in query for w in elig_words):
        ans = str(row.get("eligibility", "")).strip()
    elif any(w in query for w in apply_words):
        ans = str(row.get("application", "")).strip()
    else:
        ans = str(row.get("details", "")).strip()

    # 👉 If dataset answer empty → use AI
    if not ans or len(ans) < 5:
        ai_response = get_ai_response(user_query)
        if ai_response:
            return ai_response
        return np.random.choice(fallbacks)

    # 👉 Limit response length
    sentences = ans.split(". ")
    ans = ". ".join(sentences[:6])
    if len(sentences) > 6:
        ans += "."

    return ans