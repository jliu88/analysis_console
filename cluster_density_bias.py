from os import path

import pandas as pd
from hayspcconsole.analysis_console import Console

DIRT = r'C:\Users\jliu\Box Sync\Process Engineering\Projects\MiSeq Cluster Density\Analysis\QC FIT Bias'
DS = 'CD_Offset.xlsx'
METRIC = ['Diff']
CATEGORY = ['PhiXLot']
#XML_DIRT = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\NovaSeq\FIT'
#XML = 'NovaSeq_FIT_SPC.xml'

ds_path = path.join(DIRT,DS)
#xml_path = path.join(XML_DIRT, XML)

CONV= {'Serial Number' : 'SerialNumber',
        'Start Date' : 'StartDate'}

df = pd.read_excel(ds_path)

#Without category
#==============================================================================
# foo = Console(df, 
#               METRIC, 
#               'Run_Date')
# foo.run()
# 
# 
#==============================================================================


#With category
df.dropna(subset=CATEGORY, inplace=True)

foo = Console(df, 
              METRIC, 
              'StartDate',
              )
              #cato=CATEGORY,
              #platform='Data',
              #renamer=CONV)
foo.run()
#==============================================================================

#foo = Console(df,
#              ['Prephasing_R2'],
#              'Run_Date',
#              cato=['Flowcell_Lot'])
#
#foo.run()
