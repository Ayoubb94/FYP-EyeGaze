import os

# external
import pandas

# custom
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, \
    draw_scanpath, draw_raw

def process_files(filename, gaze_data):

    for trialnr in range(len(gaze_data)):
        # Load saccades and fixations

        # [starttime, endtime, duration, startx, starty, endx, endy]
        saccades = gaze_data[trialnr]['events']['Esac']
        # [starttime, endtime, duration, endx, endy]
        fixations = gaze_data[trialnr]['events']['Efix']

        return trialnr, fixations, saccades


def generate_csv(ENGINEEREDDATADIR, filename, fixations, saccades):

    panda_fix = pandas.DataFrame(fixations)
    panda_fix.columns = ['Sfix', 'Efix', 'Durfix', 'endxfix', 'endyfix']
    panda_sac = pandas.DataFrame(saccades)
    panda_sac.columns = ['Ssac', 'Esac', 'Dursac', 'startxsac', 'startysac', 'endxsac', 'endysac']

    if int(filename[4:5]) == 1:
        panda_fix['load'] = 1
    else:
        panda_fix['load'] = 2
    with open(ENGINEEREDDATADIR + '/%s_fix.csv' % (filename[:3]), 'a+') as f:
        panda_fix.to_csv(f, sep='\t', index=False)
    if int(filename[4:5]) == 1:
        panda_sac['load'] = 1
    else:
        panda_sac['load'] = 2
    with open(ENGINEEREDDATADIR + '/%s_sac.csv' % (filename[:3]), 'a+') as f:
        panda_sac.to_csv(f, sep='\t', index=False)

    return panda_fix, panda_sac


def generate_plots(IMGDIR, PLOTDIR, filename, fixations, saccades, data, DISPSIZE, trialnr):

    # cognitive load
    if int(filename[4:5]) == 1:
        cognitive_load = "LOW"
    else:
        cognitive_load = "HIGH"

    #imgname = "screenshot.jpg"
    #imagefile = os.path.join(IMGDIR,imgname)

    # paths
    rawplotfile = os.path.join(
        PLOTDIR,
        "raw_data_%s_%s" % (filename[:3], cognitive_load))
    scatterfile = os.path.join(
        PLOTDIR,
        "fixations_%s_%s" % (filename[:3], cognitive_load))
    scanpathfile = os.path.join(
        PLOTDIR,
        "scanpath_%s_%s" % (filename[:3], cognitive_load))
    heatmapfile = os.path.join(
        PLOTDIR,
        "heatmap_%s_%s" % (filename[:3], cognitive_load))

    # raw data points
    draw_raw(
        data[trialnr]['x'], data[trialnr]['y'],
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