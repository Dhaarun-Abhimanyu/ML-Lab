from pdfminer.high_level import extract_text
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import os

from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from keybert import KeyBERT

def ensure_nltk_resource(resource_path, resource_name):
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(resource_name, quiet=True)


# Download required nltk data (covers newer NLTK punkt_tab split)
ensure_nltk_resource('tokenizers/punkt', 'punkt')
ensure_nltk_resource('tokenizers/punkt_tab', 'punkt_tab')
ensure_nltk_resource('corpora/stopwords', 'stopwords')

# ----------------------------------------
# STEP 1: Extract text from IEEE PDF
# ----------------------------------------

base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_file = os.path.join(base_dir, "sena3.pdf")

if not os.path.exists(pdf_file):
    raise FileNotFoundError(f"PDF file not found: {pdf_file}")

print("Extracting text from PDF...\n")
text = extract_text(pdf_file)

# ----------------------------------------
# STEP 2: Preprocessing
# ----------------------------------------

stop_words = set(stopwords.words('english'))

def preprocess(text):

    text = text.lower()

    tokens = word_tokenize(text)

    clean_words = []

    for word in tokens:
        if word not in stop_words and word not in string.punctuation:
            clean_words.append(word)

    return " ".join(clean_words)

clean_text = preprocess(text)

# ----------------------------------------
# STEP 3: TF-IDF Keyword Extraction
# ----------------------------------------

print("Running TF-IDF...\n")

vectorizer = TfidfVectorizer(max_features=15)

tfidf_matrix = vectorizer.fit_transform([clean_text])

keywords_tfidf = vectorizer.get_feature_names_out()

# ----------------------------------------
# STEP 4: RAKE Keyword Extraction
# ----------------------------------------

print("Running RAKE...\n")

rake = Rake()

rake.extract_keywords_from_text(clean_text)

keywords_rake = rake.get_ranked_phrases()[:10]

# ----------------------------------------
# STEP 5: KeyBERT Keyword Extraction
# ----------------------------------------

print("Running KeyBERT...\n")

kw_model = KeyBERT()

keywords_keybert = kw_model.extract_keywords(
    clean_text,
    keyphrase_ngram_range=(1,2),
    stop_words='english',
    top_n=10
)

# ----------------------------------------
# STEP 6: Print Results
# ----------------------------------------

print("\n=========== KEYWORD EXTRACTION RESULTS ===========")

print("\nTF-IDF Keywords:")
print(keywords_tfidf)

print("\nRAKE Keywords:")
print(keywords_rake)

print("\nKeyBERT Keywords:")
print(keywords_keybert)

print("\nDone!")