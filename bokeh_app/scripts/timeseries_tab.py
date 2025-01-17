"""
Return a Bokeh panel showing line charts of steps vs time
"""

import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.layouts import TabPanel, Tabs
from bokeh.models.widgets import (CheckboxGroup, Slider, DateRangeSlider,
				  CheckboxButtonGroup, TableColumn,
				  DataTable, Select)
from bokeh.layouts import column, row
from bokeh.palettes import Category20_16


def timeseries_tab(dataframe, title):
    """
    return a tab showing steps vs time for each person
    """

    def make_dataset(name_list,
                     range_start,
                     range_end):
        """
        Filter the full dataset by name and by date range,
        and return it as a Bokeh ColumnDataSource
        """

        ## why do I have to do this? What is the point of a DateRangeSlider???
        if isinstance(range_start, (int, float)):
            range_start = datetime.fromtimestamp(range_start/1000)
        elif isinstance(range_start, str):
            range_start = datetime.fromisoformat(range_start)

        if isinstance(range_end, (int, float)):
            range_end = datetime.fromtimestamp(range_end/1000)
        elif isinstance(range_end, str):
            range_end = datetime.fromisoformat(range_end)

        filtered_df = dataframe.loc[range_start: range_end]

        source = ColumnDataSource(filtered_df)
        return source

    def style(p):
        # Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p


    def make_plot(source):
        """
        create a Bokeh figure with the selected data
        """
        names_to_plot = source.column_names[1:]

        time_series = figure(x_axis_type="datetime",
                             width=700, height=550)
        hover = HoverTool(tooltips = [("Name","$name"),
                                      ("Date","@Date{%F}"),
                                      ("Steps","$y")],
                          formatters={'Date': 'datetime'})
        time_series = style(time_series)
        time_series.add_tools(hover)
        time_series.legend.location = "top_left"
        for i, name in enumerate(names_to_plot):
            time_series.line("Date",name,source=source,
                             line_color=Category20_16[i],
                             line_width=2,
                             name=name,
                             legend_label=name)
        return time_series


    def update(attr, old, new):
        """
        Update data source when something is changed.
        """
        name_list = [name_selection.labels[i] for i in name_selection.active]
        new_src = make_dataset(name_list,
                               date_slider.value[0],
                               date_slider.value[1])
        cds.data.update(new_src.data)


    def update_lines(attr, old, new):
        """
        Hide selected lines
        """
        names_to_plot = [name_selection.labels[i] for i in name_selection.active]
        for name in names:
            if name in names_to_plot:
                p.select_one({"name": name}).visible = True
            else:
                p.select_one({"name": name}).visible = False

    ### back to the timeseries_tab function

    earliest_date = dataframe.index[0] - timedelta(days=1)
    latest_date = dataframe.index[len(dataframe)-1] + timedelta(days=1)

    names = list(dataframe.columns)
    names.sort()

    # widgets to allow user to configure the plot
    name_selection = CheckboxGroup(labels=names,
                                   active=list(range(len(names))))

    name_selection.on_change('active',update_lines)

    date_slider = DateRangeSlider(title="Date range", start=earliest_date,
                                  end=latest_date,
                                  value=(earliest_date,latest_date),
                                  step=1)
    date_slider.on_change('value',update)

    initial_names = [name_selection.labels[i] for i in name_selection.active]
    cds = make_dataset(initial_names,
                       date_slider.value[0],
                       date_slider.value[1])
    p = make_plot(cds)

    controls = column(name_selection, date_slider)
    layout = row(controls, p)

    tab = TabPanel(child=layout, title=title)
    return tab
