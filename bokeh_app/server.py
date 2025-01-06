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


def prepare_data():
    input_filename = os.path.join(os.path.dirname(__file__), "..",
                                  "data","steps2024.csv")
    df = pd.read_csv(input_filename)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    return df

def create_tabs(df):
    tab0 = timeseries_tab(df)
    tab1 = histo_tab(df)

    tabs = Tabs(tabs = [tab0,tab1])
    return tabs

def create_dashboard(doc):
    df = prepare_data()
    tabs = create_tabs(df)
    doc.add_root(tabs)


def minimal_dashboard(doc):
    print("Minimal dashboard is running...")
    p1 = figure(title="Tab 1")
    p1.line([1, 2, 3], [4, 6, 2])
    tab1 = Panel(child=p1, title="Tab 1")

    p2 = figure(title="Tab 2")
    p2.circle([1, 2, 3], [4, 6, 2])
    tab2 = Panel(child=p2, title="Tab 2")

    tabs = Tabs(tabs=[tab1, tab2])
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
