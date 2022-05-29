# Import libraries
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os.path as path
# Importing dataset
dataset = pd.read_csv(path.join(path.dirname(__file__), 'adult.csv'))

columns_with_nan = ['workclass', 'occupation', 'native.country']
for col in columns_with_nan:
    dataset[col].fillna(dataset[col].mode()[0], inplace = True)

# encoding the data for training proccess
from sklearn.preprocessing import LabelEncoder
for col in dataset.columns:
  if dataset[col].dtypes == 'object':  
    encoder = LabelEncoder()
    dataset[col] = encoder.fit_transform(dataset[col])
    
# Separating what we will get an input from what we want to predict    
X = dataset.drop('income', axis = 1) 
Y = dataset['income']

#Droping the columns we don't get an input for
X = X.drop(['workclass', 'education', 'race', 'sex', 'capital.loss', 'native.country', 'fnlwgt', 'capital.gain', 'relationship'], axis = 1)

#Ressampling the dataset cause it's not balanced
from imblearn.over_sampling import RandomOverSampler 
ros = RandomOverSampler(random_state = 42)
ros.fit(X, Y)
X_resampled, Y_resampled = ros.fit_resample(X, Y)

#training the model
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_resampled, Y_resampled, test_size = 0.2, random_state = 42)
from sklearn.ensemble import RandomForestClassifier
ran_for = RandomForestClassifier(max_depth = 102, n_estimators = 40, random_state = 42)
ran_for.fit(X_train, Y_train)


#those are the labels our model used so it's very important to get them right
labels = {'marital.status':{'Divorced':0, 'Married':1, 'Separated':2,
 'Married-spouse-absent':3, 'Never-married':4, 'Separated':5, 'Widowed':6}, 
          'occupation': {'?': 0, 'Adm-clerical':1, 'Armed-Forces':2, 'Craft-repair':3, 'Exec-managerial':4,
 'Farming-fishing':5, 'Handlers-cleaners':6, 'Machine-op-inspct':7, 'Other-service':8,
 'Priv-house-serv':9, 'Prof-specialty':10, 'Protective-serv':11, 'Sales':12,
 'Tech-support':13, 'Transport-moving':14}}

#the data we get input for in form of a dict
#get arguments from argv
data = {'age': int(sys.argv[1]), 'education.num': int(sys.argv[2]), 'marital.status': sys.argv[3], 'occupation': sys.argv[4], 'hours.per.week': int(sys.argv[5])}

#changing the strings for marital.status and occupation to corresponding labels
data['marital.status'] = labels['marital.status'][data['marital.status']]
data['occupation'] = labels['occupation'][data['occupation']]

#transforming the dict into an array
df = pd.DataFrame(data, index=[0])

#predicing the result
# if it says 0 => the income is less or equal to 50k
# if it says 1 => the income is more than 50k
result = ran_for.predict(df)

print(result[0])