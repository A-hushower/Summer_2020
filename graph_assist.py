#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:19:15 2020

@author: This code was created by the members of the Rice University Computer Science Department to serve as helper functions for students in the 
COMP 182: Algorithmic Thinking class.
"""

import matplotlib.pyplot as plt
import pylab
import math

## Plotting functions

def test(num):
    print("graph_assist: Hello", num)

def show():
    """
    Do not use this function unless you have trouble with figures.

    It may be necessary to call this function after drawing/plotting
    all figures.  If so, it should only be called once at the end.

    Arguments:
    None

    Returns:
    None
    """
    plt.show()

def plot_dist_linear(data, title, xlabel, ylabel, filename=None):
    """
    Plot the distribution provided in data as a bar plot on a linear
    scale.

    Arguments: 
    data     -- dictionary which will be plotted with the keys
                on the x axis and the values on the y axis
    title    -- title label for the plot
    xlabel   -- x axis label for the plot
    ylabel   -- y axis label for the plot
    filename -- optional name of file to which plot will be
                saved (in png format)

    Returns:
    None
    """
    _plot_dist(data, title, xlabel, ylabel, False, filename)

def plot_dist_loglog(data, title, xlabel, ylabel, filename=None):
    """
    Plot the distribution provided in data as a scatter plot on a
    loglog scale.

    Arguments: 
    data     -- dictionary which will be plotted with the keys
                on the x axis and the values on the y axis
    title    -- title label for the plot
    xlabel   -- x axis label for the plot
    ylabel   -- y axis label for the plot
    filename -- optional name of file to which plot will be
                saved (in png format)

    Returns:
    None
    """
    _plot_dist(data, title, xlabel, ylabel, True, filename)


def _pow_10_round(n, up=True):
    """
    Round n to the nearest power of 10.

    Arguments:
    n  -- number to round
    up -- round up if True, down if False

    Returns:
    rounded number
    """
    if up:
        return 10 ** math.ceil(math.log(n, 10))
    else:
        return 10 ** math.floor(math.log(n, 10))
        

def _plot_dist(data, title, xlabel, ylabel, scatter, filename=None):
    """
    Plot the distribution provided in data.

    Arguments: 
    data     -- dictionary which will be plotted with the keys
                on the x axis and the values on the y axis
    title    -- title label for the plot
    xlabel   -- x axis label for the plot
    ylabel   -- y axis label for the plot
    scatter  -- True for loglog scatter plot, False for linear bar plot
    filename -- optional name of file to which plot will be
                saved (in png format)

    Returns:
    None
    """
    ### Check that the data is a dictionary
    if not isinstance(data, dict):
        msg = "data must be a dictionary, not {0}".format(type(data).__name__)
        raise TypeError(msg)

    ### Create a new figure
    fig = pylab.figure()

    ### Plot the data
    if scatter:
        _plot_dict_scatter(data)
    else:
        _plot_dict_bar(data, 0)
    
    ### Label the plot
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    ### Draw grid
    gca = pylab.gca()
    gca.yaxis.grid(True)
    gca.xaxis.grid(False)

    if scatter:
        ### Use loglog scale
        gca.set_xscale('log')
        gca.set_yscale('log')
        gca.set_xlim([_pow_10_round(min([x for x in data.keys() if x > 0]), False), 
                      _pow_10_round(max(data.keys()))])
        gca.set_ylim([_pow_10_round(min([x for x in data.values() if x > 0]), False), 
                      _pow_10_round(max(data.values()))])

    ### Show the plot
    fig.show()

    ### Save to file
    if filename:
        pylab.savefig(filename)

def plot_lines(data, title, xlabel, ylabel, labels=None, filename=None):
    """
    Plot a line graph with the provided data.

    Arguments: 
    data     -- a list of dictionaries, each of which will be plotted 
                as a line with the keys on the x axis and the values on
                the y axis.
    title    -- title label for the plot
    xlabel   -- x axis label for the plot
    ylabel   -- y axis label for the plot
    labels   -- optional list of strings that will be used for a legend
                this list must correspond to the data list
    filename -- optional name of file to which plot will be
                saved (in png format)

    Returns:
    None
    """
    ### Check that the data is a list
    if not isinstance(data, list):
        msg = "data must be a list, not {0}".format(type(data).__name__)
        raise TypeError(msg)

    ### Create a new figure
    fig = pylab.figure()

    ### Plot the data
    if labels:
        mylabels = labels[:]
        for i in range(len(data)-len(labels)):
            mylabels.append("")
        for d, l in zip(data, mylabels):
            _plot_dict_line(d, l)
        # Add legend
        pylab.legend(loc='best')
        gca = pylab.gca()
        legend = gca.get_legend()
        pylab.setp(legend.get_texts(), fontsize='medium')
    else:
        for d in data:
            _plot_dict_line(d)

    ### Set the lower y limit to 0 or the lowest number in the values
    mins = [min(l.values()) for l in data]
    ymin = min(0, min(mins))
    pylab.ylim(ymin=ymin)

    ### Label the plot
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    ### Draw grid lines
    pylab.grid(True)

    ### Show the plot
    fig.show()

    ### Save to file
    if filename:
        pylab.savefig(filename)

def _dict2lists(data):
    """
    Convert a dictionary into a list of keys and values, sorted by
    key.  

    Arguments:
    data -- dictionary

    Returns:
    A tuple of two lists: the first is the keys, the second is the values
    """
    xvals = list(data.keys())
    xvals.sort()
    yvals = []
    for x in xvals:
        yvals.append(data[x])
    return xvals, yvals

def _plot_dict_line(d, label=None):
    """
    Plot data in the dictionary d on the current plot as a line.

    Arguments:
    d     -- dictionary
    label -- optional legend label

    Returns:
    None
    """
    xvals, yvals = _dict2lists(d)
    if label:
        pylab.plot(xvals, yvals, label=label)
    else:
        pylab.plot(xvals, yvals)

def _plot_dict_bar(d, xmin=None, label=None):
    """
    Plot data in the dictionary d on the current plot as bars. 

    Arguments:
    d     -- dictionary
    xmin  -- optional minimum value for x axis
    label -- optional legend label

    Returns:
    None
    """
    xvals, yvals = _dict2lists(d)
    if xmin == None:
        xmin = min(xvals) - 1
    else:
        xmin = min(xmin, min(xvals) - 1)
    if label:
        pylab.bar(xvals, yvals, align='center', label=label)
        pylab.xlim([xmin, max(xvals)+1])
    else:
        pylab.bar(xvals, yvals, align='center')
        pylab.xlim([xmin, max(xvals)+1])

def _plot_dict_scatter(d):
    """
    Plot data in the dictionary d on the current plot as points. 

    Arguments:
    d     -- dictionary

    Returns:
    None
    """
    xvals, yvals = _dict2lists(d)
    pylab.scatter(xvals, yvals)
    
