import os, pandas, pdb
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
import pickle


def read_data(FEATURESDIR):
    training_data = pandas.read_csv(os.path.join(FEATURESDIR, "combined_features.csv"))
    #training_data = training_data[pandas.to_numeric(training_data['avg_distsac'], errors='coerce').notnull()]
    #training_data.to_csv(os.path.join(FEATURESDIR, "text_new.csv"), index=False)
    X = training_data.drop('load', axis=1)
    y = training_data['load']

    return X, y    


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
    parameters = [{'kernel': ['rbf'],
               'gamma': [1e-4, 1e-3, 0.01, 0.1, 0.2, 0.5],
                'C': [1, 10, 100, 1000]},
              {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    #svclassifier = SVC(kernel='linear')
    svclassifier = GridSearchCV(svm.SVC(decision_function_shape='ovr'), parameters, cv=5)
    #svclassifier = SVC(kernel='linear', C=1, gamma=10)  
    svclassifier.fit(X_train, y_train)
    print(svclassifier.best_params_)
    

    print("Grid scores on training set:")

    means = svclassifier.cv_results_['mean_test_score']
    stds = svclassifier.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, svclassifier.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))

    y_pred = svclassifier.predict(X_test)
    print(confusion_matrix(y_test,y_pred))  
    print(classification_report(y_test,y_pred))

    return svclassifier


def save_model(model, MODELSDIR):
    model_name = os.path.join(MODELSDIR, "trained_pickle.pkl")
    with open(model_name, 'wb') as file:
        pickle.dump(model, file)
    return model_name