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
from gaze_features import produce_features
from gaze_training import combine_files



if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description='Plotting options')
    parser.add_argument('-plot', help='Generate plots of samples', action='store_true')
    args = parser.parse_args()

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
    else:
        for filename in os.listdir(FEATURESDIR):
            item = os.path.join(FEATURESDIR,filename)
            if os.path.isfile(item): 
                os.remove(item)
    
    # Check if trainind data data directory exists; if not, create it
    if not os.path.isdir(TRAINDATADIR):
        os.mkdir(TRAINDATADIR)
    
    # Check if testing data directory exists; if not, create it
    if not os.path.isdir(TESTDATADIR):
        os.mkdir(TESTDATADIR)
    
    # Check if models directory exists; if not, create it
    if not os.path.isdir(MODELSDIR):
        os.mkdir(MODELSDIR)

    # Experiment specs
    DISPSIZE = (6026, 1080)  # (px, px)
    SCREENSIZE = (39.9, 29.9)  # (cm, cm)
    SCREENDIST = 61.0  # cm
    PXPERCM = numpy.mean(
    [DISPSIZE[0]/SCREENSIZE[0], DISPSIZE[1]/SCREENSIZE[1]])  # px/cm


    filenames = [f for f in os.listdir("data") if not f.startswith('.')]
    filenames.sort()

    for filename in filenames:
        gaze_data = read_files(filename, DATADIR)
        trialnr, fixations, saccades = process_files(filename, gaze_data)
        panda_fix, panda_sac = generate_csv(ENGINEEREDDATADIR, filename, fixations, saccades)
        if args.plot:
            generate_plots(IMGDIR, PLOTDIR, filename, fixations, saccades, gaze_data, DISPSIZE, trialnr)
        for window_size in [15000]:
            for overlap in [70]:
                produce_features(FEATURESDIR, panda_fix, panda_sac, filename, window_size, overlap)

    featured_data = os.listdir(FEATURESDIR)
    random.shuffle(featured_data)
    training_set = featured_data[:14]
    testing_set = featured_data[14:]
    pdb.set_trace()
    combined_features = pandas.concat([pandas.read_csv(os.path.join(FEATURESDIR, f)) for f in os.listdir(FEATURESDIR)], sort=False, ignore_index=True)
    #combined_test.drop('load', axis=1, inplace=True)
    combined_features.to_csv(os.path.join(FEATURESDIR, "combined_features.csv"), index=False)

    #for file in training_set:
    #    os.rename(os.path.join(FEATURESDIR, file), os.path.join(TRAINDATADIR, file))
    #for file in testing_set:
    #    os.rename(os.path.join(FEATURESDIR, file), os.path.join(TESTDATADIR, file))

    #combine_files(TRAINDATADIR, TESTDATADIR)
