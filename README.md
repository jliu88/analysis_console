# Scatter_by_Category

This module uses Bokeh to create a simple interactive scatter chart with tooltips, with the additional flexibility of differentiating categories by colors. 

##Installation

Requires Bokeh and panda

Copy Scatter_by_Category.py to a local directory and import with another program


##Usage
Create a program that gives Scatter_by_Category.gen_charts() the following parameters. 

###Required parameters
**ds_loc**: dataframe or string location of the excel document with all the data. Column headers must be on the first row and is recommended to not include spaces. If there are spaces then they can be changed with the **renamer** parameter.

Required column headers are: 
>SerialNumber

>StartDate

**metric_list**: list of string column titles of metrics that will be plotted. List entries **must** match column titles in the excel document. No spaces! 

Using only the required parameters, we are able to create a simple scatter chart over time with a tooltip of the serial number and metric value. 


###Optional Parameters
**cat_list**: list of string column titles of categories to separate data. List entries must match column titles. No spaces!

**col_list**: list of colors to separate the categories by. Assigned default colors if none is given

**renamer**: dict of column titles to rename in order to remove spaces or find columns to assign serial number and start date to. e.g. 
>{'Serial Number' : 'SerialNumber', 'Date': 'StartDate'}

**xml_loc**: string location of xml file. xml structure must follow a specific template

**platform**: string title of the platform in the xml file

###Running
Run a bokeh server and point it at the script directory. 

For example, create a script name plotter.py that uses Scatter_by_Category.gen_charts().
Then run:
>bokeh serve plotter.py

Now navigate to the following URL in a browser:
>http://localhost:5006/plotter.py

###In Progress
1. Allow selection of x axis to plot by
2. Add pictures in README
3. Add additional information regarding xml structure and usage

##Contributing

##Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request :D
##History

TODO: Write history

##Credits

TODO: Write credits

