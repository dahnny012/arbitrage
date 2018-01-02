import hmac
import hashlib
import urllib.parse
from time import time
import requests
import json

class Client:
    def __init__(self, public, private):
        self.public = public
        self.private = str.encode(private)

    def nonce(self):
        return  int(time() * 1000)

    def sign(self, params):
        return hmac.new(self.private, self.payload(params), hashlib.sha512)
    
    def payload(self, params):
        return urllib.parse.urlencode(params).encode('utf8')

    def execute(self, params):
        headers = {
            'SIGNATURE': self.sign(params).hexdigest(),
            'KEY': self.public
        }
        return requests.post("https://bitgrail.com/api/v1/withdrawshistory", data=params, headers=headers)

    def last_price(self, ticker, date=None):
        api_url = "https://bitgrail.com/api/v1/{0}/ticker".format(ticker)
        r1 = requests.get(api_url)
        return float(r1.json()['response']['last'])

        

    def withdraw_history(self, coin):
        params = {
            'coin': coin,
            'nonce': self.nonce(),
        }
        data =  self.execute(params).json()
        parsed = json.dumps(data, indent=4, sort_keys=True)
        print(parsed)
        return data