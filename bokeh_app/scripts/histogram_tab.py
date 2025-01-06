"""
Create a tab on a Bokeh dashboard that shows histograms of how many times
people did given number of steps in a week.
"""


import numpy as np
import pandas as pd
from bokeh.plotting import figure, show

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.layouts import TabPanel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider
from bokeh.layouts import column, row
from bokeh.palettes import Category20_16



def histo_tab(dataframe):
    """
    function called by main.py to show this tab.
    """


    def calc_totals_averages(name_list):
        """
        Simple calculations on columns of the dataframe
        """
        totals = {}
        means = {}
        for name in name_list:
            totals[name] = dataframe[name].sum()
            means[name] = int(dataframe[name].mean())
        return totals, means


    def make_dataset(name_list, x_min=20000,x_max=180000, n_bins=40):
        """
        return a column datasource
        """
        totals, means = calc_totals_averages(name_list)
        hist_df = pd.DataFrame(columns=["name",
                                        "left","right",
                                        "f_interval",
                                        "steps",
                                        "colour",
                                        "total",
                                        "average"])
        for i, name in enumerate(name_list):

            step_hist, edges = np.histogram(dataframe[name],
                                            bins=n_bins,range=[x_min,x_max])
            tmp_df = pd.DataFrame({"steps": step_hist, "left": edges[:-1],
                                   "right": edges[1:]})
            tmp_df['f_interval'] = ['%d to %d steps' % (left, right) \
                                    for left, right in zip(tmp_df['left'],
                                                           tmp_df['right'])]
            tmp_df["name"] = name
            tmp_df["colour"] = Category20_16[i]
            tmp_df["total"] = totals[name]
            tmp_df["average"] = means[name]

            # add this persons data to the overall hist_df
            hist_df = hist_df._append(tmp_df)

        # convert to a Bokeh ColumnDataSource and return it
        source = ColumnDataSource(hist_df)
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
        return the bokeh figure
        """
        print("In make_plot")
        p = figure(height=600, width=600,
                   x_axis_label='steps',y_axis_label="Count")
        p.quad(source=source,
               bottom=0, top='steps',
               left='left',
               right='right',
               fill_color='colour',
               alpha=0.5,
               line_color='black',
               legend_field='name')

        hover = HoverTool(tooltips = [("Name", "@name"),
                                      ("Total","@total"),
                                      ("Average","@average"),
                                      ('Step range', '@f_interval'),
                                      ('Num of Weeks', '@steps')
                                      ])
        p.add_tools(hover)
        p = style(p)
        return p


    def update(attr, old, new):
        """
        Update the plot every time a change is made
        """
        hists_to_plot = [selection.labels[i] for i in selection.active]
        new_src = make_dataset(hists_to_plot,
                               x_min = range_select.value[0],
                               x_max = range_select.value[1],
                               n_bins = nbin_select.value)
        cds.data.update(new_src.data)

    ### back to the histo_tab function definition...
    names = list(dataframe.columns)
    names.sort()
    # widgets to allow user to configure the plot
    selection = CheckboxGroup(labels=names, active=list(range(len(names))))
    selection.on_change('active', update)
    nbin_select = Slider(start=1,end=100,step=1,value=40,title="Num bins")
    nbin_select.on_change('value', update)

    range_select = RangeSlider(start=20000,end=200000,value=(30000,130000),
                               step=1000, title="Range")
    range_select.on_change('value',update)

    # initial column data source and plot
    initial_names = [selection.labels[i] for i in selection.active]
    cds = make_dataset(initial_names)
    p=make_plot(cds)

    controls = column(selection, nbin_select, range_select)
    # create row layout
    layout = row(controls, p)
    #turn this into a tab
    tab = TabPanel(child=layout, title="Histograms")
    return tab
