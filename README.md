# YojanaGPT – NLP-Powered Indian Government Schemes Assistant

YojanaGPT is an NLP-based chatbot designed to help people discover and understand Indian government schemes. Users can ask questions in natural language and find relevant information about scheme benefits, eligibility criteria, required documents, and application procedures.

The goal is to make government-scheme information easier to search, understand, and access through a simple web interface.

## ✨ Features

- **Scheme search:** Find relevant Indian government schemes using natural-language queries.
- **Relevant responses:** Retrieve information related to benefits, eligibility, documents, and application procedures instead of displaying unnecessary full records.
- **Text preprocessing:** Normalize text to improve matching and search quality.
- **TF-IDF-based retrieval:** Represent scheme information as TF-IDF vectors and compare user queries using cosine similarity.
- **Flask web application:** Provide a browser-based interface for interacting with the assistant.
- **Conversation experience:** Support common greetings and a fallback response when a suitable match is not found.
- **Multilingual direction:** The text-processing workflow is designed to preserve Devanagari characters; translation support can be integrated for additional language coverage.

## 🎯 Problem Statement

Information about Indian government schemes is spread across multiple sources and is often difficult for citizens to locate. People may not know which scheme applies to them or where to find details about benefits, eligibility, documents, and application steps.

YojanaGPT addresses this problem by providing a single, conversational search interface that helps users locate relevant scheme information quickly.

## 🧠 How It Works

1. **Dataset loading:** Load the government-schemes dataset into a structured format using Pandas.
2. **Data preparation:** Handle missing values and prepare the available scheme fields.
3. **Text combination:** Combine useful fields such as scheme details, benefits, eligibility, application process, documents, category, and tags into searchable text.
4. **Preprocessing:** Convert text to lowercase and clean it while preserving relevant Devanagari/Marathi Unicode characters.
5. **Vectorization:** Convert the processed scheme text into numerical features using `TfidfVectorizer`.
6. **Similarity matching:** Transform the user's query and calculate cosine similarity against the scheme records.
7. **Response selection:** Select the most relevant scheme information and return a focused response through the Flask application.

## 🏗️ System Architecture

```text
             User
              |
              v
       Flask Web Interface
              |
              v
        User Query Input
              |
              v
       Text Preprocessing
              |
              v
       TF-IDF Vectorization
              |
              v
      Cosine Similarity Search
              |
              v
      Relevant Scheme Retrieval
              |
              v
       Response Generation
              |
              v
        Answer to User
```

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Web framework | Flask |
| Data handling | Pandas |
| Machine learning / NLP utilities | Scikit-learn |
| Text vectorization | TF-IDF |
| Similarity measurement | Cosine similarity |
| Dataset processing | CSV |
| Frontend | HTML, CSS, JavaScript (if included in the project UI) |
| Deployment | Vercel (for the deployed Flask application) |

## 📊 Dataset

The project uses an Indian Government Schemes dataset sourced from Kaggle.

The dataset fields used in the project include:

- `slug`
- `details`
- `benefits`
- `eligibility`
- `application`
- `documents`
- `level`
- `schemeCategory`
- `tags`

A combined text field is prepared from relevant columns to support search and retrieval.

> Dataset source: [Indian Government Schemes – Kaggle](https://www.kaggle.com/datasets/jainamgada45/indian-government-schemes)  
> Check the dataset page for its current terms of use and licensing.

## 📁 Project Structure

The exact filenames may differ depending on your local repository. A typical structure is:

```text
YojanaGPT/
│
├── app.py                  # Flask application
├── model.py                # NLP search / response logic (if separated)
├── updated_data.csv        # Processed scheme dataset
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Chatbot interface
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── .env                    # Local environment variables (do not commit)
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/meghanand786/YojanaGPT_with_flask.git
cd YojanaGPT_with_flask
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, review your local execution-policy settings or activate the environment using Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If your repository does not yet contain a `requirements.txt`, install the packages used by your implementation:

```bash
pip install flask pandas scikit-learn numpy
```

Install any additional packages required by your own code, such as a translation or AI-provider SDK, if configured.

### 4. Configure environment variables

If the application uses an external AI or translation API, create a `.env` file and add the required key:

```env
# Example only — use the variable name expected by your application
API_KEY=your_api_key_here
```

Do not commit `.env` files or expose API keys in source code. If the current version does not use an external API, this step is not required.

### 5. Run the application

```bash
python app.py
```

Open the local URL printed by Flask in your terminal, commonly:

```text
http://127.0.0.1:5000/
```

## 💬 Example Queries

Try questions such as:

- What are the benefits of PM-KISAN?
- Who is eligible for this scheme?
- Which documents are required to apply?
- How can I apply for a government scheme?
- Show schemes related to agriculture.
- ग्रामीण योजनाओं के लाभ क्या हैं? *(Example Hindi query, depending on configured language support.)*

The exact response depends on the information available in the dataset and the retrieval logic.

## 🔍 NLP Techniques Used

### Text preprocessing
- Lowercasing text.
- Cleaning unwanted characters and noise.
- Handling missing dataset values.
- Preserving Devanagari/Marathi Unicode characters where applicable.

### TF-IDF vectorization
`TfidfVectorizer` converts text into numerical vectors and gives greater weight to terms that are useful for distinguishing records.

### Cosine similarity
Cosine similarity compares the user's query vector with scheme vectors to identify the closest textual matches.

## 🚀 Deployment

The project has been deployed using Vercel:

**Live application:** [https://yojana-gpt-with-flask.vercel.app/](https://yojana-gpt-with-flask.vercel.app/)

Deployment configuration and environment variables should match the current repository setup. Keep secret keys and API credentials in the hosting platform's environment-variable settings.

## 🔮 Future Enhancements

- Improve multilingual query handling for Hindi, Marathi, and other Indian languages.
- Add semantic search or a Retrieval-Augmented Generation (RAG) pipeline for better understanding of user intent.
- Add user authentication and secure chat-history storage.
- Integrate PostgreSQL for persistent application data.
- Allow users to save or download conversations as PDF files.
- Add scheme filters based on state, category, income group, and eligibility.
- Include links to official scheme sources and show when information was last verified.
- Improve evaluation using a labelled set of queries and retrieval metrics such as Precision@K and Recall@K.

## ⚠️ Disclaimer

YojanaGPT is an informational project. Scheme eligibility, benefits, required documents, and application procedures may change. Always verify important details with the relevant official government portal or department before applying. A chatbot response should not be treated as an official eligibility decision.

## 👨‍💻 Author

**Meghanand Mahajan**

- GitHub: [@meghanand786](https://github.com/meghanand1028)

## 🙏 Acknowledgements

- Kaggle dataset contributors.
- Open-source Python and NLP communities.
- Flask and Scikit-learn documentation.

---

**Made with ❤️ to make Indian government scheme information easier to access.**
