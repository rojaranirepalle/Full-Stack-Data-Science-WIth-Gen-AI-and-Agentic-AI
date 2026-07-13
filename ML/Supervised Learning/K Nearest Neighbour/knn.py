import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

emp_sal = pd.read_csv('emp_sal.csv')

x = emp_sal.iloc[:,1:2].values
y = emp_sal.iloc[:,2].values

### Linear Regression
linear_model = LinearRegression()
linear_model.fit(x,y)

plt.scatter(x, y, color='red')
plt.plot(x,linear_model.predict(x), color='green')
plt.show()

pred_6p5 = linear_model.predict([[6.5]])
pred_6p5
 
### Polynomial Regression
from sklearn.preprocessing import PolynomialFeatures

poly_reg = PolynomialFeatures(degree=5)
X_poly = poly_reg.fit_transform(x)

linear_model_poly = LinearRegression()
linear_model_poly.fit(X_poly,y)

plt.scatter(x, y, color='red')
plt.plot(x,linear_model_poly.predict(X_poly), color='green')
plt.show()

pred_6p5_p = linear_model_poly.predict(poly_reg.fit_transform([[6.5]]))
pred_6p5_p

### SVR

from sklearn.svm import SVR

sv_regressor = SVR(kernel="poly",degree=4,gamma="auto")
sv_regressor.fit(x,y)

pred_6p5_svr = sv_regressor.predict([[6.5]])
pred_6p5_svr


plt.scatter(x, y, color='red')
plt.plot(x,sv_regressor.predict(x), color='green')
plt.show()

### KNN
from sklearn.neighbors import KNeighborsRegressor

knn_regressor = KNeighborsRegressor()
knn_regressor.fit(x,y)


pred_6p5_knn = knn_regressor.predict([[6.5]])
pred_6p5_knn
#####
knn_regressor_hp =  KNeighborsRegressor(n_neighbors=2,weights="distance", algorithm="brute",p=2)
knn_regressor_hp.fit(x,y)


pred_6p5_knn_hp = knn_regressor_hp.predict([[6.5]])
pred_6p5_knn_hp

####
knn_regressor_hp =  KNeighborsRegressor(n_neighbors=2)
knn_regressor_hp.fit(x,y)


pred_6p5_knn_hp = knn_regressor_hp.predict([[6.5]])
pred_6p5_knn_hp

#### Tree Algorithm

from sklearn.tree import DecisionTreeRegressor

DT_regressor = DecisionTreeRegressor()
DT_regressor.fit(x,y)

pred_6p5_dt_hp = DT_regressor.predict([[6.5]])
pred_6p5_dt_hp


#### Tree Algorithm

from sklearn.ensemble import RandomForestRegressor

RF_regressor = RandomForestRegressor(n_estimators=8, random_state=0)
RF_regressor.fit(x,y)

pred_6p5_rf_hp = RF_regressor.predict([[6.5]])
pred_6p5_rf_hp

