import re
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


stemmer = PorterStemmer()

STOPWORDS = {
    "the", "is", "are", "was", "were", "a", "an",
    "in", "on", "at", "to", "of", "and", "or",
    "i", "you", "he", "she", "it", "they", "we",
    "what", "who", "where", "when", "how", "why",
    "did", "do", "does", "can", "could", "would",
    "tell", "me", "about", "please", "my", "his",
    "her", "their", "this", "that", "with"
}


def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9:]+\b", text.lower())


def preprocess_text(text):
    words = tokenize(text)

    filtered_words = [
        stemmer.stem(word)
        for word in words
        if word not in STOPWORDS
    ]

    return filtered_words


INTENTS = {
    "greeting": [
        "hello", "hi detective", "hey there",
        "good morning"
    ],
    "suspects": [
        "who are the suspects",
        "show me the suspects",
        "who was present",
        "list all suspects"
    ],
    "clues": [
        "what clues have been found",
        "show me the evidence",
        "tell me the clues",
        "what evidence is available"
    ],
    "location": [
        "where did it happen",
        "where was the incident",
        "what is the crime scene location"
    ],
    "time": [
        "when did it happen",
        "what time was the incident",
        "when was the victim found"
    ],
    "victim": [
        "who is the victim",
        "tell me about the victim",
        "who was attacked"
    ],
    "help": [
        "help me",
        "what can i ask",
        "how do i investigate",
        "what should i do"
    ],
    "hint": [
        "give me a hint",
        "i need a clue",
        "help me solve this mystery"
    ]
}


def classify_intent(text):
    all_examples = []
    all_labels = []

    for intent, examples in INTENTS.items():
        for example in examples:
            all_examples.append(example)
            all_labels.append(intent)

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 4)
    )

    vectors = vectorizer.fit_transform(
        all_examples + [text]
    )

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    best_index = similarities.argmax()
    confidence = similarities[best_index]

    if confidence < 0.18:
        return "unknown"

    return all_labels[best_index]


def extract_entities(text, case):
    entities = []

    for suspect in case["suspects"]:
        if suspect["name"].lower() in text.lower():
            entities.append(suspect["name"])

    time_matches = re.findall(
        r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm)\b",
        text,
        re.IGNORECASE
    )

    entities.extend(time_matches)

    return entities


def analyze_sentiment(text):
    positive_words = {
        "good", "happy", "honest", "helpful",
        "innocent", "calm", "safe"
    }

    negative_words = {
        "angry", "afraid", "guilty", "suspicious",
        "bad", "scared", "lying", "nervous"
    }

    words = set(tokenize(text))

    positive = len(words & positive_words)
    negative = len(words & negative_words)

    if negative > positive:
        return "Negative"

    if positive > negative:
        return "Positive"

    return "Neutral"