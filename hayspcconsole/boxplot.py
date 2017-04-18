"""
Create a box plot with user input metric and category
"""
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Set1
from bokeh.models import HoverTool, ColumnDataSource

def create_boxplot(df_orig, met, **kwargs):
    
    cato = kwargs['cato']

    if 'col' in kwargs:
        col = kwargs['colors']
    else:
        col = Set1[9]

    df = df_orig
#    df['cato'] = df['cato'].round
    
    q1, q2, q3, upper, lower, outx, outy = quantiles(df, met, cato)
    p = boxplot(q1, q2, q3, upper, lower, outx, outy, col)
    
    return p

def quantiles(df, met, cato):  
    groups = df.groupby(cato)    
    q1 = groups[met].quantile(0.25)
    q2 = groups[met].quantile(0.50)
    q3 = groups[met].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr
    
    def outlier(group):
        cat = group.name

        return group[met][(group[met] < lower[cat])
                    | (group[met] > upper[cat])]

    outly = groups.apply(outlier)
    if not outly.empty:
        outx = []
        outy = []
        
        for catos in q1.index.tolist():
            for val in outly[catos]:
                outx.append(catos)
                outy.append(val)

    qmin = groups[met].quantile(0.00)
    qmax = groups[met].quantile(1.00)
    qmin_zip = zip(qmin, lower.values)
    qmax_zip = zip(qmax, upper.values)
    qmin_val = [max(x,y) for (x,y) in qmin_zip]
    qmax_val = [min(x,y) for (x,y) in qmax_zip]
    lower.replace(lower.values, qmin_val, inplace=True)
    upper.replace(upper.values, qmax_val, inplace=True)
    
    return q1, q2, q3, upper, lower, outx, outy
    
def boxplot(q1, q2, q3, upper, lower, outx, outy, color):
    
    q1_val = list(q1.values)
    q2_val = list(q2.values)
    q3_val = list(q3.values)
    upper_val = list(upper.values)
    lower_val = list(lower.values)
    
#    q1_val = q1.values
#    q2_val = q2.values
#    q3_val = q3.values
#    upper_val = upper.values
#    lower_val = lower.values
    
    cats = list(q1.index.tolist())
    cats = [str(x) for x in cats]
    
    
    col_list = []
    for i in range(len(q1_val)):
        col_list.append(color[i % len(color)])


    df = pd.DataFrame({'Category' : cats,
                       'Q1' : q1_val,
                       'Median' : q2_val,
                       'Q3' : q3_val,
                       'Upper' : upper_val,
                       'Lower' : lower_val,
                       'color' : col_list})

    source = ColumnDataSource(df)
    
    hover = HoverTool(
        tooltips = [('Category', '@Category'),
                    ('Median', '@Median')])

    p = figure(tools=['save', hover], 
               plot_height=400, 
               plot_width=950, 
               x_range=cats,
               y_range=[.99*min(lower), 1.01*max(upper)])
    
#    p.vbar(x=cats,
#            width=0.3,
#            top=q3_val,
#            bottom=q2_val, 
#            fill_color=col_list, 
#            line_color=None,
#            source=source)

    p.vbar(x='Category',
            width=0.3,
            top='Q3',
            bottom='Median', 
            fill_color='color', 
            line_color=None,
            source=source)

    p.vbar(x='Category',
            width=0.3,
            top='Median',
            bottom='Q1', 
            fill_color='color', 
            line_color=None,
            source=source)
   
    p.segment(cats, q3_val, cats, upper_val, line_color='black')
    p.segment(cats, q1_val, cats, lower_val, line_color='black')
    
    p.rect(cats, upper_val, 0.2, 0.01, line_color='black')
    p.rect(cats, lower_val, 0.2, 0.01, line_color='black')
    p.rect(cats, q2_val, 0.3, 0.01, line_color='black')
    
    p.circle(outx, outy)
    
    return p

