# ==========================================================
# Customer Review Sentiment Analysis using TF-IDF + Linear SVM
# ==========================================================

import re
import nltk
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ----------------------------------------------------------
# Download NLTK stopwords (Run only once)
# ----------------------------------------------------------
nltk.download("stopwords")

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------
dataset = pd.read_csv(
    "/Users/rojarani/Documents/AIML/NIT/FSDS/Class Notes/06_Aug_2026/6th - NLP project/4.CUSTOMERS REVIEW DATASET/Restaurant_Reviews.tsv",
    delimiter="\t",
    quoting=3
)

# ----------------------------------------------------------
# Preserve important negation words
# ----------------------------------------------------------
negation_words = {
    "not", "no", "never", "nor",
    "neither", "but"
}

custom_stopwords = set(stopwords.words("english")) - negation_words

ps = PorterStemmer()

# ----------------------------------------------------------
# Text Cleaning
# ----------------------------------------------------------
corpus = []

for review in dataset["Review"]:

    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower()
    review = review.split()

    review = [
        ps.stem(word)
        for word in review
        if word not in custom_stopwords
    ]

    corpus.append(" ".join(review))

# ----------------------------------------------------------
# Train-Test Split
# ----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    corpus,
    dataset["Liked"],
    test_size=0.20,
    random_state=0,
    stratify=dataset["Liked"]
)

# ----------------------------------------------------------
# Build Pipeline
# ----------------------------------------------------------
model = Pipeline([

    ("tfidf",
     TfidfVectorizer(
         max_features=3000,
         ngram_range=(1,2),
         sublinear_tf=True
     )
    ),

    ("classifier",
     LinearSVC(
         C=1.5,
         class_weight="balanced",
         max_iter=5000,
         random_state=42
     )
    )
])

# ----------------------------------------------------------
# Train Model
# ----------------------------------------------------------
model.fit(X_train, y_train)

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------
y_pred = model.predict(X_test)

# ----------------------------------------------------------
# Evaluation
# ----------------------------------------------------------
print("="*60)
print("Customer Review Sentiment Analysis")
print("="*60)

print(f"\nAccuracy : {accuracy_score(y_test, y_pred)*100:.2f}%")

print("\nClassification Report")
print(classification_report(y_test, y_pred))

print("Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

# ----------------------------------------------------------
# Test on New Reviews
# ----------------------------------------------------------
reviews = [

    "The food was delicious and service was excellent.",

    "Worst restaurant ever. Waste of money.",

    "Food was not good.",

    "Amazing ambience and friendly staff.",

    "I will never visit this restaurant again.",

    "The pizza was tasty and worth the price."
]

predictions = model.predict(reviews)

print("\n" + "="*60)
print("Custom Predictions")
print("="*60)

for review, prediction in zip(reviews, predictions):

    sentiment = "Positive 😊" if prediction == 1 else "Negative 😞"

    print(f"\nReview     : {review}")
    print(f"Prediction : {sentiment}")