import pandas as pd
# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, 'c:/Users/Rui Antao/projects/custom/')
import parameters
import generalfunctions
import datetime

paramfile  = r'c:/Users/Rui Antao/projects/investments/source/params.ini'
paramsection     = 'rawdata'

def projectparams():
    params = parameters.params(paramfile,paramsection)
    return params


def convertcommatodot(ivalue):
    convertvalue = ivalue.replace('.','').replace(',','.')
    return convertvalue


def calculateexpense(imovements,iitem,iyear):
    expense = imovements[imovements['Descricao'].str.contains(iitem)]
    #month = 12    
    expenseall = pd.DataFrame([])
    for month in range(1,13):
      first_day = datetime.datetime(iyear,month, 1)
      last_day = generalfunctions.last_day_of_month(datetime.datetime(iyear,month, 1))
      expensemonth = pd.DataFrame([])
      expensemonthday =  pd.DataFrame([])
      expensemonthday = expense[(expense['Datamov'] >= first_day) & (expense['Datamov'] <= last_day)]
      expensemonth = expensemonthday.groupby('Descricao')['NewDebito'].sum().reset_index()
      expensemonth['month'] = month
      expenseall = expenseall.append(expensemonth,ignore_index=True)
 
    return expenseall 









def readFileCGD(year):
    paramsCGD = projectparams()
    movementsCGDfile = paramsCGD['principaldir'] + paramsCGD['datadirectory'] + paramsCGD['movements']
    movementsCGDdata = pd.read_csv(movementsCGDfile,sep=';')

    movementsCGDdata['Datamov']   = pd.to_datetime(movementsCGDdata['Datamov'], format='%d-%m-%Y')
    movementsCGDdata['Datavalor'] = pd.to_datetime(movementsCGDdata['Datavalor'], format='%d-%m-%Y')
    movementsCGDdata['NewDebito'] = movementsCGDdata.apply(lambda x: convertcommatodot(str(x['Debito'])),axis=1)
    movementsCGDdata['NewDebito'] = movementsCGDdata['NewDebito'].astype(float)

    # use apply with lambda
    totalexpense = pd.DataFrame([])
    metlife    = calculateexpense(movementsCGDdata,'METLIFE',year)
    fidelidade = calculateexpense(movementsCGDdata,'FIDELIDADE',year)
    totalexpense = totalexpense.append(metlife,ignore_index=True)
    totalexpense = totalexpense.append(fidelidade,ignore_index=True)
    print(totalexpense)
    



if __name__ == "__main__":
  try:
    readFileCGD(2021) 
    

    

  
  except KeyboardInterrupt:
     print('\n')