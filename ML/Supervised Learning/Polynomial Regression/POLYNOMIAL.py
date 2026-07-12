import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

emp_sal = pd.read_csv('emp_sal.csv')

x = emp_sal.iloc[:,1:2].values
y = emp_sal.iloc[:,2].values

linear_model = LinearRegression()
linear_model.fit(x,y)

plt.scatter(x, y, color='red')
plt.plot(x,linear_model.predict(x), color='green')
plt.show()

pred_6p5 = linear_model.predict([[6.5]])
pred_6p5

### Polynomial
from sklearn.preprocessing import PolynomialFeatures

poly_reg = PolynomialFeatures()
X_poly = poly_reg.fit_transform(x)

linear_model_poly = LinearRegression()
linear_model_poly.fit(X_poly,y)

plt.scatter(x, y, color='red')
plt.plot(x,linear_model_poly.predict(X_poly), color='green')
plt.show()

pred_6p5_p = linear_model_poly.predict(poly_reg.fit_transform([[6.5]]))
pred_6p5_p

### polynomial degree 3 

poly_reg_d3 = PolynomialFeatures(degree=5)
X_poly_3 = poly_reg_d3.fit_transform(x)

linear_model_poly_d3 = LinearRegression()
linear_model_poly_d3.fit(X_poly_3,y)

plt.scatter(x, y, color='red')
plt.plot(x,linear_model_poly_d3.predict(X_poly_3), color='green')
plt.show()

pred_6p5_p_d3 = linear_model_poly_d3.predict(poly_reg_d3.fit_transform([[6.5]]))
pred_6p5_p_d3
