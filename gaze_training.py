import os, pandas, pdb
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle


def combine_files(TRAINDATADIR, TESTDATADIR):
	combined_csv = pandas.concat([pandas.read_csv(os.path.join(TRAINDATADIR, f)) for f in os.listdir(TRAINDATADIR)], sort=False, ignore_index=True)
	combined_csv.to_csv(os.path.join(TRAINDATADIR, "combined_training.csv"), index=False)

	combined_test = pandas.concat([pandas.read_csv(os.path.join(TESTDATADIR, f)) for f in os.listdir(TESTDATADIR)], sort=False, ignore_index=True)
	#combined_test.drop('load', axis=1, inplace=True)
	combined_test.to_csv(os.path.join(TESTDATADIR, "combined_test.csv"), index=False)


def read_data(TRAINDATADIR):
    training_data = pandas.read_csv(os.path.join(FEATURESDIR, "combined_features.csv"), sep='\t')
    training_data = training_data[pandas.to_numeric(training_data['avg_distsac'], errors='coerce').notnull()]
    #training_data.to_csv(os.path.join(FEATURESDIR, "text_new.csv"), index=False)
    #pdb.set_trace()
    X = training_data.drop('load', axis=1)
    y = training_data['load']
    
    #pdb.set_trace()
    #y[pandas.to_numeric(y['load'], errors='coerce').notnull()]
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
    print()
    means = svclassifier.cv_results_['mean_test_score']
    stds = svclassifier.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, svclassifier.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    y_pred = svclassifier.predict(X_test)
    print(confusion_matrix(y_test,y_pred))  
    print(classification_report(y_test,y_pred))
    #pdb.set_trace()


def train_model():

	pass


if __name__ == "__main__":
	# Directories and paths
    DIR = os.path.dirname(os.path.abspath(__file__))
    DATADIR = os.path.join(DIR, 'data')
    IMGDIR = os.path.join(os.path.dirname(__file__), 'imgs')
    PLOTDIR = os.path.join(DIR, 'plots')
    ENGINEEREDDATADIR = os.path.join(DIR, 'engineered_data')
    FEATURESDIR = os.path.join(DIR, 'features')
    TRAINDATADIR = os.path.join(DIR, 'train_data')
    TESTDATADIR = os.path.join(DIR, 'test_data')
    MODELSDIR = os.path.join(DIR, 'models')

    read_data(TRAINDATADIR)