# main file of the custom Python pipeline to do the following steps:
# 1. Read raw eyegaze data and calculate fixations, saccades
# 2. Process and prepare eyegaze data, and generate plots
# 3. Produce a combination of features to train a ML model
# 4. Prepare training data and train model
# 5. Prepare test data and test model
# 6. Use model to predict mental workload
# Sunday, 17th June, 2018
# Author: Ayoub Bessasso

import os, pdb, pandas
import argparse
import random
import numpy
from gaze_reader import read_files
from gaze_processor import process_files, generate_csv, generate_plots
from gaze_features import produce_features, combine_features
from gaze_training import read_data, train_model, save_model
from gaze_predictor import load_model, classify_new

def train_only():
    X, y = read_data(FEATURESDIR)
    model = train_model(X, y)
    model_name = save_model(model, MODELSDIR)


def predict_only():
    if os.listdir(UNSEENDIR) == []:
        print("No new data to predict!")
    elif len(os.listdir(MODELSDIR)) != 1:
        print("There is no trained model, or there are multiple models")
    else:
        model_name = os.path.join(MODELSDIR, "trained_pickle.pkl")
        saved_model = load_model(model_name)
        pdb.set_trace()
        new_X, new_y = read_data(UNSEENDIR)
        classify_new(save_model, new_X)


def default_pipeline():

    filenames = [f for f in os.listdir("data") if not f.startswith('.')]
    filenames.sort()

    for filename in filenames:
        gaze_data = read_files(filename, DATADIR)
        trialnr, fixations, saccades = process_files(filename, gaze_data)
        panda_fix, panda_sac = generate_csv(ENGINEEREDDATADIR, filename, fixations, saccades)
        if args.plot:
            generate_plots(IMGDIR, PLOTDIR, filename, fixations, saccades, gaze_data, DISPSIZE, trialnr)
        for window_size in [15000]:
            for overlap in [75]:
                produce_features(FEATURESDIR, panda_fix, panda_sac, filename, window_size, overlap)

    if not os.path.exists(FEATURESDIR + '/combined_features.csv'):
        combine_features(FEATURESDIR)

    X, y = read_data(FEATURESDIR)
    model = train_model(X, y)
    model_name = save_model(model, MODELSDIR)


if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description='Plotting options')
    parser.add_argument('-plot', help='Generate plots of samples', action='store_true')
    parser.add_argument('-train_only', help='Train model without processing data', action='store_true')
    parser.add_argument('-predict_only', help='Use trained model to predict new data', action='store_true')
    args = parser.parse_args()

    # Directories and paths
    DIR = os.path.dirname(os.path.abspath(__file__))
    DATADIR = os.path.join(DIR, 'data')
    IMGDIR = os.path.join(os.path.dirname(__file__), 'imgs')
    PLOTDIR = os.path.join(DIR, 'plots')
    ENGINEEREDDATADIR = os.path.join(DIR, 'engineered_data')
    FEATURESDIR = os.path.join(DIR, 'features')
    MODELSDIR = os.path.join(DIR, 'models')
    UNSEENDIR = os.path.join(DIR, 'unseen_data')

    # Check if data directory exists
    if not os.path.isdir(DATADIR):
        raise Exception(
            "ERROR: no data dir found; path '%s' does not exist!" % DATADIR)

    # check if the image directory exists
    if not os.path.isdir(IMGDIR):
        raise Exception(
            "ERROR: no image directory found; path '%s' does not exist!" % IMGDIR)
    
    # Check if plots directory exists; if not, create it
    if not os.path.isdir(PLOTDIR):
        os.mkdir(PLOTDIR)

    # Check if engineered data directory exists; if not, create it
    if not os.path.isdir(ENGINEEREDDATADIR):
        os.mkdir(ENGINEEREDDATADIR)
    else:
        for filename in os.listdir(ENGINEEREDDATADIR):
            item = os.path.join(ENGINEEREDDATADIR,filename)
            if os.path.isfile(item): 
                os.remove(item)
    
    # Check if features directory exists; if not, create it
    if not os.path.isdir(FEATURESDIR):
        os.mkdir(FEATURESDIR)
    #else:
    #    for filename in os.listdir(FEATURESDIR):
    #        item = os.path.join(FEATURESDIR,filename)
    #        if os.path.isfile(item): 
    #            os.remove(item)
    
    # Check if models directory exists; if not, create it
    if not os.path.isdir(MODELSDIR):
        os.mkdir(MODELSDIR)

    # Check if unseen_data directory exists; if not, create it
    if not os.path.isdir(UNSEENDIR):
        os.mkdir(UNSEENDIR)

    # Experiment specs
    DISPSIZE = (6026, 1080)  # (px, px)
    SCREENSIZE = (39.9, 29.9)  # (cm, cm)
    SCREENDIST = 61.0  # cm
    PXPERCM = numpy.mean(
    [DISPSIZE[0]/SCREENSIZE[0], DISPSIZE[1]/SCREENSIZE[1]])  # px/cm

    if args.train_only:
        train_only()
    elif args.predict_only:
        predict_only()
    else:
        default_pipeline()
