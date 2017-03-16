#!usr/bin/env python
import analysis_console as ac
from bokeh.sampledata.autompg import autompg
from bokeh.sampledata.us_marriages_divorces import data

#Choose example
example = 3

if example == 1: #Basic scatter chart
    x = ac.Tools(df=autompg,
                metric=list(autompg.columns),
                xaxis='weight'
                )
    x.run()



if example == 2: #Scatter chart with different colors for categories
    x = ac.Tools(df=autompg,
                metric=list(autompg.columns),
                xaxis = 'weight', 
                cato = list(autompg.columns)
                )
    x.run()
    
if example ==3: #Example of divorces over time
    x = ac.Tools(df=data,
                metric=list(data.columns),
                xaxis='Year'
                )
    x.run()
