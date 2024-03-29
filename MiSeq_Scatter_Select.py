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

main_dir = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\MiSeq\OP750\MiSeqRUO'
ds = 'MiSeq FIT Data.xlsx'
xml = 'MiSeq_OP750_SPC.xml'

ds_dir = os.path.join(main_dir,ds)
xml_dir = os.path.join(main_dir,xml)

#Read and clean data
tree = ET.parse(xml_dir)
root = tree.getroot()
df = pd.read_excel(ds_dir)


#df.dropna(inplace=True)
run_filt = lambda x:x['Run Type'] != 'Evaluation Run'
df = df.loc[run_filt]

#Renames columns to remove spaces
conv = {'Serial Number':'SerialNumber',
        'Start Date':'StartDate',
        'Cluster Density' : 'ClusterDensity',
        'Normalized Reads PF' : 'NormalizedReadsPF',
        'Run Time' : 'RunTime',
        'Phasing R1' : 'PhasingR1',
        'Phasing R2' : 'PhasingR2',
        'Prephasing R1' : 'PrephasingR1',
        'Prephasing R2' : 'PrephasingR2',
        'Q30 R1' : 'Q30R1',
        'Q30 R2' : 'Q30R2'}

df.rename(columns=conv, inplace=True)

#Adds new column which contains start date as a string
time_conv = lambda x:str(x)[:-9]
df['StartDateStr'] = df['StartDate'].apply(time_conv)

#Colors that will be used for the different groups
#color_set = ['blue', 'orange', 'green', 'red', 'yellow', 'violet','cyan',
#            'orangered','blueviolet','goldenrod','palevioletred','yellowgreen']
color_set = Set1[9]


#List of the selection choices
cat_list = ["ReagentLot", "PhiXLot", "PR2_Lot", "Flowcell_Lot", "Pooled_PhiX_Lot",
            "2N_NaOH", "Hyb_Buffer", "EB_Buffer"]
metric_list = ["Q30", "NormalizedReadsPF", "ClusterDensity", "RunTime", "PhasingR1", 
            "PhasingR2", "PrephasingR1", "PrephasingR2", "Q30R1", "Q30R2", "Error_R1",
            "Error_R2", "CFRQC"]

#paramters to extract xml data
platform = 'MiSeqRUO'

def param_get(metric_name):
    for child in root.iter('platform'):
        if child.get('name') == platform:
            for child2 in child:
                if child2.get('name') == metric_name: #substitute for generic metric
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

    cycle_filt = lambda x:x['Cycles Completed'] >= int(metric_attrib['cycles'])
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
        tooltips = [('Serial Number', '@SerialNumber'),
                    (cat.value, '@' + cat.value),
                    (metric.value, '@' + metric.value),
                    ('Date', '@StartDateStr')])
    
    p = figure(plot_height = 625, plot_width = 950, x_axis_type='datetime', 
            tools = ['pan, wheel_zoom', 'reset', 'save' , hover], active_scroll = 'wheel_zoom',
            title = "{0} by {1}".format(metric.value, cat.value))
    

    #Creates the specification and control limits    
    time_range = [min(fig_df['StartDate']), max(fig_df['StartDate'])]
    
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
        p.circle('StartDate', metric.value, size = 10, 
                color=color_set[i % len(color_set)], source = main_source[i])
        i += 1
        
    return p
    

def update(attr, old, new):
    layout.children[1] = create_figure()


#Creates the widgets and updates values when they are changed
cat = Select(title="Category:", value="ReagentLot", options=cat_list)
cat.on_change('value', update)

metric = Select(title="Metric:", value="Q30", options=metric_list)
metric.on_change('value', update)

text = TextInput(title = 'N', value='300')
text.on_change('value', update)

cat_wig = widgetbox(cat)
metric_wig = widgetbox(metric)
text_wig = widgetbox(text)

layout = column(row(metric_wig, cat_wig, text_wig), create_figure())

curdoc().add_root(layout)
