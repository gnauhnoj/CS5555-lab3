import loader
import numpy as np
import datetime
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
__author__ = 'jhh283'


def plt_plot_date(x, y, xlabel, ylabel, title, filename):
    fig = plt.figure()
    x = mdates.date2num(x)
    C = plt.plot(x, y)
    xstd = np.std(x)
    xlim = [min(x) - xstd, max(x) + xstd]
    ystd = np.std(y)
    ylim = [min(y) - ystd, max(y) + ystd]
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.savefig(filename, dpi=100)
    plt.show()
    plt.close()


def sort_time(x, y):
    npa = np.array(zip(x, y))
    npa = npa[npa[:, 0].argsort()]
    return npa[:, 0], npa[:, 1]


def plot_feelings(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].feelings is not None]
    y = [dataset[key].feelings for key in dataset if dataset[key].feelings is not None]
    x, y = sort_time(x, y)
    xlab = 'Date'
    ylab = 'Personal Feeling Score (1-5)'
    title = 'Feelings Plot'
    fn = 'feelings.png'
    plt_plot_date(x, y, xlab, ylab, title, fn)
    return [x, y]


def plot_weight(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].weight != {}]
    y = [dataset[key].weight['weight'] for key in dataset if dataset[key].weight != {}]
    x, y = sort_time(x, y)
    xlab = 'Date'
    ylab = 'Weight (kg)'
    title = 'Weight Plot'
    fn = 'weight.png'
    plt_plot_date(x, y, xlab, ylab, title, fn)
    return [x, y]


def plot_sleep(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].sleep['summary']['totalSleepRecords'] > 0]
    y = [dataset[key].sleep['summary']['totalMinutesAsleep'] for key in dataset if dataset[key].sleep['summary']['totalSleepRecords'] > 0]
    y2 = [dataset[key].sleep['summary']['totalTimeInBed'] for key in dataset if dataset[key].sleep['summary']['totalSleepRecords'] > 0]
    xlab = 'Date'
    ylab = 'Sleep (min)'
    title = 'Sleep Plot'
    fn = 'sleep.png'
    plt_plot_date(x, y, xlab, ylab, title, fn)
    return [x, y]


def plot_activity(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].activity['summary']['steps'] > 0]
    y = [dataset[key].activity['summary']['steps'] for key in dataset if dataset[key].activity['summary']['steps'] > 0]
    y2 = [dataset[key].activity['summary']['sedentaryMinutes'] for key in dataset if dataset[key].activity['summary']['steps'] > 0]
    xlab = 'Date'
    ylab = 'Activity (steps)'
    title = 'Activity Plot'
    fn = 'activity.png'
    plt_plot_date(x, y2, xlab, ylab, title, fn)
    return [x, y2]

if __name__ == '__main__':
    reload(loader)
    dataset = loader.load_files()
    feelings = plot_feelings(dataset)
    weight = plot_weight(dataset)
    # sleep = plot_sleep(dataset)
    # activity = plot_activity(dataset)
    # print dataset.keys()
