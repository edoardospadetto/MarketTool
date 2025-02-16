import hashlib
import requests
import pandas as pd
import json
import datetime
import re

from src.time_misc import  IsDataOlderOneHour, IsDataOlderTenMinutes,toUnixTimestamp


def GoodHeaders_FrankfurtSE(url='https://api.boerse-frankfurt.de/v1/search/equity_search', type=1):
    tracing_salt = "w4ivc1ATTGta6njAZzMbkL3kJwxMfEAKDa3MNr"
    tracing_id = "ea65e63f-b88f-414f-b1a9-e035263c8b0f"
    mydate = datetime.datetime.utcnow()
    datez= mydate.strftime('%FT%T.%f')[:-3]+'Z'
    datecompact =  mydate.strftime('%Y%m%d%H%M')


    s = datez + url + tracing_salt;
    xtraceid = hashlib.md5(s.encode()).hexdigest()
    xsec= hashlib.md5(datecompact.encode()).hexdigest()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.boerse-frankfurt.de',
        'priority': 'u=1, i',
        'referer': 'https://www.boerse-frankfurt.de/',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-client-traceid':xtraceid,
        'x-security':xsec
    }
    if(type==1):
        headers['client-date'] = datez
    elif(type==2):
        idx = url.index('de/')+2
        url_path =url[idx:]
        for i in range(9):
            if('/v'+str(i) in url_path) :
                url_path = url_path.replace('/v'+str(i), "")

        #let K = new URL(a.url).pathname.replace(/\/v[0-9]{1,}/, "") + "@" + M + "W" + u.N.mds.tracingId;
        x_request_trace_id = url_path +'@' + datez +"W" + tracing_id
        #/mdstokenservice/token@2024-09-14T16:25:34.813ZWea65e63f-b88f-414f-b1a9-e035263c8b0f
        headers['x-request-trace-id'] = hashlib.sha256((x_request_trace_id).encode('utf-8')).hexdigest()
        headers['x-request-datetime'] = datez

    return(headers)


