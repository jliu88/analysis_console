from os import path

import pandas as pd
from hayspcconsole.analysis_console import Console

DIRT = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\MiSeq\OP750\MiSeqRUO'
DS = 'MiSeq FIT Data.xlsx'
METRIC = ['Q30', 'ReadsPF', 'ClusterDensity', 'RunTime']
CATEGORY = ['ReagentLot', 'PhiXLot', 'Flowcell_Lot']
XML_DIRT = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\MiSeq\OP750\MiSeqRUO'
XML = 'MiSeq_OP750_SPC.xml'

ds_path = path.join(DIRT,DS)
xml_path = path.join(XML_DIRT, XML)

CONV = {'Serial Number':'SerialNumber',
        'Start Date':'StartDate',
        'Cluster Density' : 'ClusterDensity',
        'Reads PF' : 'ReadsPF',
        'Run Time' : 'RunTime',
        'Phasing R1' : 'PhasingR1',
        'Phasing R2' : 'PhasingR2',
        'Prephasing R1' : 'PrephasingR1',
        'Prephasing R2' : 'PrephasingR2',
        'Q30 R1' : 'Q30R1',
        'Q30 R2' : 'Q30R2'}

df = pd.read_excel(ds_path)

#Without category
#foo = Console(df, 
#              METRIC, 
#              'StartDate', 
#              renamer=CONV,
#              xml_loc=xml_path,
#              platform='MiSeqRUO')
#foo.run()




#With category
foo = Console(df, 
              METRIC, 
              'StartDate', 
              renamer=CONV,
              cato=CATEGORY,
              xml_loc=xml_path,
              platform='MiSeqRUO')
foo.run()
