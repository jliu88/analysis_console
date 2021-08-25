#!usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import xml.etree.ElementTree as ET
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Select, TextInput
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.palettes import Set1

main_dir = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\NovaSeq\FIT'
ds = 'NovaSeq_FIT_Data.xlsx'
xml = 'NovaSeq_FIT_SPC.xml'

ds_dir = os.path.join(main_dir,ds)
xml_dir = os.path.join(main_dir,xml)

#Read and clean data
tree = ET.parse(xml_dir)
root = tree.getroot()
df = pd.read_excel(ds_dir)


#df.dropna(inplace=True)
#run_filt = lambda x:x['Run Type'] != 'Evaluation Run'
#df = df.loc[run_filt]

#Renames columns to remove spaces
conv = {'%_PF' : 'P_PF',
        '%_Occupied' : 'P_Occupied'}

df.rename(columns=conv, inplace=True)

#Adds new column which contains start date as a string
time_conv = lambda x:str(x)[:-9]
df['StartDateStr'] = df['Run_Date'].apply(time_conv)

#Colors that will be used for the different groups
#color_set = ['blue', 'orange', 'green', 'red', 'yellow', 'violet','cyan',
#            'orangered','blueviolet','goldenrod','palevioletred','yellowgreen']
color_set = Set1[9]


#List of the selection choices
cat_list = ["SBS_Lot", "Buffer_Lot", "Cluster_Lot", "Flowcell_Lot"]
metric_list = ['Q30_Read1', 'Q30_Read2', 'Run_Time', 'Yield_Total',
               'Prephasing_R1', 'Prephasing_R2', 'Phasing_R1', 'Phasing_R2', 
               'Resynthesis', 'Cycle1_Intensity', 'P_PF', 'P_Occupied',
               'Occupied_PF', 'CFRQC', 'FWHM_Green', 'FWHM_Red', 'SD_FWHM_Green', 
               'Error_Rate']

#paramters to extract xml data
platform = 'Data'

def param_get(metric_name):
    for child in root.iter('platform'):
        if child.get('name') == platform:
            for child2 in child:
                if child2.get('name') == metric_name: #substitute for generic metric name
                    tags = []
                    texts = []
                    for child3 in child2:
                        tags.append(child3.tag)
                        texts.append(child3.text)
                    attrib_get = dict(zip(tags,texts))
                    return attrib_get
                             
        
def create_figure():
    fig_df = df
    
    fig_df = fig_df[-int(text.value):]
    
    #Reverse lookup original column name if name if part of the conversion dict.
    #This will not be needed in the general Bokeh_Select
    if metric.value in conv.values():
        metric_name = [k for (k, v) in conv.iteritems() if v == metric.value][0]
    
    else:
        metric_name = metric.value

    #Gets all the metric attributes from the xml file
    
    metric_attrib = param_get(metric_name)


    cycle_filt = lambda x:x['Total_Cycles'] >= int(metric_attrib['cycles'])
    fig_df = fig_df.loc[cycle_filt]

    #Finds the unique list of the category and counts them
    uniq_cat = list(set(fig_df[cat.value].dropna()))   
    color_cnt = len(uniq_cat)

    #Groups by the category and assigns each group to a ColumnDataSource    
    indv_cat = fig_df.groupby(cat.value)
    main_source = []
    for item in indv_cat:
        source = ColumnDataSource(ColumnDataSource.from_df(item[1]))
        main_source.append(source)
    
    #Creates the tooltip and assign plot parameters
    hover = HoverTool(
        tooltips = [('Serial_Number', '@Serial_Number'),
                    (cat.value, '@' + cat.value),
                    (metric.value, '@' + metric.value),
                    ('Date', '@StartDateStr')])
    
    p = figure(plot_height = 625, plot_width = 950, x_axis_type='datetime', 
            tools = ['pan, wheel_zoom', 'reset', 'save' , hover], active_scroll = 'wheel_zoom',
            title = "{0} by {1}".format(metric.value, cat.value))
    

    #Creates the specification and control limits    
    time_range = [min(fig_df['Run_Date']), max(fig_df['Run_Date'])]
    
    if metric_attrib['usl'] != "NA":
        usl = metric_attrib['usl']
        p.line(time_range, 2*[usl], color = 'red', legend = 'Upper Specification: ' + usl)        
    if metric_attrib['lsl'] != "NA":
        lsl = metric_attrib['lsl']
        p.line(time_range, 2*[lsl], color = 'red', legend = 'Lower Specification: ' + lsl)

    upl = metric_attrib['upl']
    lpl = metric_attrib['lpl']
    p.line(time_range, 2*[upl], color = 'orange', legend = 'Upper Process Limit: ' + upl)
    p.line(time_range, 2*[lpl], color = 'orange', legend = 'Lower Process Limit: ' + lpl)

    #Plot from each ColumnDataSource with a different color
    i = 0
    while i < color_cnt:
        p.circle('Run_Date', metric.value, size = 10, 
                color=color_set[i % len(color_set)], source = main_source[i])
        i += 1
        
    return p
    

def update(attr, old, new):
    layout.children[1] = create_figure()


#Creates the widgets and updates values when they are changed
cat = Select(title="Category:", value="SBS_Lot", options=cat_list)
cat.on_change('value', update)

metric = Select(title="Metric:", value="Q30_Read1", options=metric_list)
metric.on_change('value', update)

text = TextInput(title = 'N', value='300')
text.on_change('value', update)

cat_wig = widgetbox(cat)
metric_wig = widgetbox(metric)
text_wig = widgetbox(text)

layout = column(row(metric_wig, cat_wig, text_wig), create_figure())

curdoc().add_root(layout)
