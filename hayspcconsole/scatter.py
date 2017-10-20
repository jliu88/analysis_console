"""
Create a scatter plot with user input metric and category
"""

import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.palettes import Set1

def create_scatter(df_orig, met, xaxis, **kwargs):
    """
    Creates and returns a scatter plot as a bokeh figure object with circle glyphs
    """    
    if 'cato' in kwargs:
        cato = kwargs['cato']
    else:
        cato = False
    if 'col' in kwargs:
        col = kwargs['colors']
    else:
        col = Set1[9]
    if 'metric_attrib' in kwargs:
        metric_attrib = kwargs['metric_attrib']
    else:
        metric_attrib = False

    df = df_orig
        
    p = scatter_template(df, met, xaxis, cato)
            
    #Finds the unique list of the category and counts them
    if cato:
        uniq_cat = df[cato].unique()
        cat_cnt = len(uniq_cat)
               
        #Groups by the category and assigns each group to a ColumnDataSource    
        indv_cat = df.groupby(cato)
        
        source = []
        for item in indv_cat:
            sub_source = ColumnDataSource(ColumnDataSource.from_df(item[1]))
            source.append(sub_source)

        i = 0
        while i < cat_cnt:
            p.circle(xaxis, 
                    met,
                    size=10, 
                    color=col[i % len(col)], 
                    source=source[i])
            i += 1

    else:
        source = ColumnDataSource(df)
        p.circle(xaxis, 
                met,
                size=10,
                source=source)
    
    if metric_attrib:
        p = create_limits(p, df, xaxis, metric_attrib)


    return p
    
def scatter_template(df, met, xaxy, cato):
    """
    Initialize the scatter chart with parameters
    """
    scatter_args = {'plot_height' : 625,
                    'plot_width' : 950,
                    'tools' : ['pan, wheel_zoom', 'reset', 'save'],
                    'active_scroll' : 'wheel_zoom'}
                   
    tooltips = [(met, '@' + met)]
                
    if 'SerialNumber' in df.columns:
        tooltips.insert(0, ('Serial Number', '@SerialNumber'))
                
    #Looks at the last entry in the xaxis column to see if it is a date
    #If it is a date then create a date column as a string to display in 
    #the tooltip
    if isinstance(df[xaxy].iloc[-1], pd.tslib.Timestamp):
        filt = lambda x:str(x)[:-9]
        df['Date_str'] = df[xaxy].apply(filt)
        scatter_args['x_axis_type'] = 'datetime'
        tooltips.append((xaxy, '@Date_str'))
    else:
        tooltips.append((xaxy, '@' + xaxy))

    #Title and tooltips depending on if there are categories
    if cato:
        tooltips.insert(2, (cato, '@' + cato))
        scatter_args['title'] = "{0} by {1}".format(met, cato) 
    else:
        scatter_args['title'] = "{0}".format(met)

    hover = HoverTool(tooltips = tooltips)
    scatter_args['tools'].append(hover)
    
    p = figure(**scatter_args)
    p.xaxis.axis_label = xaxy
    p.yaxis.axis_label = met            
           
    return p
    
def create_limits(p, df, xaxis, metric_attrib):
    """
    Creates spec and control limits
    """
    #Creates the specification and control limits    
    time_range = [min(df[xaxis]), max(df[xaxis])]
    
    if metric_attrib['usl'] != "NA":
        usl = metric_attrib['usl']
        p.line(time_range, 
            2*[usl], 
            color='red',
            legend='Upper Specification: ' + usl)        
    if metric_attrib['lsl'] != "NA":
        lsl = metric_attrib['lsl']
        p.line(time_range,
            2*[lsl],
            color='red', 
            legend='Lower Specification: ' + lsl)
    if metric_attrib['upl'] != 'NA':
        upl = metric_attrib['upl']
        p.line(time_range, 
            2*[upl],
            color='orange',
            legend='Upper Process Limit: ' + upl)
    if metric_attrib['lpl'] != 'NA':
        lpl = metric_attrib['lpl']
        p.line(time_range,
            2*[lpl], 
            color='orange', 
            legend='Lower Process Limit: ' + lpl)    

    return p
#



    
    

        