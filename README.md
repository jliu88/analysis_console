# analysis_console

This module uses Bokeh to create a simple interactive scatter chart with tooltips, with the additional flexibility of differentiating categories by colors. 

# Installation

Requires Bokeh and panda

Copy analysis_console.py to a local directory and import with another program.

# Usage
Create a script that imports analysis_console and feed it parameters.

See example.py for examples 

## Required Arguments
- **df** (df or str): dataframe or string location of the excel document with all the data. Column headers must be on the first row and is recommended to not include spaces. If there are spaces then they can be changed with the **renamer** parameter.

Additional information can be stored in the tooltips if the column header is:
```
SerialNumber
```

- **metric** (list): string column titles of metrics that will be plotted. List entries **must** match column titles in the excel document. No spaces! 

- **xaxis** (str): column title for the x axis

## Optional Arguments
- **cato** (list): string column titles of categories to separate data. List entries must match column titles. No spaces!

- **col** (list): colors to separate the categories by. Default is Set1[9]

- **renamer** (dict): column titles to rename in order to remove spaces or find columns to assign serial number to. e.g. 
```
{'Serial Number' : 'SerialNumber', 'Date': 'StartDate'}
```
- **xml_loc** (str): location of xml file. xml structure must follow a specific template

- **platform** (str): title of the platform in the xml file

# Running
## Writting the script
Import the module and feed it arguments. For example:
```
import analysis_console
x = analaysis_console.tools(df, metric, xaxis)
x.run()
```

See example.py for additional examples

## Displaying the chart
Run a bokeh server and point it at the script directory. 

For example, if your script is named example.py.
Open the console and run:
```
bokeh serve example.py
```

Now navigate to the following URL in a browser:
```
http://localhost:5006/example
```

To directly open the page, you can also enter into the console:
```
bokeh serve example.py --show
```

# In Progress
1. Allow xaxis to be selectable 
2. Add pictures in README
3. Add additional information regarding xml structure and usage

# Contributing

# Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request :D
# History

TODO: Write history

# Credits

TODO: Write credits

