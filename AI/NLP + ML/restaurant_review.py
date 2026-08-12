import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('/Users/rojarani/Documents/AIML/NIT/FSDS/Class Notes/06_Aug_2026/6th - NLP project/4.CUSTOMERS REVIEW DATASET/Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpus = []

for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(corpus).toarray()

y = dataset.iloc[:, 1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(corpus, y,
                                                    test_size = 0.20,
                                                    random_state = 0)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)


# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance



from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)


# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance


from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(C=1.0, max_iter=1000)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance


from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)   
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance


from xgboost import XGBClassifier
classifier = XGBClassifier()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance

from sklearn.ensemble import GradientBoostingClassifier
classifier = GradientBoostingClassifier()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance


from sklearn.ensemble import AdaBoostClassifier
classifier = AdaBoostClassifier()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = classifier.score(X_train,y_train)
bias

variance = classifier.score(X_test,y_test)
variance


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import VotingClassifier

# 1. Advanced Vectorization (Captures context better)
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 2. Ensemble Strategy (Combines the strengths of both models)
clf1 = LogisticRegression(C=1.0, max_iter=1000)
clf2 = LinearSVC(C=0.5)

# A voting classifier mitigates individual model weaknesses
ensemble_model = VotingClassifier(estimators=[('lr', clf1), ('svm', clf2)], voting='hard')
ensemble_model.fit(X_train_vec, y_train)

y_pred = ensemble_model.predict(X_test_vec)

ac = accuracy_score(y_test, y_pred)
print(ac)
  
bias = ensemble_model.score(X_train_vec,y_train)
bias

variance = ensemble_model.score(X_test_vec,y_test)
variance