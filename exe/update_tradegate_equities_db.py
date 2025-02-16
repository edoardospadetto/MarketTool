from data_mining.tradegate_se import  search_tradegate,get_price_tradegate
import html_to_json
from utils.scraping_misc import go_down, find_path
import os
from utils.time_misc import toUnixTimestamp
import pandas as pd
import datetime
def clean_row(a_row):
    #print(a_row)
    # if('b' in a_row.keys()):
    #     a = go_down(a_row, ['b',0,'_value']).join(go_down(a_row,['_values']))
    # else:
    a = go_down(a_row, ['_value'])
    return(a)


def scan_tradegate_stocks_query(query, skip_isins=[]):
    c = search_tradegate(query)
    c=c.decode('utf-8').replace('<b>','')
    c=c.replace('</b>','')
    c = html_to_json.convert(c)
    path1 = find_path(c,"Mercedes-Benz" )
    path2 = find_path(c, "Novo-Nordisk" )

    prow = ['html', 0, 'body', 0, 'div', 0, 'div', 0, 'div', 0, 'div', 0, 'div', 1, 'div', 0, 'div', 0, 'table', 0, 'tbody', 0, 'tr']
    lpp = ['html', 0, 'body', 0, 'div', 0, 'div', 0, 'div', 0, 'div', 0, 'div', 3, 'div', 0, 'div', 0, 'div', 1, 'table', 1, 'tr', 4, 'td', 0, 'strong', 0, '_value']
    table = go_down(c,prow)

    output = []

    for row in table:

        c = go_down(row,['td',1,'_value'])
        if c in skip_isins:
            print(c,'skip')
            continue
        a = go_down(row,['td',3,'_value'])
        d = go_down(row,['td',0,'a',0,'_value'])
        b = go_down(row,['td',2,'_value'])
        f = go_down(html_to_json.convert(get_price_tradegate(c)),lpp)
        out = {'name':d,'isin':c,'ticker':a,'wkn':b,'lastPrice':f,'lastPriceTimeStamp':toUnixTimestamp(datetime.datetime.now())}
        print(out)
        output.append(out)
    return(output)


OPCONTINUE = 'continue'
OPSTART ='start'
op = OPCONTINUE
dbname='tradegateSE_stocks.csv'
path = "data/StocksData/"
dbs = os.listdir(path)
dbs = [db for db in dbs if 'tradegate' in db.lower()]
if(len(dbs)>1 and op!= OPCONTINUE):
    raise Exception('Error, tradegate SE stocks database is not unique')
elif(len(dbs)==0 and op==OPCONTINUE):
    raise Exception('Error, tradegate SE stocks database missing')


columns = ['name', 'isin', 'ticker', 'wkn', 'lastPrice','lastPriceTimeStamp']

if(op == OPSTART):
    df = pd.DataFrame(columns = columns)
    skip_isins0=[]
    df.to_csv(path+dbname,index=False)
elif (op == OPCONTINUE):
    df = pd.read_csv(path+dbname, index_col=False)
    skip_isins0=list(df.loc[:,'isin'])
    dfcolumns = set(df.columns)


    if ( set(columns) != set(dfcolumns) ):
        raise Exception('Error, tradegate SE stocks database corrupted')






s = "abcdefghijklmnopqrstuvwxyz0123456789"


for s in s:
    df = pd.read_csv(path+dbname, index_col=False)
    o = scan_tradegate_stocks_query(s, skip_isins=skip_isins0)
    skip_isins0 = list ( set ( skip_isins0 + [io['isin'] for io in o] ))
    print('saving...')
    for io in o:
        df.loc[len(df)] = io
    df.to_csv(path+dbname,index=False)
    print('DONE!')
