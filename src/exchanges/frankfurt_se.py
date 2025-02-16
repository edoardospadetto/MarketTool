
import json
import urllib
import html_to_json
import requests

from  src.misc.long_payloads import GoodHeaders_FrankfurtSE
from  src.misc.scraping_misc import go_down

import json
from websocket import create_connection


def bond_master_data_frankfurtse(isin):
    apiurl = "https://api.boerse-frankfurt.de/v1/data/master_data_bond?isin="+isin
    apiheaders = GoodHeaders_FrankfurtSE(apiurl)
    req = urllib.request.Request(apiurl, headers=apiheaders)
    resp =  urllib.request.urlopen(req)
    bond_data=json.loads(resp.read().decode('utf-8'))
    return(bond_data)


def bond_interest_rate_widget_frankfurtse(isin):
    apiurl = "https://api.boerse-frankfurt.de/v1/data/interest_rate_widget?isin="+isin
    apiheaders = GoodHeaders_FrankfurtSE(apiurl)
    req = urllib.request.Request(apiurl, headers=apiheaders)
    resp =  urllib.request.urlopen(req)
    bond_data=json.loads(resp.read().decode('utf-8'))
    return(bond_data)

def equity_key_data_Frankfurt_SE(isin):
    apiurl = "https://api.boerse-frankfurt.de/v1/data/equity_key_data?isin="+isin
    apiheaders = GoodHeaders_FrankfurtSE(apiurl)
    req = urllib.request.Request(apiurl, headers=apiheaders)
    resp =  urllib.request.urlopen(req)

    stock_data=json.loads(resp.read().decode('utf-8'))
    #
    stock_data.pop("marketCapitalizationExtended")
    return(stock_data)

def get_slug_Frankfurt_SE(isin):
    url = 'https://api.boerse-frankfurt.de/v1/global_search/limitedsearch/de?searchTerms='+isin
    headers = GoodHeaders_FrankfurtSE(url)

    req = urllib.request.Request(url, headers=headers)
    resp =  urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))[0][0]['slug']
    return(data)

def get_token_Frankfurt_SE():
    url = 'https://api.boerse-frankfurt.de/v1/mdstokenservice/token'
    headers = GoodHeaders_FrankfurtSE(url,type=2)
    req = urllib.request.Request(url, headers=headers)
    resp =  urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    return(data['token'])


def get_price_hystory(isin, resolution,from_date,to_date):

    url = 'https://api.boerse-frankfurt.de/v1/tradingview/history'
    token = get_token_Frankfurt_SE()
    headers = GoodHeaders_FrankfurtSE(url,type=1)

    auth = {"subscribeAuthentication":{"token":token},"requestId":"request-1"}
    url_auth = "wss://mds.ariva-services.de/api/v1/marketstates/ws"

    json_data = {
    'symbol': 'XFRA:'+isin,
    'resolution': resolution,
    'from': from_date,
    'to': to_date,
    }

    url = "https://api.boerse-frankfurt.de/v1/tradingview/history?symbol={symbol}&resolution={resolution}&from={from}&to={to}&countback=329"
    url_built=url
    for k,v in json_data.items():
        url_built = url_built.replace("{"+k+"}", str(v))
    print(url_built)

    req = urllib.request.Request(url_built, headers=headers, method='GET')
    resp =  urllib.request.urlopen(req)

    data = json.loads(resp.read().decode('utf-8'))


    return(data)

def equity_ticker_Frankfurt_SE(slug):
    dummyheaders={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    url2 = "https://www.boerse-frankfurt.de/equity/"+str(slug.encode('utf-8'))[2:-1].replace('\\x','%')
    req = urllib.request.Request(url2, headers=dummyheaders)

    resp =  urllib.request.urlopen(req)
    page=html_to_json.convert(resp)


    tree_sym = ['html', 0, 'body', 0, 'app-root', 0, 'app-wrapper', 0, 'div', 0, 'div', 0, 'div', 1, 'app-equity', 0,
                    'div', 0, 'div', 0, 'app-widget-datasheet-header', 0, 'div', 0, 'div', 0, 'div', 0, 'div', 0, 'div', 1, 'div', 0, 'span', 2, '_value']

    a = go_down(page,tree_sym).split(':')[1][1:]

    return(a)



def scan_Frankfurt_SE(asset_type = "equity", num = 500, offset=0):

    if(num > 500):
        raise
    dummyheaders={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }


    json_data = {
        'indices': [],
        'regions': [],
        'countries': [],
        'sectors': [],
        'types': [],
        'forms': [],
        'segments': [],
        'markets': [],
        'stockExchanges': [],
        'lang': 'en',
        'offset': offset,
        'limit': num,
        'sorting': 'TURNOVER',
        'sortOrder': 'DESC',
    }



    tot = 0
    thisLen = num
    c_fundam = ['alpha250', 'alpha30', 'beta250', 'beta30', 'correlation250', 'correlation30', 'dividendPerShare', 'dividendPerShareExtra', 'dividendYear', 'dividendYield', 'isin', 'marketCapitalization',
                    'numberOfShares', 'performanceKeysReferenceTime', 'priceEarningsRatio', 'sharpeRatio250', 'sharpeRatio30', 'volatility250', 'volatility30', 'winPerShare']


    idx = 0
    dataOut={}

    url = 'https://api.boerse-frankfurt.de/v1/search/'+asset_type+'_search'
    headers = GoodHeaders_FrankfurtSE(url)
    data = json.dumps(json_data)
    data = str(data)
    data = data.encode('utf-8')

    req = urllib.request.Request(url, headers=headers, data=data)
    resp =  urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))['data']
    thisLen = len(data)


    for d in data:
        print(idx, d['isin'],str(d['slug'].encode('utf-8'))[2:-1].replace('\\x','%'))
        idx+=1

        if(asset_type == 'equity'):
            equity_key_data= equity_key_data_Frankfurt_SE(d['isin'])
            ticker=equity_ticker_Frankfurt_SE(d['slug'])
            dataOut[idx] = equity_key_data
            data['ticker'] = ticker
            data["name"] = d['name']['originalValue']
        elif(asset_type == 'bond'):
            dataOut[str(idx)] = d


    offset +=len(data)
    return(dataOut, offset)
