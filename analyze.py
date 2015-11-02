import loader
import plot
import numpy as np
import datetime
from sklearn import cluster
from sklearn.preprocessing import StandardScaler, Imputer
__author__ = 'jhh283'


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
            k = 0
            for j, day in enumerate(dates):
                if day_int[j]:
                    temp = feat_vec[k, 1:]
                    for meas in temp:
                        subvec.append(meas)
                    k += 1
                else:
                    subvec.append(None)
            subvec = np.array(subvec)
        else:
            subvec = feat_vec[:, 1:]
        vec.append(subvec)
    vec = np.column_stack(vec)
    return vec


def fill_gaps(vec):
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(vec)
    vec = imp.transform(vec)
    return imp, vec


def scale_data(vec):
    scaler = StandardScaler()
    scaler.fit(vec)
    vec = scaler.transform(vec)
    return scaler, vec

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

    imp, fill_vec = fill_gaps(vec)
    scaler, norm_vec = scale_data(fill_vec)
    print norm_vec
