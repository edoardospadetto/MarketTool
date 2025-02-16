import requests

def get_headers_tradegate():
    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    return(headers)


def get_price_tradegate(isin):
    url = "https://www.tradegate.de/orderbuch.php?lang=en&isin="+isin
    headers = get_headers_tradegate()
    response = requests.get(url, headers=headers)
    return(response.content)

def search_tradegate(query):
    headers = get_headers_tradegate()

    params = {
        'suche': query,
        'lang': 'en',
    }

    response = requests.get('https://www.tradegate.de/kurssuche.php', params=params, headers=headers)
    #print(response.content
    return(response.content)
