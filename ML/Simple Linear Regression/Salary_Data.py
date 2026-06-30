#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:00:31 2026
Phase 2 : Simple Linear Regression
@author: rojarani
"""

import pandas as pd

sal_data = pd.read_csv('Salary_Data.csv')

x = sal_data.iloc[:,:-1]
y = sal_data.iloc[:,-1]

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)

from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
regressor.fit(x_train,y_train)

y_pred = regressor.predict(x_test)

import matplotlib.pyplot as plt

plt.scatter(x_test,y_test,color="red")
plt.plot(x_train,regressor.predict(x_train),color="blue")
plt.title("Salary Predection")
plt.xlabel("Year of experience")
plt.ylabel("salary")
plt.show()

m_coef = regressor.coef_
c_intercept = regressor.intercept_

y_12 = m_coef*12+c_intercept
print(y_12)