def get_justetf_list_payload():

    headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.justetf.com',
            'priority': 'u=1, i',
            'referer': 'https://www.justetf.com/it/search.html?search=ETFS',
            'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    df = pd.read_csv('data/ServerIdentityData/serverIdentity.csv')
    dfmasked = df.loc[ df.loc[:,'website'] == 'www.justetf.com' ]
    dfmasked = df.loc[ df.loc[:,'cookie'] == 'JSESSIONID' ]

    valueJSESSION = df.loc[0,'value']
    lastTimeStamp = df.loc[0,'lastTimeStamp']


    cookies = {}
    if(IsDataOlderTenMinutes(lastTimeStamp)):
        print('UPDATE: Just ETF Cookie JSESSIONID ')
        relevant=[ 'JSESSIONID' ]

        response = requests.get('https://www.justetf.com/it/search.html', params={}, cookies=cookies, headers=headers)
        cookiesTMP = [a.split('=') for a in response.headers['Set-Cookie'].split(';')]

        for c in cookiesTMP:
            for r in relevant:
                if r in c[0]:
                    cookies[r]=c[1]
                    break
        row = dfmasked.index.values.astype(int)[0]
        df.loc[row,'value'] = cookies["JSESSIONID"]
        df.loc[row,'lastTimeStamp'] = toUnixTimestamp(datetime.datetime.now())
        df.to_csv('data/ServerIdentityData/serverIdentity.csv', index = False)
    else:
        cookies['JSESSIONID'] = valueJSESSION


    data = {
        'draw': '10',
        'columns[0][data]': '',
        'columns[0][name]': 'selectCheckbox',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'name',
        'columns[1][name]': 'name',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'true',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': '',
        'columns[2][name]': 'sparkline',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'fundCurrency',
        'columns[3][name]': 'fundCurrency',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'true',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'fundSize',
        'columns[4][name]': 'fundSize',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'true',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'ter',
        'columns[5][name]': 'ter',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'true',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': '',
        'columns[6][name]': 'bullet',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'weekReturnCUR',
        'columns[7][name]': 'weekReturn',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'true',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'columns[8][data]': 'monthReturnCUR',
        'columns[8][name]': 'monthReturn',
        'columns[8][searchable]': 'true',
        'columns[8][orderable]': 'true',
        'columns[8][search][value]': '',
        'columns[8][search][regex]': 'false',
        'columns[9][data]': 'threeMonthReturnCUR',
        'columns[9][name]': 'threeMonthReturn',
        'columns[9][searchable]': 'true',
        'columns[9][orderable]': 'true',
        'columns[9][search][value]': '',
        'columns[9][search][regex]': 'false',
        'columns[10][data]': 'sixMonthReturnCUR',
        'columns[10][name]': 'sixMonthReturn',
        'columns[10][searchable]': 'true',
        'columns[10][orderable]': 'true',
        'columns[10][search][value]': '',
        'columns[10][search][regex]': 'false',
        'columns[11][data]': 'yearReturnCUR',
        'columns[11][name]': 'yearReturn',
        'columns[11][searchable]': 'true',
        'columns[11][orderable]': 'true',
        'columns[11][search][value]': '',
        'columns[11][search][regex]': 'false',
        'columns[12][data]': 'threeYearReturnCUR',
        'columns[12][name]': 'threeYearReturn',
        'columns[12][searchable]': 'true',
        'columns[12][orderable]': 'true',
        'columns[12][search][value]': '',
        'columns[12][search][regex]': 'false',
        'columns[13][data]': 'fiveYearReturnCUR',
        'columns[13][name]': 'fiveYearReturn',
        'columns[13][searchable]': 'true',
        'columns[13][orderable]': 'true',
        'columns[13][search][value]': '',
        'columns[13][search][regex]': 'false',
        'columns[14][data]': 'ytdReturnCUR',
        'columns[14][name]': 'ytdReturn',
        'columns[14][searchable]': 'true',
        'columns[14][orderable]': 'true',
        'columns[14][search][value]': '',
        'columns[14][search][regex]': 'false',
        'columns[15][data]': 'yearReturn1CUR',
        'columns[15][name]': 'yearReturn1',
        'columns[15][searchable]': 'true',
        'columns[15][orderable]': 'true',
        'columns[15][search][value]': '',
        'columns[15][search][regex]': 'false',
        'columns[16][data]': 'yearReturn2CUR',
        'columns[16][name]': 'yearReturn2',
        'columns[16][searchable]': 'true',
        'columns[16][orderable]': 'true',
        'columns[16][search][value]': '',
        'columns[16][search][regex]': 'false',
        'columns[17][data]': 'yearReturn3CUR',
        'columns[17][name]': 'yearReturn3',
        'columns[17][searchable]': 'true',
        'columns[17][orderable]': 'true',
        'columns[17][search][value]': '',
        'columns[17][search][regex]': 'false',
        'columns[18][data]': 'yearReturn4CUR',
        'columns[18][name]': 'yearReturn4',
        'columns[18][searchable]': 'true',
        'columns[18][orderable]': 'true',
        'columns[18][search][value]': '',
        'columns[18][search][regex]': 'false',
        'columns[19][data]': 'yearVolatilityCUR',
        'columns[19][name]': 'yearVolatility',
        'columns[19][searchable]': 'true',
        'columns[19][orderable]': 'true',
        'columns[19][search][value]': '',
        'columns[19][search][regex]': 'false',
        'columns[20][data]': 'threeYearVolatilityCUR',
        'columns[20][name]': 'threeYearVolatility',
        'columns[20][searchable]': 'true',
        'columns[20][orderable]': 'true',
        'columns[20][search][value]': '',
        'columns[20][search][regex]': 'false',
        'columns[21][data]': 'fiveYearVolatilityCUR',
        'columns[21][name]': 'fiveYearVolatility',
        'columns[21][searchable]': 'true',
        'columns[21][orderable]': 'true',
        'columns[21][search][value]': '',
        'columns[21][search][regex]': 'false',
        'columns[22][data]': 'yearReturnPerRiskCUR',
        'columns[22][name]': 'yearReturnPerRisk',
        'columns[22][searchable]': 'true',
        'columns[22][orderable]': 'true',
        'columns[22][search][value]': '',
        'columns[22][search][regex]': 'false',
        'columns[23][data]': 'threeYearReturnPerRiskCUR',
        'columns[23][name]': 'threeYearReturnPerRisk',
        'columns[23][searchable]': 'true',
        'columns[23][orderable]': 'true',
        'columns[23][search][value]': '',
        'columns[23][search][regex]': 'false',
        'columns[24][data]': 'fiveYearReturnPerRiskCUR',
        'columns[24][name]': 'fiveYearReturnPerRisk',
        'columns[24][searchable]': 'true',
        'columns[24][orderable]': 'true',
        'columns[24][search][value]': '',
        'columns[24][search][regex]': 'false',
        'columns[25][data]': 'yearMaxDrawdownCUR',
        'columns[25][name]': 'yearMaxDrawdown',
        'columns[25][searchable]': 'true',
        'columns[25][orderable]': 'true',
        'columns[25][search][value]': '',
        'columns[25][search][regex]': 'false',
        'columns[26][data]': 'threeYearMaxDrawdownCUR',
        'columns[26][name]': 'threeYearMaxDrawdown',
        'columns[26][searchable]': 'true',
        'columns[26][orderable]': 'true',
        'columns[26][search][value]': '',
        'columns[26][search][regex]': 'false',
        'columns[27][data]': 'fiveYearMaxDrawdownCUR',
        'columns[27][name]': 'fiveYearMaxDrawdown',
        'columns[27][searchable]': 'true',
        'columns[27][orderable]': 'true',
        'columns[27][search][value]': '',
        'columns[27][search][regex]': 'false',
        'columns[28][data]': 'maxDrawdownCUR',
        'columns[28][name]': 'maxDrawdown',
        'columns[28][searchable]': 'true',
        'columns[28][orderable]': 'true',
        'columns[28][search][value]': '',
        'columns[28][search][regex]': 'false',
        'columns[29][data]': 'inceptionDate',
        'columns[29][name]': 'inceptionDate',
        'columns[29][searchable]': 'true',
        'columns[29][orderable]': 'true',
        'columns[29][search][value]': '',
        'columns[29][search][regex]': 'false',
        'columns[30][data]': 'distributionPolicy',
        'columns[30][name]': 'distributionPolicy',
        'columns[30][searchable]': 'true',
        'columns[30][orderable]': 'false',
        'columns[30][search][value]': '',
        'columns[30][search][regex]': 'false',
        'columns[31][data]': 'sustainable',
        'columns[31][name]': 'sustainable',
        'columns[31][searchable]': 'true',
        'columns[31][orderable]': 'true',
        'columns[31][search][value]': '',
        'columns[31][search][regex]': 'false',
        'columns[32][data]': 'numberOfHoldings',
        'columns[32][name]': 'numberOfHoldings',
        'columns[32][searchable]': 'true',
        'columns[32][orderable]': 'true',
        'columns[32][search][value]': '',
        'columns[32][search][regex]': 'false',
        'columns[33][data]': 'currentDividendYield',
        'columns[33][name]': 'currentDividendYield',
        'columns[33][searchable]': 'true',
        'columns[33][orderable]': 'true',
        'columns[33][search][value]': '',
        'columns[33][search][regex]': 'false',
        'columns[34][data]': 'yearDividendYield',
        'columns[34][name]': 'yearDividendYield',
        'columns[34][searchable]': 'true',
        'columns[34][orderable]': 'true',
        'columns[34][search][value]': '',
        'columns[34][search][regex]': 'false',
        'columns[35][data]': 'domicileCountry',
        'columns[35][name]': 'domicileCountry',
        'columns[35][searchable]': 'true',
        'columns[35][orderable]': 'false',
        'columns[35][search][value]': '',
        'columns[35][search][regex]': 'false',
        'columns[36][data]': 'replicationMethod',
        'columns[36][name]': 'replicationMethod',
        'columns[36][searchable]': 'true',
        'columns[36][orderable]': 'false',
        'columns[36][search][value]': '',
        'columns[36][search][regex]': 'false',
        'columns[37][data]': 'savingsPlanReady',
        'columns[37][name]': 'savingsPlanReady',
        'columns[37][searchable]': 'true',
        'columns[37][orderable]': 'false',
        'columns[37][search][value]': '',
        'columns[37][search][regex]': 'false',
        'columns[38][data]': 'hasSecuritiesLending',
        'columns[38][name]': 'hasSecuritiesLending',
        'columns[38][searchable]': 'true',
        'columns[38][orderable]': 'false',
        'columns[38][search][value]': '',
        'columns[38][search][regex]': 'false',
        'columns[39][data]': 'isin',
        'columns[39][name]': 'isin',
        'columns[39][searchable]': 'true',
        'columns[39][orderable]': 'false',
        'columns[39][search][value]': '',
        'columns[39][search][regex]': 'false',
        'columns[40][data]': 'ticker',
        'columns[40][name]': 'ticker',
        'columns[40][searchable]': 'true',
        'columns[40][orderable]': 'false',
        'columns[40][search][value]': '',
        'columns[40][search][regex]': 'false',
        'columns[41][data]': 'wkn',
        'columns[41][name]': 'wkn',
        'columns[41][searchable]': 'true',
        'columns[41][orderable]': 'false',
        'columns[41][search][value]': '',
        'columns[41][search][regex]': 'false',
        'columns[42][data]': 'valorNumber',
        'columns[42][name]': 'valorNumber',
        'columns[42][searchable]': 'true',
        'columns[42][orderable]': 'false',
        'columns[42][search][value]': '',
        'columns[42][search][regex]': 'false',
        'columns[43][data]': '',
        'columns[43][name]': 'addButton',
        'columns[43][searchable]': 'true',
        'columns[43][orderable]': 'false',
        'columns[43][search][value]': '',
        'columns[43][search][regex]': 'false',
        'order[0][column]': '4',
        'order[0][dir]': 'desc',
        'start': '0',
        'length': '25',
        'search[value]': '',
        'search[regex]': 'false',
        'ajaxsortOrder': 'desc',
        'ajaxsortField': 'fundSize',
        'lang': 'en',
        'country': 'IT',
        'defaultCurrency': 'EUR',
        'universeType': 'private',
        'etfsParams': 'search=ETFS&query=',
    }

    return(data,headers,cookies)



