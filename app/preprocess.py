import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Pre-compile regular expressions for faster processing
url_pattern = re.compile(r"https?://\S+|www\.\S+")
html_pattern = re.compile(r"<.*?>|&amp;|&quot;|&lt;|&gt;")
mention_pattern = re.compile(r"@\w+")
hashtag_pattern = re.compile(r"#\w+")
alphabetic_pattern = re.compile(r"[^a-zA-Z\s]")
extra_spaces_pattern = re.compile(r"\s+")

# Ensure NLTK resources are downloaded quietly on initialization
nltk_resources = ['stopwords', 'wordnet', 'omw-1.4']
for resource in nltk_resources:
    try:
        nltk.data.find(f'corpora/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

# Define negation words to preserve in sentiment analysis
negation_words = {
    'not', 'no', 'never', 'nor', 'neither', 'against', 'but',
    'don', "don't", 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't",
    'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
    'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

# Cache stopwords (excluding negations) and lemmatizer instance
stop_words = set(stopwords.words('english')) - negation_words
lemmatizer = WordNetLemmatizer()

def preprocess_text(text: str) -> str:
    """
    Cleans and preprocesses raw tweet text.
    Matches exactly the preprocessing pipeline used in training.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = url_pattern.sub('', text)
    
    # 3. Remove HTML entities and tags
    text = html_pattern.sub('', text)
    
    # 4. Remove @mentions
    text = mention_pattern.sub('', text)
    
    # 5. Remove hashtags
    text = hashtag_pattern.sub('', text)
    
    # 6. Remove numbers and punctuation
    text = alphabetic_pattern.sub('', text)
    
    # 7. Tokenize, remove stopwords, and lemmatize (preserve 'no' despite length 2)
    words = text.split()
    cleaned_words = [
        lemmatizer.lemmatize(word) for word in words 
        if word not in stop_words and (len(word) > 2 or word == 'no')
    ]

    
    # 8. Join back and clean extra whitespace
    cleaned_text = ' '.join(cleaned_words)
    return extra_spaces_pattern.sub(' ', cleaned_text).strip()
