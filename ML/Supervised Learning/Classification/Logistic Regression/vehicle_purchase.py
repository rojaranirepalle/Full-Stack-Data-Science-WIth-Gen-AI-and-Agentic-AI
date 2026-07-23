import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

vehicle_purchase = pd.read_csv('vehicle_purchase.csv')

x = vehicle_purchase.iloc[:,[2,3]].values
y = vehicle_purchase.iloc[:,-1].values

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=0)


SS = StandardScaler()
x_train = SS.fit_transform(x_train)
x_test = SS.transform(x_test)


classifier = LogisticRegression()
classifier.fit(x_train,y_train)

y_pred = classifier.predict(x_test)


cm = confusion_matrix(y_test,y_pred)
print(cm)

ac = accuracy_score(y_test, y_pred)
print(ac)

cr = classification_report(y_test,y_pred)
print(cr)

bias = classifier.score(x_train,y_train)
print(bias)

variance = classifier.score(x_test, y_test)
print(variance)

### Future Prediction ###
vehicle_future_pred = pd.read_csv('validation_data.csv')

vehicle_fp = vehicle_future_pred.copy()

dataset = vehicle_fp.iloc[:,[3,4]].values
pre_data = SS.fit_transform(dataset)

vehicle_fp['y_fpred'] = classifier.predict(pre_data)

vehicle_fp.to_csv('validation_data.csv')

from sklearn.metrics import roc_auc_score , roc_curve

y_pred_prob = classifier.predict_proba(x_test)[:,1]

auc_score = roc_auc_score(y_test,y_pred_prob)
print(auc_score)

fpr, tpr, thresholds = roc_curve(y_test,y_pred_prob)

plt.plot(fpr,tpr, color='orange', label='ROC')
plt.plot([0,1],[0,1], color='darkblue', linestyle='--')
plt.xlabel('False Positive Rate')   
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.grid()
plt.show()
