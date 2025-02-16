


def scan_Stocks_Nasdaq_SE():

    num = 500
    outputNum = 500
    offset=0
    headers = get_nasdaq_stocks_headers()
    df = None
    done = False
    while(num == outputNum):
        params = {
            'tableonly': 'false',
            'limit': str(num),
            'offset': str(offset),
        }
        url = 'https://api.nasdaq.com/api/screener/stocks?'+urllib.parse.urlencode(params)


        data = json.dumps(params)
        data = str(data)
        data = data.encode('utf-8')

        req = urllib.request.Request(
                url,
                headers=headers
        )
        response = urllib.request.urlopen(req)

        data = json.loads(response.read().decode('utf-8'))
        if(not done):
            done = True
            df = pd.DataFrame(columns = list(data['data']['table']['rows'][0].keys()))


        rows = data['data']['table']['rows']
        outputNum = len(rows)
        offset += outputNum
        print('->',offset)

        for d in rows:
            df.loc[len(df)] = d
