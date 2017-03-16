# analysis_console

This module uses Bokeh to create a simple interactive scatter chart with tooltips, with the additional flexibility of differentiating categories by colors. 

## Installation

Requires Bokeh and panda

Copy analysis_console.py to a local directory and import with another program.

## Usage
Create a script that imports analsyis_console and feed it parameters.


See example.py for example 

### Required parameters
**df**: dataframe or string location of the excel document with all the data. Column headers must be on the first row and is recommended to not include spaces. If there are spaces then they can be changed with the **renamer** parameter.

Additional information can be stored in the tooltips if the column header is:
>SerialNumber

**metric**: list of string column titles of metrics that will be plotted. List entries **must** match column titles in the excel document. No spaces! 

Using only the required parameters, we are able to create a simple scatter chart over time with a tooltip of the serial number and metric value. 

**xaxis**: column title for the x axis

### Optional Parameters
**cato**: list of string column titles of categories to separate data. List entries must match column titles. No spaces!

**col**: list of colors to separate the categories by. Default is Set1[9]

**renamer**: dict of column titles to rename in order to remove spaces or find columns to assign serial number and start date to. e.g. 
>{'Serial Number' : 'SerialNumber', 'Date': 'StartDate'}

**xml_loc**: string location of xml file. xml structure must follow a specific template

**platform**: string title of the platform in the xml file

### Running
#### Writting the script
Import the module and feed it arguments. For example:

x = analaysis_console.tools(df, metric)

x.run()

See example.py for additional examples

#### Displaying the chart
Run a bokeh server and point it at the script directory. 

For example, if your script is named example.py.
Open the console and run:
>bokeh serve example.py
Now navigate to the following URL in a browser:
>http://localhost:5006/plotter.py

You can also enter:
>bokeh serve example.py --show
and it will directly open the page

### In Progress
1. Add pictures in README
2. Add additional information regarding xml structure and usage

## Contributing

## Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request :D
## History

TODO: Write history

## Credits

TODO: Write credits

