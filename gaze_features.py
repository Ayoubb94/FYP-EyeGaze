import os, pandas

def produce_features(FEATURESDIR, panda_fix, panda_sac, name, window_size, overlap):
    # This function should create a new data frame with data divided into 10s windows
    # With averaged fixation duration, mean of horizontal fixation postion,
    # mean of vertical fixation position, mean saccade speed or dur, and mean saccade distance
    # merge into panda_both, merge into panda_new

    panda_new = pandas.DataFrame()

    start_time = int(min(panda_fix.iloc[0,0], panda_sac.iloc[0,0]))
    while True:
        end_time = int(start_time + window_size)
        window_fix = panda_fix.loc[panda_fix['Sfix'].isin(range(start_time, end_time))]
        window_sac = panda_sac.loc[panda_sac['Ssac'].isin(range(start_time, end_time))]

        if window_fix.empty or window_sac.empty:
            break

        avg_durfix = window_fix['Durfix'].mean()
        avg_xfix = window_fix['endxfix'].mean()
        avg_yfix = window_fix['endyfix'].mean()
        std_xfix = window_fix['endxfix'].std()
        std_yfix = window_fix['endyfix'].std()
        avg_dursac = window_sac['Dursac'].mean()
        avg_distsac = ((window_sac['endxsac'].mean() - window_sac['startxsac'].mean())**2 + \
                        (window_sac['endysac'].mean() - window_sac['startysac'].mean())**2)**0.5
        fix_freq = window_fix.shape[0]
        sac_freq = window_sac.shape[0]
        load = int(name[4:5])
        panda_new = panda_new.append({'avg_durfix': avg_durfix, 'avg_xfix': avg_xfix,
                                    'avg_yfix': avg_yfix, 'std_xfix': std_xfix,
                                    'std_yfix': std_yfix, 'avg_dursac': avg_dursac,
                                    'avg_distsac': avg_distsac, 'load': load,
                                    'fix_freq': fix_freq, 'sac_freq': sac_freq},
                                    ignore_index=True)
        start_time = end_time - overlap*window_size/100

    with open(FEATURESDIR + '/%s_features_%s_%s.csv' % (name[:3], window_size, overlap), 'a+') as f:
        panda_new.to_csv(f, sep='\t', index=False)

