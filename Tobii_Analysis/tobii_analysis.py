# Analysis script for tobii eyegaze data, based on the analysis
# script written by Edwin Dalmaijer.
# Sunday, 27th May, 2018

__author__ = "Ayoub Bessasso"

# Native
import os

# Custom
from pygazeanalyser.detectors import blink_detection, fixation_detection, \
    saccade_detection
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, \
    draw_scanpath, draw_raw

# External
import numpy
import copy
import argparse
import pandas
import pdb


def read_tobii(filename, reduced, missing=0.0, debug=False):
    """Returns a list with dicts for every trial. A trial dict contains the
    following keys:
        x		-	numpy array of x positions
        y		-	numpy array of y positions
        time		-	numpy array of timestamps
        events	-	dict with the following keys:
            Sfix	-	list of lists, each containing [starttime]
            Ssac	-	list of lists, each containing [starttime]
            Sblk	-	EMPTY! list of lists, each containing [starttime]
            Efix	-	list of lists, each containing \
                        [starttime, endtime, duration, endx, endy]
            Esac	-	list of lists, each containing \
                        [starttime, endtime, dur, startx, starty, endx, endy]
            Eblk	-	EMPTY! list of lists, each containing [starttime, endtime, dur]
            msg	    -	list of lists, each containing [time, message]

    Args:
        filename	-   path to the file that has to be read

    Kwargs:
        missing	    -	value to be used for missing data (default = 0.0)
        debug	    -	Boolean indicating if DEBUG mode should be on or off;
                            if DEBUG mode is on, information on what the script
                            currently is doing will be printed to the console
                            (default = False)

    Returns
        data		-	a list with a dict for every trial (see above)
    """

    # debug mode
    if debug:
        def message(msg):
            print(msg)
    else:
        def message(msg):
            pass

    # check if the file exists
    if os.path.isfile(filename):
        # open file
        message("opening file '%s'" % filename)
        f = open(filename, 'r')
    # raise exception if the file does not exist
    else:
        raise Exception(
            "Error in read_eyetribe: file '%s' does not exist" % filename)

    # read file contents
    message("reading file '%s'" % filename)
    raw = f.readlines()

    # close file
    message("closing file '%s'" % filename)
    f.close()

    # variables
    data = []
    time = []
    x = []
    y = []
    events = {'Sfix': [], 'Ssac': [], 'Sblk': [],
              'Efix': [], 'Esac': [], 'Eblk': [], 'msg': []}

    if reduced:
        limit = 5000
    else:
        limit = len(raw)
    # loop through all lines
    for i in range(limit):

        # string to list
        line = [float(s) for s in raw[i].replace('\n', '').split(',')]
        line[0] = line[0] * 1000
        # line[1] = line[1] - 1920  # Correcting for display to the left

        # see if current line contains relevant data
        try:
            # extract data
            time.append(line[0])
            x.append(line[1])
            y.append(line[2])
        except IndexError:
            message("line '%s' could not be parsed" % line)
            continue  # skip this line

    message("%d samples found" % (len(raw)))
    message("plotting %d samples" % (limit))
    # trial dict
    trial = {}
    trial['x'] = numpy.array(x)
    trial['y'] = numpy.array(y)
    trial['time'] = numpy.array(time)
    trial['events'] = copy.deepcopy(events)
    # events
    trial['events']['Sblk'], trial['events']['Eblk'] = blink_detection(
        trial['x'], trial['y'], trial['time'], missing=missing)
    trial['events']['Sfix'], trial['events']['Efix'] = fixation_detection(
        trial['x'], trial['y'], trial['time'], missing=missing)
    trial['events']['Ssac'], trial['events']['Esac'] = saccade_detection(
        trial['x'], trial['y'], trial['time'], missing=missing)
    # add trial to data
    data.append(trial)

    return data


