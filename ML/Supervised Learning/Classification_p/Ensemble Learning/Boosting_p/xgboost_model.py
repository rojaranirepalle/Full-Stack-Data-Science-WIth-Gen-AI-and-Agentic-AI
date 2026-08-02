import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

vehicle_purchase = pd.read_csv('Churn_Modelling.csv')

x = vehicle_purchase.iloc[:,3:-1].values
y = vehicle_purchase.iloc[:,-1].values

le = LabelEncoder()

x[:,2] = le.fit_transform(x[:,2])

print(x)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

ct = ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[1])],remainder='passthrough')

x = np.array(ct.fit_transform(x))


x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.20,random_state=0)


from xgboost import XGBClassifier

classfier = XGBClassifier()

classfier.fit(x_train,y_train)
y_pred=classfier.predict(x_test)

cm = confusion_matrix(y_test,y_pred)
print(cm)

ac = accuracy_score(y_test, y_pred)
print(ac)

cr = classification_report(y_test,y_pred)
print(cr)

bias = classfier.score(x_train,y_train)
print(bias)

variance = classfier.score(x_test, y_test)
print(variance)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classfier, X=x_train, y=y_train, cv=100)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
