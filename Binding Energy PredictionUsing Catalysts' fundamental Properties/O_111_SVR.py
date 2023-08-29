import os, sys
import numpy as np
import pandas as pd
from math import sqrt
from sklearn.svm import SVR
from joblib import load, dump
from sklearn import model_selection
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import GradientBoostingRegressor


dirname = os.path.dirname(__file__)
# dirname = '/Users/shivanshu/Desktop/Sem IX/MTP'
sys.path.insert(0, dirname)
filename = os.path.join(dirname, 'O_111_featured_data.csv')
SVR_model_name = os.path.join(dirname, 'SVR_O_111.pickle')


data = pd.read_csv(filename)
data = data.drop(['Unnamed: 0'],axis=1)
data.dropna(inplace=True)
data  = data.loc[data['B.E.']<0]
Y = data.loc[:,'B.E.'].values
X = data.loc[:, 'AN' : "SE'"].values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, shuffle=True)


def Best_estimator_grid(X, Y, clf, params, cv):
    """ Returns the best estimator from a dictionary of parameters"""
    print("Within Best_estimator")
    clf_grid = GridSearchCV(clf, params, cv=cv, n_jobs=4, verbose=10)
    clf_grid.fit(X, Y)
    return clf_grid


clf = SVR(verbose=True)
params = {'C': [ 1, 10, 50, 100],
           'kernel' : [ 'rbf','poly','linear', 'sigmoid' ],
           'gamma' : ['auto', 'scale']     }

# params = {'C': [ 1],
#            'kernel' : [ 'rbf' ],
#            'gamma' : ['auto']     }


print("Finding optimal SVR model ............")

optimal_model = Best_estimator_grid(X_train, y_train, clf, params, 5)
best_model = optimal_model.best_estimator_
print("Optimal Model of SVR is" , best_model)
dump(best_model, os.path.join(dirname, SVR_model_name))
print("Model has been dumped Successfully !!!")
print("Finding root mean square error ............")


best_model.fit(X_train,y_train)
y_train_predicted = best_model.predict(X_train)
y_test_predicted = best_model.predict(X_test)


def percent_error(y_true, y_pred):
       error  = (y_true - y_pred)/y_true
       error = np.square(error)
       error = np.sqrt(error)
       outliners = 0
       for i in range(0, len(error)):
              if abs(error[i]) > 1:
                     # print('here')
                     outliners = outliners+1
                     error[i] = 0
       ans = np.sum(error)
       ans = ans/len(error)
       return ans, outliners

percent_train, outliner_train = percent_error(y_train, y_train_predicted)
percent_test, outliner_test = percent_error(y_test, y_test_predicted)


errors=[]
errors_train=[]
error_list=[]
error_all_i=np.zeros(24)
for i in range(0,100):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle=True)
    best_model.fit(X_train, y_train)
    y_train_predicted=best_model.predict(X_train)
    y_test_predicted=best_model.predict(X_test)

    # Later find which values create most errors
    errors.append(sqrt(mean_squared_error(y_test, y_test_predicted)))
    errors_train.append(sqrt(mean_squared_error(y_train, y_train_predicted)))
    print(i)
    

print ("Train Error" + str(sum(errors_train)/float(len(errors_train)))) 
print ("Test Error" + str(sum(errors)/float(len(errors))))


with open('SVR_O_111_results.txt', 'w') as f:
    print('Test_error:', str(sum(errors)/float(len(errors))), file=f)  # Python 3.x
    print('Train_error:', str(sum(errors_train)/float(len(errors_train))), file=f)  # Python 3.x
    print('R square score for test data is ',str(best_model.score(X_test, y_test)), file=f)
    print('R square score for train data is ',str(best_model.score(X_train, y_train)), file=f)
    print ("Percentage Train Error", percent_train*100, "% with", outliner_train, "of",len(y_train), "outliner points", file=f) 
    print ("Percentage Test Error", percent_test*100, "% with", outliner_test,"of",len(y_test), "outliner points", file=f)


