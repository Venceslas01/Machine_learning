# -*- coding: utf-8 -*-
"""untitled.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/Venceslas01/d40ef1b91b10b2b1b9ce90e14f4678c5/untitled.ipynb
"""

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

from numpy import arange
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_excel('Data_Pigment.xlsx')
df

#df['Day']=df['Day'].astype('category')
#df['Day']=df['Day'].cat.codes

df.isnull().sum()

#X=df.drop(columns='Chla')
X=df[['Chlb','19Hf','19Bf','Fuco','Perid','Allo','Zea']]
y=df['Chla']
X

# creating train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
y_test

lr=LinearRegression()
lr.fit(X_train,y_train)
m=lr.coef_
print(m)

c=lr.intercept_
c

y_pred_test=lr.predict(X_test)
y_pred_test

plt.scatter(y_test ,y_pred_test )
plt.xlabel('actual charges')
plt.ylabel('Predicted charges')
plt.title('Régression linéaire')
plt.show()

r2_score(y_test,y_pred_test)



X = X_train
Y = y_train

# Standardiser les données pour avoir une moyenne de 0 et un écart type de 1
#Y = np.array((Y - Y.mean()) / Y.std())
#X = X.apply(lambda rec: (rec - rec.mean()) / rec.std(), axis=0)

# Calculer les paramètres de régression en utilisant la méthode des moindres carrés
X_transpose = X.transpose()
X_transpose_X = np.dot(X_transpose, X)
X_transpose_Y = np.dot(X_transpose, Y)
theta = np.dot(np.linalg.inv(X_transpose_X), X_transpose_Y)
b = Y.mean() - np.dot(X.mean(), theta)

# Afficher les paramètres estimés
print('Bias:', b, 'Weights:', theta)

# Prédire les valeurs de Y à l'aide des paramètres estimés
def predict_Y(b,theta,X):
    return b + np.dot(X,theta)
Y_pred =predict_Y(b,theta,X_test)
Y_pred

# Afficher le graphique
plt.scatter(y_test, Y_pred)
plt.xlabel('Valeurs réelles')
plt.ylabel('Valeurs prédites')
plt.title('Régression linéaire multiple - Moindres carrés')
plt.show()

print( 'score_moindre_carrés : ', r2_score(y_test,y_pred_test))

r_square = (sum((y_pred_test - y_test) ** 2)) / (0.3 * 11164)
print(r_square)

# 2_   gradient descente

# Standardiser les données pour avoir une moyenne de 0 et un écart type de 1
#Y=np.array((Y-Y.mean())/Y.std())
#X=X.apply(lambda rec:(rec-rec.mean())/rec.std(),axis=0)
#X.head()
def initialize(dim):
    b=random.random()
    theta=np.random.rand(dim)
    return b,theta

b,theta=initialize(7)
print('Bias: ',b, '\nWeights:' ,theta)

"""# Nouvelle section"""

def predict_Y(b,theta,X):
    return b + np.dot(X,theta)
Y_hat=predict_Y(b,theta,X_test)
Y_hat
import math

def get_cost(Y,Y_hat):
    Y_resd=Y-Y_hat
    return np.sum(np.dot(Y_resd.T,Y_resd))/len(Y-Y_resd)
Y_hat=predict_Y(b,theta,X)
get_cost(Y,Y_hat)
def update_theta(x,y,y_hat,b_0,theta_o,learning_rate):
    db=(np.sum(y_hat-y)*2)/len(y)
    dw=(np.dot((y_hat-y),x)*2)/len(y)
    b_1=b_0-learning_rate*db
    theta_1=theta_o-learning_rate*dw
    return b_1,theta_1
#print("After initialization -Bias: ",b,"theta: ",theta)
Y_hat=predict_Y(b,theta,X)
b,theta=update_theta(X,Y,Y_hat,b,theta,0.01)
#print("After first update -Bias: ",b,"theta: ",theta)
get_cost(Y,Y_hat)
def run_gradient_descent(X,Y,alpha,num_iterations):
    b,theta=initialize(X.shape[1])
    iter_num=0
    gd_iterations_df=pd.DataFrame(columns=['iteration','cost'])
    result_idx=0
    for each_iter in range(num_iterations):
        Y_hat=predict_Y(b,theta,X)
        this_cost=get_cost(Y,Y_hat)
        prev_b=b
        prev_theta=theta
        b,theta=update_theta(X,Y,Y_hat,prev_b,prev_theta,alpha)
        if(iter_num%10==0):
            gd_iterations_df.loc[result_idx]=[iter_num,this_cost]
            result_idx=result_idx+1
        iter_num +=1
  #  print('Final Estimate of b and theta :',b,theta)
    return gd_iterations_df,b,theta
gd_iterations_df,b,theta=run_gradient_descent(X,Y,alpha=0.001,num_iterations=200)
print('Bias: ',b, '\nWeights:' ,theta)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
plt.plot(gd_iterations_df['iteration'],gd_iterations_df['cost'])
plt.xlabel('Number of iterations')
plt.ylabel('Cost or MSE')

alpha_df_1,b,theta=run_gradient_descent(X,Y,alpha=0.01,num_iterations=2000)
alpha_df_2,b,theta=run_gradient_descent(X,Y,alpha=0.001,num_iterations=2000)
plt.plot(alpha_df_1['iteration'],alpha_df_1['cost'],label='alpha=0.01')
plt.plot(alpha_df_2['iteration'],alpha_df_2['cost'],label='alpha=0.001')
plt.legend()
plt.ylabel('cost')
plt.xlabel('Number of iterations')
plt.title('Cost Vs. Iterations for different alpha values')

r_square = (sum((y_pred_test - y_test) ** 2)) / (0.3 * 11164)
print(r_square)

#define cross-validation method to evaluate model
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
#define model
model = RidgeCV(alphas=arange(0.001, 1, 0.01), cv=cv, scoring='neg_mean_absolute_error')
#fit model
model.fit(X,Y)
#display lambda that produced the lowest test MSE
print(model.alpha_)



y_pred_ridge=model.predict(X_test)
print('y_pred_test : ', y_pred_ridge)

# Afficher le graphique
plt.scatter(y_test, y_pred_ridge)
plt.xlabel('Valeurs réelles')
plt.ylabel('Valeurs prédites')
plt.title('Régression linéaire - Ridge')
plt.show()

r_square = (sum((y_pred_ridge - y_test) ** 2)) / (0.3 * 11164)
print(r_square)






