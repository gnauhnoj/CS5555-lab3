import loader
import plot
import numpy as np
import datetime
import math
import sys
from sklearn import cluster
from sklearn.preprocessing import StandardScaler, Imputer
__author__ = 'jhh283'

global FEELING_THRESH, WEIGHT_THRESH, ALMOST_EVERY, SLEEP_TOO_MUCH, SLEEP_TOO_LITTLE, INACTIVE_STEPS, OVERACTIVE_STEPS
ALMOST_EVERY = 0.8
FEELING_THRESH = 3
# percent change in weight
WEIGHT_THRESH = 0.05
# sleep is in minutes
SLEEP_TOO_MUCH = 8*60
SLEEP_TOO_LITTLE = 6*60
# step thresholds
INACTIVE_STEPS = 3000
OVERACTIVE_STEPS = 20000


# build our feature matrix
def build_vec(feats):
    for i, feat in enumerate(feats):
        feats[i] = np.column_stack(feat)

    feats_vert = [feat.shape[0] for feat in feats]
    max_ind = feats_vert.index(max(feats_vert))
    dates = feats[max_ind][:, 0]

    vec = []
    for i, c in enumerate(feats_vert):
        feat_vec = feats[i]
        if c < len(dates):
            subvec = []
            day_int = np.in1d(dates, feat_vec[:, 0])
            # print len(day_int), len(dates)
            k = 0
            for j, day in enumerate(dates):
                if day_int[j]:
                    temp = feat_vec[k, 1:]
                    subvec.append(temp)
                    k += 1
                else:
                    temp = [None, None] if i == 3 else [None]
                    subvec.append(temp)
            subvec = np.array(subvec)
        else:
            subvec = feat_vec[:, 1:]
        vec.append(subvec)
    vec = np.column_stack(vec)
    return vec


# fill gaps in data with mean
def fill_gaps(vec):
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(vec)
    vec = imp.transform(vec)
    return imp, vec


# normalize data vector by mean/std
def scale_data(vec):
    vec = [float(i) for i in vec]
    scaler = StandardScaler()
    scaler.fit(vec)
    vec = scaler.transform(vec)
    return scaler, vec


# check feelings < 3 every day
def verify_depressed_feelings(mtx_col):
    total_days = mtx_col.shape[0]
    dep_days = len(np.where(mtx_col < FEELING_THRESH)[0])
    return (dep_days / total_days) > ALMOST_EVERY


# check weight for fluctuations of >5%
def test_weight_change(mtx_col):
    mtx_col = mtx_col.tolist()
    min_weight = sys.maxint
    max_weight = -sys.maxint - 1
    state = False
    for weight in mtx_col:
        if weight is None:
            continue
        if weight < min_weight:
            min_weight = weight
        if weight > max_weight:
            max_weight = weight
        high = min_weight * (1 + WEIGHT_THRESH)
        low = max_weight * (1 - WEIGHT_THRESH)
        state = (weight > high) or (weight < low) or state
    return state


# function to remove Nones from a list and to test to see if elements
# greater than a provided high and lower than provided low
# make up a proportion greater than config variable
def test_range(mtx_col, low, high):
    mtx_col = mtx_col.tolist()
    mtx_col = [i for i in mtx_col if i is not None]
    total_days = len(mtx_col)
    low_cat = len([j for j in mtx_col if j < low])
    high_cat = len([j for j in mtx_col if j > high])
    test_bool = ((low_cat + high_cat) / total_days) > ALMOST_EVERY
    return mtx_col, test_bool


# function which tests to see if number of days that are significantly different
# from mean make up a proportion greater than config variable
def test_variation(mtx_col):
    scaler, scaled = scale_data(mtx_col)
    total_days = len(mtx_col)
    total_flux = check_flux(scaled)
    total_flux = len([flux for flux in total_flux if flux])
    return (total_flux / total_days) > ALMOST_EVERY


# check if you're sleeping too much or too little
# also check to see if your sleep is varying significantly every day
def test_sleep_amount(mtx_col):
    mtx_col, sleep_habits = test_range(mtx_col, SLEEP_TOO_LITTLE, SLEEP_TOO_MUCH)
    total_days = len(mtx_col)

    sleep_flux = test_variation(mtx_col)
    return sleep_habits or sleep_flux


# check activity levels
# check step count against defined thresholds
# check variability in steps and sedentary levels (hard to find reccomendations of sedentary time)
def test_activity_amount(step_col, sedentary_col):
    step_col, step_habits = test_range(step_col, INACTIVE_STEPS, OVERACTIVE_STEPS)
    total_days = len(step_col)

    # check variation in step count
    step_flux = test_variation(step_col)

    # check variation in sedentary minutes count
    # do this to make sure that we remove nones from the list
    sedentary_col, sedentary_habits = test_range(sedentary_col, 0, 0)
    sed_flux = test_variation(sedentary_col)

    return step_habits or sed_flux or step_flux


# this assumes matrix input is structured as -- [feelings, weight, sleep, activity]
def verify_depression_sev(mtx):
    imp, fill_vec = fill_gaps(mtx)
    feeling_cond = verify_depressed_feelings(fill_vec[:, 0])
    weight_cond = test_weight_change(mtx[:, 1])
    sleep_cond = test_sleep_amount(mtx[:, 2])
    act_cond = test_activity_amount(mtx[:, 3], mtx[:, 4])
    cond = feeling_cond and weight_cond and sleep_cond and act_cond
    return cond


# checks to see if a feature vector has every feature significantly outside of expected range
def check_flux(mtx_col):
    std = np.std(mtx_col)
    mean = np.mean(mtx_col)
    return (np.absolute(mtx_col - mean) > 2*std)

if __name__ == '__main__':
    reload(loader)
    dataset = loader.load_files()

    feelings = plot.plot_feelings(dataset)
    weight = plot.plot_weight(dataset)
    sleep = plot.plot_sleep(dataset)
    activity = plot.plot_activity(dataset)

    feats = [feelings, weight, sleep, activity]
    vec = build_vec(feats)
    print vec
    print 'Severe or Moderate Depression Identified?', verify_depression_sev(vec)