def read_files(reduced, csvonly):

    # Loop through all files
    for ppname in PPS:
        print("loading gaze data")

        # path
        fp = os.path.join(DATADIR, '%s.tsv' % ppname)

        # check if the path exist
        if not os.path.isfile(fp):
            raise Exception(
                "No eye data file file found for participant '%s'" % (ppname))

        # read the file
        tobiidata = read_tobii(fp, reduced, missing=0.0, debug=True)

        #save_csv(tobiidata)

        pplotdir = os.path.join(PLOTDIR, ppname[:3])

        if not csvonly:
            print("plotting gaze data")

        # Loop through trials
        for trialnr in range(len(tobiidata)):

            # Load image name, saccades, and fixations
            imgname = "screenshot.jpg"
            imagefile = os.path.join(IMGDIR,imgname)
            print(imagefile)
            # [starttime, endtime, duration, startx, starty, endx, endy]
            saccades = tobiidata[trialnr]['events']['Esac']
            # [starttime, endtime, duration, endx, endy]
            fixations = tobiidata[trialnr]['events']['Efix']

            # cognitive load
            if int(ppname[4:5]) == 1:
                cognitive_load = "LOW"
            else:
                cognitive_load = "HIGH"
            if reduced:
                suffix = "_reduced"
            else:
                suffix = ""
            
            # Save the fixation and saccades in csv format for MATLAB
            save_csv(fixations, saccades, ppname, suffix)

            if not csvonly:
                # paths
                rawplotfile = os.path.join(
                    pplotdir,
                    "raw_data_%s_%s%s" % (ppname[:3], cognitive_load, suffix))
                scatterfile = os.path.join(
                    pplotdir,
                    "fixations_%s_%s%s" % (ppname[:3], cognitive_load, suffix))
                scanpathfile = os.path.join(
                    pplotdir,
                    "scanpath_%s_%s%s" % (ppname[:3], cognitive_load, suffix))
                heatmapfile = os.path.join(
                    pplotdir,
                    "heatmap_%s_%s%s" % (ppname[:3], cognitive_load, suffix))


                # raw data points
                draw_raw(
                    tobiidata[trialnr]['x'], tobiidata[trialnr]['y'],
                    DISPSIZE, imagefile=None, savefilename=rawplotfile)

                # fixations
                draw_fixations(
                    fixations, DISPSIZE, imagefile=None, durationsize=True,
                    durationcolour=False, alpha=0.5, savefilename=scatterfile)

                # scanpath
                draw_scanpath(
                    fixations, saccades, DISPSIZE, imagefile=None,
                    alpha=0.5, savefilename=scanpathfile)

                # heatmap
                draw_heatmap(
                    fixations, DISPSIZE, imagefile=None,
                    durationweight=True, alpha=0.5, savefilename=heatmapfile)


def set_directories(filenames):
    # Add function description, and change this to be more universal
    for name in filenames:
        p_dir = os.path.join(PLOTDIR, name[:3])
        if not os.path.isdir(p_dir):
            os.mkdir(p_dir)


def process_data(panda_fix, panda_sac, name):
    # This function should create a new data frame with data divided into 10s windows
    # With averaged fixation duration, mean of horizontal fixation postion,
    # mean of vertical fixation position, mean saccade speed or dur, and mean saccade distance
    # merge into panda_both, merge into panda_new

    panda_new = pandas.DataFrame()

    start_time = int(min(panda_fix.iloc[0,0], panda_sac.iloc[0,0]))
    while True:
        end_time = int(start_time + 10000)
        window_fix = panda_fix.loc[panda_fix['Sfix'].isin(range(start_time, end_time))]
        window_sac = panda_sac.loc[panda_sac['Ssac'].isin(range(start_time, end_time))]

        if window_fix.empty or window_sac.empty:
            break

        avg_durfix = window_fix['Durfix'].mean()
        avg_xfix = window_fix['endxfix'].mean()
        avg_yfix = window_fix['endyfix'].mean()
        avg_dursac = window_sac['Dursac'].mean()
        avg_distsac = ((window_sac['endxsac'].mean() - window_sac['startxsac'].mean())**2 + \
                        (window_sac['endysac'].mean() - window_sac['startysac'].mean())**2)**0.5
        load = int(name[4:5])
        panda_new = panda_new.append({'avg_durfix': avg_durfix, 'avg_xfix': avg_xfix,
                                    'avg_yfix': avg_yfix, 'avg_dursac': avg_dursac,
                                    'avg_distsac': avg_distsac, 'load': load},
                                    ignore_index=True)
        start_time = end_time
        #pdb.set_trace()

    with open(ENGINEEREDDATADIR + '/all_features.csv', 'a+') as f:
        panda_new.to_csv(f, sep='\t', index=False)
    '''
    panda_both = pandas.concat([panda_fix, panda_sac], axis=1, sort=False)
    panda_both['load'] = int(name[4:5])

    with open(ENGINEEREDDATADIR + '/%s_both%s.csv' % (name[:3], suffix), 'a+') as f:
        panda_both.to_csv(f, sep='\t', index=False)
    '''


