import re
import nltk

# Download Nepali sentence tokenizer models or use basic split by punctuation
# For simplicity, we'll split on punctuation marks for Nepali
def split_sentences(text):
    # Simple split on '।' or newline or dot (for Nepali sentences)
    sentences = re.split(r'[।\n]', text)
    return [s.strip() for s in sentences if s.strip()]

def remove_stopwords(text, stopwords):
    words = text.split()
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered)

def clean_text(text):
    # Remove special characters except Nepali alphabets, digits, spaces, punctuation
    text = re.sub(r'[^ऀ-ःक-हअ-औऔ-०-९\s।,.]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
