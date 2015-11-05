import numpy as np
import datetime
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
__author__ = 'jhh283'

# set of functions to parse our Stats data structure and to plot time series for each
# data stream we are interested in


# general plotting utility function
def plt_plot_date(x, y, xlabel, ylabel, title, filename):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    hfmt = mdates.DateFormatter('%m/%d')
    C = plt.plot_date(x, y, ls='solid')
    # xstd = np.std(x)
    xstd = datetime.timedelta(days=1)
    xlim = [min(x) - xstd, max(x) + xstd]
    ystd = np.std(y)
    ylim = [min(y) - ystd, max(y) + ystd]
    plt.xlim(xlim)
    plt.ylim(ylim)
    # plt.xticks(rotation='vertical')
    ax.xaxis.set_major_formatter(hfmt)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.savefig(filename, dpi=100)
    plt.show()
    plt.close()


# sorts np arrays according to the provided time stamp
def sort_time(x, y, y_next=None):
    npa = np.array(zip(x, y))
    if y_next is not None:
        npa = np.column_stack([npa, y_next])
    npa = npa[npa[:, 0].argsort()]
    if y_next is not None:
        return npa[:, 0], npa[:, 1], npa[:, 2]
    return npa[:, 0], npa[:, 1]


# plots user-provided feeling survey response
def plot_feelings(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].feelings is not None]
    y = [dataset[key].feelings for key in dataset if dataset[key].feelings is not None]
    x, y = sort_time(x, y)
    xlab = 'Date'
    ylab = 'Personal Feeling Score (1-5)'
    title = 'Subjective Feeling Score'
    fn = 'feelings.png'
    plt_plot_date(x, y, xlab, ylab, title, fn)
    return [x, y]


# plots weight as retrieved from the fitbit api
def plot_weight(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].weight != {}]
    y = [dataset[key].weight['weight'] for key in dataset if dataset[key].weight != {}]
    x, y = sort_time(x, y)
    xlab = 'Date'
    ylab = 'Weight (kg)'
    title = 'Weight'
    fn = 'weight.png'
    plt_plot_date(x, y, xlab, ylab, title, fn)
    return [x, y]


# plots sleep as retrieved from the fitbit api
def plot_sleep(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].sleep['summary']['totalSleepRecords'] > 0]
    y = [dataset[key].sleep['summary']['totalMinutesAsleep'] for key in dataset if dataset[key].sleep['summary']['totalSleepRecords'] > 0]
    # y2 = [dataset[key].sleep['summary']['totalTimeInBed'] for key in dataset if dataset[key].sleep['summary']['totalSleepRecords'] > 0]
    x, y = sort_time(x, y)
    xlab = 'Date'
    ylab = 'Total Minutes Asleep (min)'
    title = 'Total Time Asleep'
    fn = 'sleep.png'
    plt_plot_date(x, y, xlab, ylab, title, fn)
    return [x, y]


# plots step count and sedentary time as retrieved from the fitbit api
def plot_activity(dataset):
    x = [dataset[key].date for key in dataset if dataset[key].activity['summary']['steps'] > 0]
    y_steps = [dataset[key].activity['summary']['steps'] for key in dataset if dataset[key].activity['summary']['steps'] > 0]
    y_sed_act = [dataset[key].activity['summary']['sedentaryMinutes'] for key in dataset if dataset[key].activity['summary']['steps'] > 0]
    x, y_steps, y_sed_act = sort_time(x, y_steps, y_sed_act)
    xlab = 'Date'
    ylab = 'Step Count (steps)'
    title = 'Steps Taken'
    fn = 'steps.png'
    plt_plot_date(x, y_steps, xlab, ylab, title, fn)
    xlab = 'Date'
    ylab = 'Sedentary Time (minutes)'
    title = 'Sedentary Time'
    fn = 'activity.png'
    plt_plot_date(x, y_sed_act, xlab, ylab, title, fn)
    return [x, y_steps, y_sed_act]
