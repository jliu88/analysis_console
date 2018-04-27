from os import path

import pandas as pd
from hayspcconsole.analysis_console import Console

DIRT = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\NovaSeq\FIT'
DS = 'NovaSeq_FIT_Data.xlsx'
METRIC = ['Q30_Read1', 'Q30_Read2', 'Q30_Total', 'Run_Time', 'Yield_Total',
          'Prephasing_R1', 'Prephasing_R2', 'Phasing_R1', 'Phasing_R2',
          '%_PF', 'Resynthesis', 'Cycle1_Intensity', 'Error_Rate', 'FWHM_Green',
          'FWHM_Red', 'SD_FWHM_Green']
CATEGORY = ['SBS_Lot', 'Buffer_Lot', 'Flowcell_Lot', 'Flowcell_Group']
XML_DIRT = r'\\ushw-file\users\transfer\Hayward_Statistical_Process_Control\Control_Charts\NovaSeq\FIT'
XML = 'NovaSeq_FIT_SPC.xml'

ds_path = path.join(DIRT,DS)
xml_path = path.join(XML_DIRT, XML)

CONV= {'Total_Cycles': 'Cycles Completed'}

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
              'Run_Date',
              cato=CATEGORY,
              xml_loc=xml_path,
              platform='Data',
              renamer=CONV)
foo.run()
#==============================================================================

#foo = Console(df,
#              ['Prephasing_R2'],
#              'Run_Date',
#              cato=['Flowcell_Lot'])
#
#foo.run()
