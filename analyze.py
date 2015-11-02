import loader
import plot
import numpy as np
import datetime
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
__author__ = 'jhh283'


if __name__ == '__main__':
    reload(loader)
    dataset = loader.load_files()
    feelings = plot.plot_feelings(dataset)
    weight = plot.plot_weight(dataset)
    sleep = plot.plot_sleep(dataset)
    activity = plot.plot_activity(dataset)

