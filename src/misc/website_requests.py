import requests
import time
import html_to_json
from websockets.sync.client import connect


from src.long_payloads import *
from src.scraping_misc import *





def JustEtf_GetLastPrice_Raw(cookies, headers, isin, currency='EUR' ):
    url = 'https://www.justetf.com/api/etfs/'+isin+'/quote?currency=EUR&locale=it'

    ress = requests.get(
        url,
        cookies=cookies,
        headers=headers
    )
    price_raw  = ress.content.decode('utf-8')
    return(price_raw)


def BoerseFrankfurt_GetLastPrice_Raw(isin):

    url = 'https://api.boerse-frankfurt.de/v1/mdstokenservice/token'

    headers = GoodHeaders_FrankfurtSE(url, type=2)


    response = requests.get(url, headers=headers)
    token = json.loads(response.content)['token']


    data = {"subscribeAuthentication":{"token":token},"requestId":"request-1"}

    data1 = {"subscribeMarketstates":{"marketstateQueries":[isin]},"requestId":"request-1"}
    with connect("wss://mds.ariva-services.de/api/v1/marketstates/ws") as websocket:
        websocket.send(json.dumps(data))
        message = websocket.recv()
        websocket.send(json.dumps(data1))
        message = websocket.recv()

    return(message)


def Nasdaq_GetLastPrice_Raw(ticker):
    headers = get_nasdaq_stocks_headers()
    response = requests.get(
        'https://api.nasdaq.com/api/quote/watchlist?symbol='+ticker.lower()+'%7cstocks',
        headers=headers,
    )

    return(response.content)

def ECB_Eur_ExchangeRates_RAW():
    url="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
    response = requests.get(url)
    return(response.content)

def  ECB_Eur_ExchangeRates():

    content = ECB_Eur_ExchangeRates_RAW()
    pathToTable=['html', 0, 'body', 0, 'div', 2, 'main', 0, 'div', 2, 'div', 1, 'div', 0, 'div', 0, 'table', 0, 'tbody', 0, 'tr']
    pathToVal = ['td', 2, 'a', 0, 'span', 0, '_value']
    pathToCode = ['td', 0, 'a',0,'_value']
    pathToName = ['td', 1, 'a', 0,'_value']

    table = go_down(html_to_json.convert(content),pathToTable)

    data={}

    for i in range(len(table)):
        name = go_down(table[i],pathToName)
        code = go_down(table[i],pathToCode)
        value = go_down(table[i],pathToVal)
        data[code] = {'name':name,'value':value}

    return data


# hello()