def get_amundi_payload():
	data = {
    "context": {
        "countryCode": "NLD",
        "countryName": "Netherlands",
        "googleCountryCode": "NL",
        "domainName": "www.amundietf.nl",
        "bcp47Code": "en-GB",
        "languageName": "English",
        "gtmCode": "GTM-KR9BS5J",
        "languageCode": "en",
        "userProfileName": "RETAIL",
        "userProfileSlug": "retail",
        "portalProfileName": 'null',
        "portalProfileSlug": 'null'
    },
    "productIds": [
        "LU1829218749"
    ],
    "characteristics": [
        "CESURE_COMMENTS",
        "FULL_PROPERTY_OF_THE_ASSETS",
        "FUND_BREAKDOWNS_AS_OF_DATE",
        "POSITION_AS_OF_DATE",
        "ISIN",
        "FUND_UCITS",
        "TOTAL_EXPENSE_RATIO",
        "EU_SD_STATUS",
        "FUND_ISSUER",
        "DOMICILE",
        "FUND_REPLICATION_METHODOLOGY",
        "FUND_SAMPLING",
        "SECURITIES_LANDING",
        "PORTFOLIO_MANAGERS",
        "FUND_PEA",
        "UMBRELLA_AUM",
        "FUND_FISCAL_YEAR_END",
        "MINIMUM_INVESTMENT",
        "TICKER",
        "DISTRIBUTION_POLICY",
        "TER",
        "NAV",
        "NAV_DISPLAYED",
        "NAV_DATE_DISPLAYED",
        "NAV_DATE_FOR_PERFORMANCE_CALCULATIONS",
        "BENCHMARK_NAME",
        "BENCHMARK_TICKER",
        "SECTORIAL_COMPOSITION",
        "CURRENCY_COMPOSITION",
        "PERFORMANCE_NAV",
        "PERFORMANCE_AUM",
        "FIRST_COTATION_DATE",
        "STRATEGY",
        "ASSET_CLASS",
        "INVESTMENT_ZONE",
        "INVESTMENT_TYPE",
        "ETF_CLASSIFICATION1",
        "BENCHMARK_INDEX_TYPE",
        "NUMBER_OF_COMPONENTS",
        "BENCHMARK_INDEX_CURRENCY",
        "SHARE_MARKETING_NAME",
        "OLD_SHARE_MARKETING_NAME",
        "SUBTYPE",
        "CURRENCY",
        "CURRENCY_HEDGE",
        "NULL",
        "SHARE_CLASSIFICATION_SHORT_LEVERAGE",
        "ESSENTIALS",
        "MNEMO",
        "KIID",
        "AUM",
        "CORE",
        "SRRI",
        "INVESTMENT_OBJECTIVE",
        "INDEX_DATA_FOR_BAR_CHART_RATING",
        "INDEX_DATA_FOR_BAR_CHART_MATURITY",
        "INDEX_DATA_FOR_PIE_CHART_CURRENCY",
        "VECTOR_MAP_FOR_INDEX",
        "INDEX_DATA_FOR_PIE_CHART_BICS",
        "INDEX_DATA_FOR_PIE_CHART_FTSE",
        "ASSET_DATA_BAR_CHART_IMMATURITY",
        "INDEX_DATA_FOR_BAR_CHART_MLLYNCHADJUSTEDRATING",
        "FUND_NNA_LISTING_CCY",
        "FUND_NNA_IN_EURO",
        "FUND_AUM_IN_EURO",
        "MAIN_LISTING",
        "EXCHANGE_PLACE",
        "NNA",
        "AUM_IN_EURO",
        "FUND_FUND_NAME",
        "FUND_REFLEX_CODE",
        "FUND_SECURITIES_LENDING",
        "FUND_COLLATERALVALUE",
        "SEC_LENDING_SINCE_INCEPTION",
        "FUND_CURRENT_LOAN",
        "FUND_AVERAGE_LOAN",
        "FUND_MAXIMUM_LOAN",
        "FUND_SEC_LENDING_DATE",
        "COUNTERPARTY_RISK_OF_NAV",
        "FUND_SWAP_COUNTERPART",
        "FUND_SWAP_DATE",
        "FUND_SWAP_DAILYVALUE",
        "FUND_DISPLAY_BREAKDOWN",
        "ASSET_DATA_BAR_CHART_RATING",
        "ASSET_DATA_BAR_CHART_MATURITY",
        "ASSET_DATA_PIECHART_CURRENCY",
        "VECTOR_MAP_DATA_FOR_HOLDING",
        "NBVIEWS",
        "RETURNS",
        "LAST_INAV_VALUE",
        "INAV_CURRENCY",
        "FUND_AUM",
        "SHARE_CLASSIFICATION_LEVARAGE",
        "SHARE_CLASSIFICATION_SHORT",
        "SHOW_PERFORMANCE_GRAPH",
        "PARENT_INDEX_TICKER",
        "OUTPERFORMANCE",
        "RISK_REDUCTION",
        "DRAWDOWN_REDUCTION",
        "INAV_SGX",
        "WKN",
        "IMPLICIT_LEVERAGE",
        "IMPLICIT_LEVERAGE_VALUE",
        "IMPLICIT_LEVERAGE_VALUE_DATE",
        "LAST_LEVERAGE_RESET_DATE",
        "NAV_VALUE_AT_RESET_DATE",
        "FUTURE_VALUE_AT_RESET_DATE",
        "EXCEPTIONAL_EVENT",
        "EXCEPTIONAL_DISCLAIMERS",
        "ARE_FUND_HOLDINGS_DISPLAYED",
        "IS_VERMOGENSSTRATEGIE_PRODUCT",
        "NNA_DATA_DATE",
        "PERFORMANCE_DATA_DATE",
        "MINIMUM_VARIANCE",
        "FUND_AUM_IN_CCY_DISPLAYED",
        "LAST_NAV_AFTER_EFFECTIVE_COTATION_DATE",
        "IS_BENCHMARK_PROVIDER_STOXX",
        "OLD_SHARE_ISIN",
        "IS_MAIN_PER_GET_SHARE_CHARACS_WS",
        "FUND_LEGAL_FORM",
        "SHARE_CLASSIFICATION_4",
        "SHARE_NAME_CHANGE_DATE",
        "HAS_WEB_PAGE",
        "FUND_ESG_QUALITY_RATING",
        "FUND_ESG_QUALITY_SCORE",
        "INDEX_TRACKED",
        "TEMPERATURE",
        "HUB_CATEGORY",
        "HAS_GREENFIN_LABEL",
        "E_SCORE",
        "S_SCORE",
        "G_SCORE",
        "CARBON_INTENSITY_TONS",
        "CARBON_EMISSIONS_FINANCED",
        "WEIGHTED_CARBON_INTENSITY_TONS",
        "LAUNCH_DATE",
        "BENCHMARK_NUMBER_OF_COMPONENTS",
        "CARBON_EMISSIONS_TONS_INVESTED",
        "WEIGHTED_AVERAGE_CARBON_INTENSITY_TONS_SALES",
        "SCOPE_1",
        "SCOPE_2",
        "SCOPE_3",
        "INDEX_REASON_ONE",
        "INDEX_REASON_TWO",
        "INDEX_REASON_THREE",
        "ETF_REASON_ONE",
        "ETF_REASON_TWO",
        "ETF_REASON_THREE",
        "INDEX_INFORMATION_DATE",
        "CARBON_EMISSIONS_TONS",
        "WEIGHTED_AVERAGE_CARBON_INTENSITY_TONS",
        "CARBON_EFFICIENCY",
        "CARBON_INTENSITY_TONS_SALES",
        "LAUNCH_DATE_ORIGIN",
        "HAS_SRI_LABEL",
        "COUNTRIES_WITHOUT_WEBPAGE",
        "ISIN_MERGE_TYPE",
        "FUND_ISR_LABEL",
        "SUB_CATEGORY",
        "ESG_CARBON_DATA_ESG_SCORE",
        "HAS_STATIC_FUND_DISCLAIMER",
        "ESG_CARBON_DATA_DATE",
        "ESG_CARBON_DATA_INDEX",
        "ESG_CARBON_DATA_ESG_RATING",
        "ESG_CARBON_DATA_ENVIRONMENTAL_SCORE",
        "ESG_CARBON_DATA_SOCIAL_SCORE",
        "ESG_CARBON_DATA_GOVERNANCE_SCORE",
        "ESG_CARBON_DATA_ALIGNMENT_DEGREE",
        "ESG_CARBON_DATA_EMISSION_PER_MUSD",
        "ESG_CARBON_DATA_CARBON_INTENSITY",
        "ESG_CARBON_DATA_CARBON_INTENSITY_W_AVG_PCT",
        "ESG_CARBON_DATA_CARBON_CARB_EMISSIONS_SCOPRE_1_PER_MUSD",
        "ESG_CARBON_DATA_CARBON_CARB_EMISSIONS_SCOPRE_2_PER_MUSD",
        "ESG_CARBON_DATA_CARBON_CARB_EMISSIONS_SCOPRE_3_PER_MUSD",
        "REPLICATION_IS_SWAP_BASED",
        "REPLICATION_IS_DIRECT",
        "FUND_DOMICILIATION_COUNTRY",
        "CO_TOOL_FILTER_LEVEL_ONE",
        "CO_TOOL_FILTER_LEVEL_TWO",
        "CO_TOOL_FILTER_LEVEL_THREE",
        "SHOULD_BE_DISPLAYED_IN_CO_TOOL",
        "EASY_BOURSE",
        "BOURSE_DIRECT",
        "SHARE_CLASS_AUM_IN_SHARE_CURRENCY",
        "SHARE_CLASS_AUM_IN_EUR",
        "SHARE_CLASS_AUM_IN_LISTING_CURRENCY",
        "COTOOL_LEVEL_1",
        "COTOOL_LEVEL_2",
        "COTOOL_LEVEL_3",
        "GEOGRAPHY",
        "SUBASSET_CLASS",
        "ESG_SCOPE",
        "IMPACT",
        "SUB",
        "IS_ESG",
        "FUND_SFDR_CLASSIFICATION",
        "HAS_SAVINGS_PLAN",
        "HAS_BROKER_COMMISSIONS",
        "LAST_DATE_FOR_INDEX_PERFORMANCE",
        "LAST_DATE_FOR_COUNTERVALORISED_ADJUSTED_NAV",
        "IS_THEMATIC",
        "ETF_FRENCH_DESCRIPTION",
        "PRODUCT_TAX_DATE",
        "PRODUCT_TAX_CURRENCY",
        "PRODUCT_TAX_MIN_EQUITY_RATIO",
        "PRODUCT_TAX_EQUITY_RATIO_TYPE",
        "MNEMO",
        "MARKET_MAKERS",
        "PASSPORTED_COUNTRIES",
        "MARKET_MAKERS",
        "BENCHMARK_NAME",
        "BENCHMARK_WEBSITE",
        "BENCHMARK_YIELD",
        "BENCHMARK_LAST_INDEX_PRICE",
        "BENCHMARK_LAST_AVERAGE_RATING",
        "BENCHMARK_TICKER",
        "HAS_LISTING_DATA",
        "EXCEPTIONAL_DISCLAIMERS",
        "MERGE_INFO",
        "BENCHMARK_LAST_ANALYTICS_UPDATE_DATE",
        "BENCHMARK_MATURITY",
        "BENCHMARK_CARBON_EFFICIENCY",
        "BENCHMARK_COUPON_RATE",
        "BENCHMARK_DURATION",
        "IS_SHORT_UNDERLYING",
        "BENCHMARK_MODIFIED_DURATION",
        "BENCHMARK_CONVEXITY",
        "BENCHMARK_ESTIMATED_HEDGE_COST",
        "IS_SWAP_DISPLAYED",
        "DISCLAIMER_FOR_SWAP_SECTION",
        "LAST_TRACKED_INDEX_NAME",
        "BENCHMARK_BENCH_START_DATE",
        "GERMAN_TAX_TRANSPARENCY",
        "INSURANCE_CONTRACTS_COUNT",
        "EUSD_STATUS",
        "FUND_PORTFOLIO_MANAGERS",
        "DATE_OF_MERGE",
        "ISA",
        "SIPP",
        "UKFRS",
        "FUND_GERMAN_VL",
        "ASSET_UNDER_MANAGEMENT",
        "BASE_CURRENCY",
        "REPLICATION_METHODOLOGY",
        "INDEX_BREAKDOWNS_AS_OF_DATE",
        "PERFORMANCE_AS_OF_DATE",
        "FUND_FUND_ROLES",
        "TRADING_CURRENCIES",
        "SHARES_OUT",
        "CAPI_OR_DISTRI",
        "SRI",
        "STRESS_SCENARIO",
        "FAVOURABLE_SCENARIO",
        "MODERATE_SCENARIO",
        "UNFAVOURABLE_SCENARIO",
        "RHP",
        "COMPOSITION_OF_COST",
        "HAS_SPECIFIC_UK_PRO_DISCLAIMER",
        "DISTRIBUTION_FREQUENCY",
        "UKFRS"
    ],
    "historics": [
        {
            "indicator": "fundAumInMCcy",
            "startDate": "1000-01-01T00:00:00.000Z",
            "endDate": "2050-01-01T00:00:00.000Z"
        },
        {
            "indicator": "officialNav",
            "startDate": "1000-01-01T00:00:00.000Z",
            "endDate": "2050-01-01T00:00:00.000Z"
        },
        {
            "indicator": "countervalorisedAdjustedNAV",
            "startDate": "1000-01-01T00:00:00.000Z",
            "endDate": "2050-01-01T00:00:00.000Z"
        },
        {
            "indicator": "adjustedBenchPrice",
            "startDate": "1000-01-01T00:00:00.000Z",
            "endDate": "2050-01-01T00:00:00.000Z"
        },
        {
            "indicator": "dividendAmount",
            "startDate": "1000-01-01T00:00:00.000Z",
            "endDate": "2050-01-01T00:00:00.000Z"
        },
        {
            "indicator": "dividendCurrency",
            "startDate": "1000-01-01T00:00:00.000Z",
            "endDate": "2050-01-01T00:00:00.000Z"
        }
    ],
    "metrics": [
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2014"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2015"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2016"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2017"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2018"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2019"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2020"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2021"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2022"
        },
        {
            "indicator": "benchmarkCalendarPerformance",
            "period": "2023"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2014"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2015"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2016"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2017"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2018"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2019"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2020"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2021"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2022"
        },
        {
            "indicator": "parentIndexCalendarPerformance",
            "period": "2023"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2014"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2015"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2016"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2017"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2018"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2019"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2020"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2021"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2022"
        },
        {
            "indicator": "shareCalendarPerformance",
            "period": "2023"
        },
        {
            "indicator": "shareAnnualizedPerformance",
            "period": "ONE_YEAR"
        },
        {
            "indicator": "shareAnnualizedPerformance",
            "period": "THREE_YEARS"
        },
        {
            "indicator": "shareAnnualizedPerformance",
            "period": "FIVE_YEARS"
        },
        {
            "indicator": "shareAnnualizedPerformance",
            "period": "TEN_YEARS"
        },
        {
            "indicator": "benchmarkAnnualizedPerformance",
            "period": "ONE_YEAR"
        },
        {
            "indicator": "benchmarkAnnualizedPerformance",
            "period": "THREE_YEARS"
        },
        {
            "indicator": "benchmarkAnnualizedPerformance",
            "period": "FIVE_YEARS"
        },
        {
            "indicator": "benchmarkAnnualizedPerformance",
            "period": "TEN_YEARS"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "ONE_MONTH"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "ONE_YEAR"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "THREE_YEARS"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "THREE_MONTH"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "THREE_YEARS"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "SIX_MONTH"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "FIVE_YEARS"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "TEN_YEARS"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "YEAR_TO_DATE"
        },
        {
            "indicator": "benchmarkCumulativePerformance",
            "period": "SINCE_CREATION"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "FIVE_YEARS"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "THREE_YEARS"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "YEAR_TO_DATE"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "ONE_YEAR"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "THREE_MONTH"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "SIX_MONTH"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "TEN_YEARS"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "ONE_MONTH"
        },
        {
            "indicator": "parentIndexCumulativePerformance",
            "period": "SINCE_CREATION"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "FIVE_YEARS"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "THREE_YEARS"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "YEAR_TO_DATE"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "ONE_YEAR"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "THREE_MONTH"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "SIX_MONTH"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "TEN_YEARS"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "ONE_MONTH"
        },
        {
            "indicator": "shareCumulativePerformance",
            "period": "SINCE_CREATION"
        },
        {
            "indicator": "benchmarkYeartoyearPerformance",
            "period": "THIRD_YEAR"
        },
        {
            "indicator": "benchmarkYeartoyearPerformance",
            "period": "SECOND_YEAR"
        },
        {
            "indicator": "benchmarkYeartoyearPerformance",
            "period": "FIRST_YEAR"
        },
        {
            "indicator": "benchmarkYeartoyearPerformance",
            "period": "FIFTH_YEAR"
        },
        {
            "indicator": "benchmarkYeartoyearPerformance",
            "period": "FOURTH_YEAR"
        },
        {
            "indicator": "parentIndexReatilPerformance",
            "period": "THIRD_YEAR"
        },
        {
            "indicator": "parentIndexReatilPerformance",
            "period": "SECOND_YEAR"
        },
        {
            "indicator": "parentIndexReatilPerformance",
            "period": "FIRST_YEAR"
        },
        {
            "indicator": "parentIndexReatilPerformance",
            "period": "FIFTH_YEAR"
        },
        {
            "indicator": "parentIndexReatilPerformance",
            "period": "FOURTH_YEAR"
        },
        {
            "indicator": "shareYeartoyearPerformance",
            "period": "THIRD_YEAR"
        },
        {
            "indicator": "shareYeartoyearPerformance",
            "period": "SECOND_YEAR"
        },
        {
            "indicator": "shareYeartoyearPerformance",
            "period": "FIRST_YEAR"
        },
        {
            "indicator": "shareYeartoyearPerformance",
            "period": "FIFTH_YEAR"
        },
        {
            "indicator": "shareYeartoyearPerformance",
            "period": "FOURTH_YEAR"
        }
    ],
    "breakDown": {
        "aggregationFields": [
            "INDEX_TOP10",
            "FUND_TOP10",
            "INDEX_SECTORS",
            "INDEX_MATURITIES",
            "INDEX_RATINGS",
            "INDEX_RAWMATERIALS",
            "INDEX_CURRENCIES",
            "INDEX_COUNTRIES"
        ]
    },
    "productType": "PRODUCT",
    "composition": {
        "compositionFields": [
            "date",
            "type",
            "bbg",
            "isin",
            "name",
            "weight",
            "quantity",
            "currency",
            "sector",
            "country",
            "countryOfRisk"
        ]
    }
}

	return(data)




def get_nasdaq_stocks_headers():

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.nasdaq.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.nasdaq.com/',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    return(headers)