def save_csv(fixations, saccades, name, suffix):
    # Add function description

    panda_fix = pandas.DataFrame(fixations)
    panda_fix.columns = ['Sfix', 'Efix', 'Durfix', 'endxfix', 'endyfix']
    panda_sac = pandas.DataFrame(saccades)
    panda_sac.columns = ['Ssac', 'Esac', 'Dursac', 'startxsac', 'startysac', 'endxsac', 'endysac']

    process_data(panda_fix, panda_sac, name)
    #pdb.set_trace()

'''
    if int(name[4:5]) == 1:
        panda_fix['load'] = 1
    else:
        panda_fix['load'] = 2
    with open(ENGINEEREDDATADIR + '/%s_fix%s.csv' % (name[:3], suffix), 'a+') as f:
        panda_fix.to_csv(f, sep='\t', index=False)
    if int(name[4:5]) == 1:
        panda_sac['load'] = 1
    else:
        panda_sac['load'] = 2
    with open(ENGINEEREDDATADIR + '/%s_sac%s.csv' % (name[:3], suffix), 'a+') as f:
        panda_sac.to_csv(f, sep='\t', index=False)
'''


if __name__ == "__main__":
    # Eyegaze data files
    PPS = [
        'p01_1_gaze',
        'p01_2_gaze',
        'p02_1_gaze',
        'p02_2_gaze',
        'p03_1_gaze',
        'p03_2_gaze',
        'p04_1_gaze',
        'p04_2_gaze',
        'p05_1_gaze',
        'p05_2_gaze',
        'p06_1_gaze',
        'p06_2_gaze',
        'p07_1_gaze',
        'p07_2_gaze',
        'p08_1_gaze',
        'p08_2_gaze',
        'p09_1_gaze',
        'p09_2_gaze',
        'p10_1_gaze',
        'p10_2_gaze',
        'p11_1_gaze',
        'p11_2_gaze',
        'p12_1_gaze',
        'p12_2_gaze',
        'p13_1_gaze',
        'p13_2_gaze',
        'p14_1_gaze',
        'p14_2_gaze',
        'p15_1_gaze',
        'p15_2_gaze',
        'p16_1_gaze',
        'p16_2_gaze',
        'p17_1_gaze',
        'p17_2_gaze',
        'p18_1_gaze',
        'p18_2_gaze']


    # Command-line arguments
    parser = argparse.ArgumentParser(description='Plotting options')
    parser.add_argument('-reduced', help='Plot 5000 samples only',
                        action='store_true')
    parser.add_argument('-csvonly', help='Only generate csv files',
                        action='store_true')
    args = parser.parse_args()


    # Directories and paths
    DIR = os.path.dirname(__file__)
    IMGDIR = os.path.join(DIR, 'imgs')
    DATADIR = os.path.join(DIR, 'data')
    PLOTDIR = os.path.join(DIR, 'plots')
    OUTPUTFILENAME = os.path.join(DIR, "output.txt")
    ENGINEEREDDATADIR = os.path.join(DIR, 'engineered_data')

    # Check if image directory exists
    if not os.path.isdir(IMGDIR):
        raise Exception(
            "ERROR: no image dir found; path '%s' does not exist!" % IMGDIR)
    # Check if data directory exists
    if not os.path.isdir(DATADIR):
        raise Exception(
            "ERROR: no data dir found; path '%s' does not exist!" % DATADIR)
    # Check if output directory exist; if not, create it
    if not os.path.isdir(PLOTDIR):
        os.mkdir(PLOTDIR)
    # Check if engineered data directory exist; if not, create it
    if not os.path.isdir(ENGINEEREDDATADIR):
        os.mkdir(ENGINEEREDDATADIR)

    # Experiment specs
    DISPSIZE = (6026, 1080)  # (px, px)
    SCREENSIZE = (39.9, 29.9)  # (cm, cm)
    SCREENDIST = 61.0  # cm
    PXPERCM = numpy.mean(
        [DISPSIZE[0]/SCREENSIZE[0], DISPSIZE[1]/SCREENSIZE[1]])  # px/cm

    set_directories(PPS)
    read_files(args.reduced, args.csvonly)
