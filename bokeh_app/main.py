"""
Bokeh dashboard for displaying plots of weekly step counts for different people.
One tab shows line plots on a time axis, while another tab shows histograms of
how often each person achieved a given weekly step-count.

Assumes input data in a csv file with columns Date,Person1,Person2,...
and the cell values being the weekly step counts for those person/dates.
"""

import os
import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.timeseries_tab import timeseries_tab
from scripts.histogram_tab import histo_tab

input_filename = os.path.join(os.path.dirname(__file__),"data","steps2019.csv")
df = pd.read_csv(input_filename)
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index("Date")

tab0 = timeseries_tab(df)
tab1 = histo_tab(df)

tabs = Tabs(tabs = [tab0,tab1])

curdoc().add_root(tabs)
