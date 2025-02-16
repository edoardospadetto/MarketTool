from data_mining.frankfurt_se import scan_Frankfurt_SE,  bond_interest_rate_widget_frankfurtse,bond_master_data_frankfurtse
from data_mining.website_requests import BoerseFrankfurt_GetLastPrice_Raw
from utils.time_misc import toUnixTimestamp
from utils.scraping_misc import  go_down
import json
import pandas as pd
import os
import datetime

OPCONTINUE = 'continue'
OPSTART ='start'
op = OPCONTINUE #OPSTART
dbname='frankfurtSE_bonds.csv'
path = "data/BondsData/"
dbs = os.listdir(path)
dbs = [db for db in dbs if 'frankfurt' in db.lower()]
if(len(dbs)>1 and op!= OPCONTINUE):
    raise Exception('Error, frankfurt SE bonds database is not unique')
elif(len(dbs)==0 and op==OPCONTINUE):
    raise Exception('Error, frankfurt SE bonds database missing')


columns = ["name","type", "subtype", "isin", "currency", "issuer",
           "issueDate", "maturity", "startInterestDate", "coupon",
           "interestPaymentCycle", "lastPrice", "lastPriceTimeStamp"]


if(op == OPSTART):
    df = pd.DataFrame(columns = columns)
    maxnum = 25
    new_offset=0
    c_offset = -maxnum

elif (op == OPCONTINUE):
    df = pd.read_csv(path+dbname)
    dfcolumns = set(df.columns)
    print(dfcolumns)
    print(columns)
    print(len(df))
    maxnum = 25
    new_offset=len(df)
    c_offset = len(df)-maxnum
    if ( set(columns) != set(dfcolumns) ):
        raise Exception('Error, frankfurt SE bonds database corrupted')


while(c_offset==new_offset-maxnum):
    c_offset=new_offset
    LastPriceTimeStamp = toUnixTimestamp(datetime.datetime.now())

    data, new_offset = scan_Frankfurt_SE(asset_type = 'bond', num = maxnum, offset=c_offset)


    for k,d in data.items():
        try:
            raw=BoerseFrankfurt_GetLastPrice_Raw(d['isin'])
            raw = json.loads(raw)
            d1=bond_interest_rate_widget_frankfurtse(d['isin'])
            d2=bond_master_data_frankfurtse(d['isin'])
            print('d1',d1)
            print('d2',d1)

            #print(data2)

            row = [ d['name']['originalValue'], 'bond',d2['type']['translations']['en'], d['isin'],
                    d['keyData']['currency']['originalValue'], d2['issuer'], d2['issueDate'],d2['maturity'],
                   d1['startInterestPayment'],go_down(d,['keyData','coupon']),go_down(d1,['interestPaymentCycle','originalValue']),
                   d['lastQuote'], LastPriceTimeStamp ]

            df.loc[len(df)] = row
            print(row)
        except:
            print('bad')
    df.to_csv(path+dbname,index=False)
