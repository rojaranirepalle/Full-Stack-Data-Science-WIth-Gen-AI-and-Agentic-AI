import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

vehicle_purchase = pd.read_csv('vehicle_purchase.csv')

x = vehicle_purchase.iloc[:,[2,3]].values
y = vehicle_purchase.iloc[:,-1].values

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=0)

### Decision tree not required scaling

SS = StandardScaler()
x_train = SS.fit_transform(x_train)
x_test = SS.transform(x_test)



### Multinomial 
from sklearn.tree import DecisionTreeClassifier

classfier = DecisionTreeClassifier(criterion='gini',splitter='best',max_depth=100)
classfier.fit(x_train,y_train)


y_pred = classfier.predict(x_test)
y_pred


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


### RandomForestClassifier 
from sklearn.ensemble import RandomForestClassifier

classfier = RandomForestClassifier(max_depth=4, n_estimators=30, criterion='entropy', random_state=0)
classfier.fit(x_train,y_train)


y_pred = classfier.predict(x_test)
y_pred


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