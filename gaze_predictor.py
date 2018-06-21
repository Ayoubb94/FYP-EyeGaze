import os, pandas, pdb
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
import pickle

def load_model(model_name):
    # Load from file
    with open(model_name, 'rb') as file:  
    	pickle_model = pickle.load(file)
    return pickle_model

def classify_new(model, new_X):
    prediction = model.predict(new_X)