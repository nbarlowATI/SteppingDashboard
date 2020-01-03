"""
The main bokeh server app - read the data from csv, create the tabs, and
add them to a document.
"""


import os
import pandas as pd

from bokeh.server.server import Server

from tornado.ioloop import IOLoop

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.timeseries_tab import timeseries_tab
from scripts.histogram_tab import histo_tab


def prepare_data():
    input_filename = os.path.join(os.path.dirname(__file__),
                                  "data","steps2019.csv")
    df = pd.read_csv(input_filename)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    return df

def create_tabs(df):
    tab0 = timeseries_tab(df)
    tab1 = histo_tab(df)

    tabs = Tabs(tabs = [tab0,tab1])
#    curdoc().add_root(tabs)
    return tabs

def create_dashboard(doc):
    df = prepare_data()
    tabs = create_tabs(df)
    doc.add_root(tabs)


def run_server(origin, port):
    """
    Run the Bokeh app
    """
    server = Server({'/bokeh_app': create_dashboard}, io_loop=IOLoop(),
                    allow_websocket_origin=[
                        "localhost",
                        "steppingup2019.azurewebsites.net",
                        "steppingup2019.azurewebsites.net:5006",
                        "steppingup2019.azurewebsites.net:80",
                        "%s:%d" % ('localhost', int(port)),
                        "%s:%d" % (origin, int(port))
                    ],
                    port=int(port))
    server.start()
    server.io_loop.start()
    return server
