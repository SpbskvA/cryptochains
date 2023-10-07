import json
import requests
import numpy as np
import pandas as pd

headers = {
    'authority': 'p2p.binance.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'bnc-uuid': 'c950fa58-cbcc-4ab9-b440-4fb2e7122fe6',
    'c2ctype': 'c2c_merchant',
    'clienttype': 'web',
    'csrftoken': '',
    'device-info': '',
    'fvideo-id': '33ebcfe5d8a7a8ccbe33c755a9daf613516d4b8b',
    'lang': 'ru',
    'origin': 'https://p2p.binance.com',
    'referer': 'https://p2p.binance.com/ru/trade/RosBank/USDT?fiat=RUB',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'x-trace-id': '',
    'x-ui-request-trace': '',
}

json_data = {
    'page': 1,
    'rows': 10,
    'countries': [],
    'publisherType': None,
    'asset': 'USDT',
    'fiat': 'RUB',
    'tradeType': 'BUY',
}

response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=json_data)
json_file = json.dumps(response.json(), indent=4, ensure_ascii=False)

data = json.loads(json_file)
for i in data['data']:
    print(i['adv'])