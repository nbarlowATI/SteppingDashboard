#!/usr/bin/env python

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
import argparse

from server import run_server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="bokeh dashboard for steps")
    parser.add_argument("--host",help="hostname",default="0.0.0.0")
    parser.add_argument("--port",help="port",default=5006)
    args = parser.parse_args()

    run_server(args.host, args.port)
