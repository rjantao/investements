import pandas as pd
import sys
sys.path.insert(0, 'c:/Users/Rui Antao/projects/custom/')
import parameters
import numpy as np


paramfile  = r'c:/Users/Rui Antao/projects/investments/source/params.ini'
paramsection     = 'rawdata'

def projectparams():
    params = parameters.params(paramfile,paramsection)
    return params

def vgaleoldobjects():
    params = projectparams()
    objectsvgaleold = params['principaldir'] + params['datadirectory'] + 'prodvgale11.dsv'
    objectsdataold = pd.read_csv(objectsvgaleold,sep=';')
    print(objectsdataold)
    objectsvgalenew = params['principaldir'] + params['datadirectory'] + 'bdgalenew.dsv'
    objectsdatanew = pd.read_csv(objectsvgalenew,sep=';')
    print(objectsdatanew)

    merged = objectsdataold.merge(objectsdatanew, how='left', 
                    left_on=['OBJECT_NAME','OBJECT_TYPE'],
                    right_on=['OBJECT_NAMEN','OBJECT_TYPEN'])
  
    merged ['Match'] = merged.apply(lambda row:'N' if row['OBJECT_TYPEN'] is np.NaN else 'Y',axis=1)
    mergednotmatch   =  merged[(merged['Match']=='N')].reset_index()
    comparevgale = params['principaldir'] + params['datadirectory'] + 'comparevgale.csv'
    
    mergednotmatch.to_csv(comparevgale)
    print(mergednotmatch)



if __name__ == "__main__":
  try:
    vgaleoldobjects()

  
  except KeyboardInterrupt:
     print('\n')