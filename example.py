#!usr/bin/env python
from hayspcconsole.analysis_console import Console
from bokeh.sampledata.autompg import autompg
from bokeh.sampledata.us_marriages_divorces import data

#Choose example
example = 2

if example == 1: #Basic scatter chart
    x = Console(df=autompg,
                metric=list(autompg.columns),
                xaxis='weight'
                )
    x.run()



if example == 2: #Scatter chart with different colors for categories
    x = Console(df=autompg,
                metric=list(autompg.columns),
                xaxis = 'weight', 
                cato = list(autompg.columns)
                )
    x.run()
    
if example ==3: #Example of divorces over time
    x = Console(df=data,
                metric=list(data.columns),
                xaxis='Year'
                )
    x.run()
