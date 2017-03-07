#!usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import xml.etree.ElementTree as ET
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Select
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

def gen_chart(ds_loc, metric_list, cat_list = [], renamer = {}, col_list = [],
            xml_loc ='', platform = ''):
    """
    Creates an interactive scatter chart that can be grouped by categories
    
    Keyword arguments:
    ds_loc: string location of excel document where data is stored
    metric_list: list of string column titles of metrics that will be plotted. List entries must match column titles
    cat_list: list of string column titles of categories to separate data. List entries must match column titles
    col_list: list of colors to separate the categories by. Assigned default colors if none is given
    renamer: dict of column titles to rename. e.g. {'Serial Number' : 'SerialNumber', 'Start Date': 'StartDate'}
    xml_loc: string location of xml file 
    platform: string title of the platform in the xml file
    """    

    #Converts excel to dataframe and renames columns if required
    df = pd.read_excel(ds_loc)

    if renamer != {}:
        df.rename(columns = renamer, inplace = True)

    #Adds new column which contains start date as a string in order to use 
    #start date as tooltips
    time_conv = lambda x:str(x)[:10]
    df['StartDateStr'] = df['StartDate'].apply(time_conv)

    #Assign default colors for the different categories
    if col_list == []:
        col_list = ['blue', 'orange', 'green', 'red', 'yellow', 'violet','cyan',
                    'orangered','blueviolet','goldenrod','palevioletred',
                    'yellowgreen']

    def create_figure():
        #Different charts will be created depending on whether categories are 
        #given and whether there is an xml file provided
        if cat_list != []:
            p = cat_exist()
        if cat_list == []:
            p = cat_not_exist()
        if xml_loc != []:
            p = xml_user(p)
     
        return p

    def update(attr, old, new):
        layout.children[1] = create_figure()
   
    def cat_exist():
        #Counts how many unique types in the category in order to assign colors
        uniq_cat = list(set(df[cat.value].dropna()))   
        color_cnt = len(uniq_cat)
    
        #Groups by the category and assigns each group to a ColumnDataSource    
        indv_cat = df.groupby(cat.value)
        main_source = []

        for item in indv_cat:
            source = ColumnDataSource(ColumnDataSource.from_df(item[1]))
            main_source.append(source)

        #Creates the tooltip and assign plot parameters
        hover = HoverTool(
            tooltips = [('Serial Number', '@SerialNumber'),
                        (cat.value, '@' + cat.value),
                        (metric.value, '@' + metric.value),
                        ('Date', '@StartDateStr')])
        
        p = figure(plot_height = 625, plot_width = 950, x_axis_type='datetime', 
                tools = ['pan, wheel_zoom', 'reset', 'save' , hover], 
                active_scroll = 'wheel_zoom',
                title = "{0} by {1}".format(metric.value, cat.value))

        #Plot from each ColumnDataSource with a different color. Color rotates 
        #back to beginning if all colors are used

        i = 0
        while i < color_cnt:
            p.circle('StartDate', metric.value, size = 10, 
                    color=col_list[i % len(col_list)], source = main_source[i])
            i += 1
        return p

    def cat_not_exist():
        #Creates the tooltip and assign plot parameters
        source = ColumnDataSource.from_df(df)

        hover = HoverTool(
            tooltips = [('Serial Number', '@SerialNumber'),
                        (metric.value, '@' + metric.value),
                        ('Date', '@StartDateStr')])
    
        p = figure(plot_height = 625, plot_width = 950, x_axis_type='datetime', 
                tools = ['pan, wheel_zoom', 'reset', 'save' , hover], 
                active_scroll = 'wheel_zoom', title = "{0}".format(metric.value))

        #Plot from ColumnDataSource
        p.circle('StartDate', metric.value, color = 'blue', source = source)
        return p

    def xml_user(p):
        tree = ET.parse(xml_loc)
        root = tree.getroot()

        #Reverse lookup original column name if name part of the conversion dict.
        if renamer != {}:
            if metric.value in renamer.values():
                metric_name = [k for (k, v) in renamer.iteritems() if v == metric.value][0]
            else:
                metric_name = metric.value
        
        #Gets all the metric attributes from the xml file
        metric_attrib = param_get(metric_name, root)   

        #Creates the specification and control limit lines
        #usl/lsl is red while upl/lpl is orange
        time_range = [min(df['StartDate']), max(df['StartDate'])]
        
        if metric_attrib['usl'] != "NA":
            usl = metric_attrib['usl']
            p.line(time_range, 2*[usl], color = 'red', 
                    legend = 'Upper Specification: ' + usl)        
        if metric_attrib['lsl'] != "NA":
            lsl = metric_attrib['lsl']
            p.line(time_range, 2*[lsl], color = 'red', 
                    legend = 'Lower Specification: ' + lsl)
    
        upl = metric_attrib['upl']
        lpl = metric_attrib['lpl']

        p.line(time_range, 2*[upl], color = 'orange', 
                legend = 'Upper Process Limit: ' + upl)
        p.line(time_range, 2*[lpl], color = 'orange', 
                legend = 'Lower Process Limit: ' + lpl)
        
        return p

    def param_get(metric_name, root):
        #First looks for the platform name, then grabs all the children tags 
        #and texts into a dict
        for child in root.iter('platform'):
            if child.get('name') == platform:
                for child2 in child:
                    if child2.get('name') == metric_name: 
                        tags = []
                        texts = []
                        for child3 in child2:
                            tags.append(child3.tag)
                            texts.append(child3.text)
                        attrib_get = dict(zip(tags,texts))
                        return attrib_get


    #Initializes selections and updates selection values when changed
    metric = Select(title="Metric:", value=metric_list[0], options=metric_list)
    metric.on_change('value', update)
    
    if cat_list != []:
        cat = Select(title='Category:', value=cat_list[0], options=cat_list)
        cat.on_change('value', update)
        controls = widgetbox(metric, cat)
    else:
        controls = widgetbox(metric)
        
    layout = column(controls, create_figure())
    
    curdoc().add_root(layout)
