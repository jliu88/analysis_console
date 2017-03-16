import xml.etree.ElementTree as ET
import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models.widgets import Select, TextInput
from bokeh.models import HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.palettes import Set1

class tools(object):
    
    def __init__(self, df, metric, xaxis, **kwargs):
        """
        Keyword arguments:
        ds_loc (df or str): df of table or location of excel document where data is stored
        metric (list): df column titles of metrics that will be plotted.
        xaxis (str): df column title of x axis
        cato (list, optional): df column titles of categories to separate data
        col (list, optional): colors to separate the categories by. Default is Set1[9]
        renamer (dict, optional): column titles to rename. e.g. {'Serial Number' : 'SerialNumber', 'Start Date': 'StartDate'}
        xml_loc (str, optional): location of xml file 
        platform (str, optional): title of the platform in the xml file
        """
        
        if isinstance(df, str):
            self.df = pd.read_excel(df)
        if isinstance(df, pd.DataFrame):
            self.df = df
        
        self.df.dropna(inplace=True)

        if 'cato' in kwargs:
            self.cato = kwargs['cato']

        if 'renamer' in kwargs:
            self.renamer = kwargs['renamer']
            self.df.rename(columns = self.renamer, inplace =True)
                                
        if 'xml_loc' in kwargs:
            tree = ET.parse(kwargs['xml_loc'])
            self.root = tree.getroot()
            self.platform = kwargs['platform']

        if 'col' in kwargs:
            self.colors = kwargs['col']
        else:
            self.colors = Set1[9] 

        self.metric = metric
        self.xaxis = xaxis


    def create_scatter(self):
        """
        Creates scatter
        """
        self.scatter_df = self.df[-int(self.lastn.value):]

        if hasattr(self, 'root'):
            #Reverse lookup original column name if name if part of the conversion dict.
            #This will not be needed in the general Bokeh_Select
            if self.metric_select.value in self.renamer.values():
                metric_name = [k for (k, v) in self.renamer.iteritems() if v == self.metric_select.value][0]

            else:
                metric_name = self.metric_select.value

            self.param_get(metric_name)

            cycle_filt = lambda x:x['Cycles Completed'] >= int(self.metric_attrib['cycles'])
            self.scatter_df = self.scatter_df.loc[cycle_filt]            

        p = self.scatter_template()
                
        #Finds the unique list of the category and counts them
        if hasattr(self, 'cato'):
            uniq_cat = self.scatter_df[self.cato_select.value].unique()
            cat_cnt = len(uniq_cat)
                   
            #Groups by the category and assigns each group to a ColumnDataSource    
            indv_cat = self.scatter_df.groupby(self.cato_select.value)
            
            source = []
            for item in indv_cat:
                sub_source = ColumnDataSource(ColumnDataSource.from_df(item[1]))
                source.append(sub_source)

            i = 0
            while i < cat_cnt:
                p.circle(self.xaxis, 
                        self.metric_select.value,
                        size=10, 
                        color=self.colors[i % len(self.colors)], 
                        source=source[i])
                i += 1

        else:
            source = ColumnDataSource(self.scatter_df)
            p.circle(self.xaxis, 
                    self.metric_select.value,
                    size=10,
                    source=source)
        
        if hasattr(self, 'root'):
            p = self.create_limits(p)

        return p
        
    def scatter_template(self):
        """
        Initialize the scatter chart with parameters
        """
        scatter_args = {'plot_height' : 625,
                        'plot_width' : 950,
                        'tools' : ['pan, wheel_zoom', 'reset', 'save'],
                        'active_scroll' : 'wheel_zoom'}
                       
        tooltips = [(self.metric_select.value, '@' + self.metric_select.value)]
                    
        if 'SerialNumber' in self.scatter_df.columns:
            tooltips.insert(0, ('Serial Number', '@SerialNumber'))
                    
        #Looks at the last entry in the xaxis column to see if it is a date
        #If it is a date then create a date column as a string to display in 
        #the tooltip
        if isinstance(self.df[self.xaxis].iloc[-1], pd.tslib.Timestamp):
            filt = lambda x:str(x)[:-9]
            self.scatter_df['Date_str'] = self.scatter_df[self.xaxis].apply(filt)
            scatter_args['x_axis_type'] = 'datetime'
            tooltips.append((self.xaxis, '@Date_str'))
        else:
            tooltips.append((self.xaxis, '@' + self.xaxis))

        #Title and tooltips depending on if there are categories
        if hasattr(self, 'cato'):
            tooltips.insert(2, (self.cato_select.value, '@' + self.cato_select.value))
            scatter_args['title'] = "{0} by {1}".format(self.metric_select.value, self.cato_select.value) 
        else:
            scatter_args['title'] = "{0}".format(self.metric_select.value)

        hover = HoverTool(tooltips = tooltips)
        scatter_args['tools'].append(hover)
                               
        return figure(**scatter_args)
        
    def create_limits(self, p):
        """
        Creates spec and control limits
        """
        #Creates the specification and control limits    
        time_range = [min(self.scatter_df[self.xaxis]), max(self.scatter_df[self.xaxis])]
        
        if self.metric_attrib['usl'] != "NA":
            usl = self.metric_attrib['usl']
            p.line(time_range, 
                2*[usl], 
                color='red',
                legend='Upper Specification: ' + usl)        
                
        if self.metric_attrib['lsl'] != "NA":
            lsl = self.metric_attrib['lsl']
            p.line(time_range,
                2*[lsl],
                color='red', 
                legend='Lower Specification: ' + lsl)
    
        if self.metric_attrib['upl'] != 'NA':
            upl = self.metric_attrib['upl']
            p.line(time_range, 
                2*[upl],
                color='orange',
                legend='Upper Process Limit: ' + upl)
                
        if self.metric_attrib['lpl'] != 'NA':
            lpl = self.metric_attrib['lpl']
            p.line(time_range,
                2*[lpl], 
                color='orange', 
                legend='Lower Process Limit: ' + lpl)    
    
        return p

    def create_boxplot(self):
        """
        Creates boxplot
        """
        
    def create_table(self):
        """
        Creates data table
        """

    def create_widget(self):
        """
        Creates widgets
        """

        if hasattr(self, 'cato'):
            self.cato_select = Select(title='Category:', 
                                    value=self.cato[0], 
                                    options=self.cato)
            self.cato_box = widgetbox(self.cato_select)
        
        self.metric_select = Select(title="Metric:", 
                                    value=self.metric[0], 
                                    options=self.metric)
        self.metric_box = widgetbox(self.metric_select)

        self.lastn = TextInput(title='N',
                            value='300')
        self.lastn_box = widgetbox(self.lastn)
            
        
    def param_get(self, metric_name):
        """
        Gets parameters from xml
        """
        for child in self.root.iter('platform'):
            if child.get('name') == self.platform:
                for child2 in child:
                    if child2.get('name') == metric_name: 
                        tags = []
                        texts = []
                        for child3 in child2:
                            tags.append(child3.tag)
                            texts.append(child3.text)
                        self.metric_attrib = dict(zip(tags,texts))
       
    def update(self, attr, old, new):
        """
        Updates the output
        """
        self.layout.children[1] = self.create_scatter()

        
    def run(self):
        """
        Run for server to work
        """
        self.create_widget()        

        #Create layout of the page 
        if hasattr(self, 'cato'):
            self.layout = column(row(self.metric_box, self.cato_box, self.lastn_box), 
                    self.create_scatter())
        else:
            self.layout = column(row(self.metric_box, self.lastn_box), self.create_scatter())
        
        self.metric_select.on_change('value', self.update)
        self.lastn.on_change('value', self.update)
    
        if hasattr(self, 'cato'):
            self.cato_select.on_change('value', self.update)
        
        curdoc().add_root(self.layout)
        
        

        