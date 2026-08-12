import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Load dataset
dataset = pd.read_csv('/Users/rojarani/Documents/AIML/NIT/FSDS/Class Notes/06_Aug_2026/6th - NLP project/4.CUSTOMERS REVIEW DATASET/Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

# 2. FIX THE STOPWORDS: Keep words that dictate critical sentiment shifts
negation_words = {'not', 'no', 'never', 'neither', 'nor', 'but', 'against', 'isnt', 'wasnt', 'arent', 'werent'}
custom_stopwords = set(stopwords.words('english')) - negation_words

corpus = []
ps = PorterStemmer()

# 3. Clean text cleanly (keeping context)
for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    # Stem and remove stopwords, while preserving negation words
    review = [ps.stem(word) for word in review if word not in custom_stopwords]
    review = ' '.join(review)
    corpus.append(review)

# 4. Train-Test Split using the TEXT corpus directly (Do NOT vectorize here!)
X_train, X_test, y_train, y_test = train_test_split(corpus, dataset.iloc[:, 1].values, 
                                                    test_size = 0.20, 
                                                    random_state = 0)

# 5. Pipeline with aggressive capacity settings to eliminate High Bias
pipeline_svc = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 3),       # Crucial: captures phrases like "not good" or "not worth it"
        min_df=1,                 # Dataset is small (1000 reviews), keep features
        sublinear_tf=True
    )),
    ('svc', LinearSVC(
        C=1.5,                    # Lower regularization to fit data tighter
        class_weight='balanced', 
        max_iter=5000, 
        random_state=42
    ))
])

# 6. Fit and Evaluate
pipeline_svc.fit(X_train, y_train)

print("New Accuracy:", pipeline_svc.score(X_test, y_test))
print("\nClassification Report:\n", classification_report(y_test, pipeline_svc.predict(X_test)))
