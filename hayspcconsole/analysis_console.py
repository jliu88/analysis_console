import xml.etree.ElementTree as ET

import pandas as pd
from bokeh.models.widgets import Select, TextInput
from bokeh.palettes import Set1
from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row, column

from . import scatter
from . import boxplot
from . import table

class Console(object):
    """
    Args:     
        ds_loc (df or str): df of table or location of excel document where data is stored
        metric (list): df column titles of metrics that will be plotted.
        xaxis (str): df column title of x axis
        cato (list, optional): df column titles of categories to separate data
        col (list, optional): colors to separate the categories by. Default is Set1[9]
        renamer (dict, optional): column titles to rename. e.g. {'Serial Number' : 'SerialNumber', 'Start Date': 'StartDate'}
        xml_loc (str, optional): location of xml file 
        platform (str, optional): title of the platform in the xml file
    
    Returns:
        Console object
    """

    def __init__(self, df, metric, xaxis, **kwargs):   
        
        self.s_kwargs = {}
        
        if isinstance(df, str):
            self.df = pd.read_excel(df)
        if isinstance(df, pd.DataFrame):
            self.df = df        
        #self.df.dropna(subset=metric, inplace=True)
        if 'cato' in kwargs:
            self.cato = kwargs['cato']
            #self.df.dropna(subset=self.cato)
        if 'renamer' in kwargs:
            self.renamer = kwargs['renamer']
            self.df.rename(columns = self.renamer, inplace =True)
            self.s_kwargs['renamer'] = self.renamer
        if 'xml_loc' in kwargs:
            tree = ET.parse(kwargs['xml_loc'])
            self.root = tree.getroot()
            self.platform = kwargs['platform']
            self.s_kwargs['root'] = self.root
            self.s_kwargs['platform'] = self.platform
        if 'col' in kwargs:
            self.colors = kwargs['col']
            self.s_kwargs['colors'] = self.colors
        else:
            self.colors = Set1[9] 
        
        self.metric = metric
        self.xaxis = xaxis
        self.lastn = 300
        
        print('initialized')
        
    def param_get(self, metric_name, root, platform):
        """
        Gets parameters from xml
        """
        for child in root.iter('platform'):
            if child.get('name') == platform:
                for child2 in child:
                    if child2.get('name') == metric_name: 
                        tags = []
                        texts = []
                        for child3 in child2:
                            tags.append(child3.tag)
                            texts.append(child3.text)
                        metric_attrib = dict(zip(tags,texts))
                        return metric_attrib
        

    def create_widgets(self):
        self.metsel = Select(title="Metric:", 
                                    value=self.metric[0], 
                                    options=self.metric)
        self.mets_box = widgetbox(self.metsel)
        self.lastsel = TextInput(title='N',
                            value='300')
        self.lasts_box = widgetbox(self.lastsel)
        
        #If categories, create category select 
        if hasattr(self, 'cato'):
            self.catosel = Select(title='Category:', 
                                    value=self.cato[0], 
                                    options=self.cato)
            self.catos_box = widgetbox(self.catosel)

    def update_attrib(self):
        #Reverse lookup original column name if name if part of the conversion dict.
        #This will not be needed in the general Bokeh_Select
            if self.metsel.value in self.renamer.values():
                metric_name = [k for (k, v) in self.renamer.items() 
                                if v == self.metsel.value][0]
            
            else:
                metric_name = self.metsel.value
            
            metric_attrib = self.param_get(metric_name, self.root, self.platform)
            print(metric_attrib)
            
            cycle_filt = lambda x:x['Cycles Completed'] >= int(metric_attrib['cycles'])
            self.df = self.df.loc[cycle_filt]      
            self.s_kwargs['metric_attrib'] = metric_attrib
                

    def update(self, attr, old, new):
        """
        Updates the output
        """
        if hasattr(self, 'root'):
            self.update_attrib()
        
        self.df = self.df[-int(self.lastsel.value):]
        
        #If categories, create box plots
        if hasattr(self, 'cato'):
            self.s_kwargs['cato'] = self.catosel.value
            
            pb = boxplot.create_boxplot(self.df,
                                        self.metsel.value,
                                        **self.s_kwargs)
            self.layout.children[2] = pb
            
            pt = table.create_table(self.df,
                                    self.metsel.value,
                                    **self.s_kwargs)
            self.layout.children[3] = pt
            
        ps = scatter.create_scatter(self.df, 
                                   self.metsel.value,
                                   self.xaxis, 
                                   **self.s_kwargs)    

        self.layout.children[1] = ps


    def run(self):#, onscatter=True, onboxplot=False, tableon=False):
        """
        Run for server to work
        """
        self.create_widgets()     
      
        if hasattr(self, 'root'):
            self.update_attrib()
        
        self.df = self.df[-int(self.lastsel.value):]
        
        #Create layout of the page 
        if hasattr(self, 'cato'):
            self.s_kwargs['cato'] = self.catosel.value
            ps = scatter.create_scatter(self.df, 
                                       self.metsel.value,
                                       self.xaxis, 
                                       **self.s_kwargs)
            
            pb = boxplot.create_boxplot(self.df,
                                        self.metsel.value,
                                        **self.s_kwargs)
      
            pt = table.create_table(self.df,
                                    self.metsel.value,
                                    **self.s_kwargs)
        
            self.layout = column(row(self.mets_box, self.catos_box, self.lasts_box), 
                                 ps, pb, pt)

        else: 
            print(self.metsel.value, self.xaxis)
            ps = scatter.create_scatter(self.df, 
                                       self.metsel.value,
                                       self.xaxis, 
                                       **self.s_kwargs)
            self.layout = column(row(self.mets_box, self.lasts_box), ps)
            
            
            
        self.metsel.on_change('value', self.update)
        self.lastsel.on_change('value', self.update)
        if hasattr(self, 'cato'):
            self.catosel.on_change('value', self.update)
        
        curdoc().add_root(self.layout)       
        