"""
The main bokeh server app - read the data from csv, create the tabs, and
add them to a document.
"""


import os
import pandas as pd

from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.server.server import Server

from tornado.ioloop import IOLoop

from bokeh.io import curdoc
from bokeh.models.layouts import Tabs

from scripts.timeseries_tab import timeseries_tab
from scripts.histogram_tab import histo_tab


def prepare_data(year=None):
    if year:
        filename = f"steps{year}.csv"
    else:
        filename = "all_years.csv"
    input_filename = os.path.join(os.path.dirname(__file__), "..",
                                  "data",filename)
    df = pd.read_csv(input_filename)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    return df

def create_tabs(df, df_allyears):
    tab0 = timeseries_tab(df, "2024")
    tab1 = histo_tab(df)
    tab2 = timeseries_tab(df_allyears, "all years")

    tabs = Tabs(tabs = [tab0,tab1, tab2])
    return tabs

def create_dashboard(doc):
    df = prepare_data("2024")
    df_all_years = prepare_data()
    tabs = create_tabs(df, df_all_years)
    doc.add_root(tabs)


def run_server(origin, port):
    """
    Run the Bokeh app
    """
    server = Server({'/steps': create_dashboard},io_loop=IOLoop(),
                    allow_websocket_origin=[
                        "localhost",
                        "%s:%d" % ('localhost', int(port)),
                        "%s:%d" % (origin, int(port))
                    ],
                    port=int(port))

    server.start()
    server.io_loop.start()
    return server
