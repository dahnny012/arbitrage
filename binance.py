import requests

class Client:
    def last_price(self, ticker):
        api_url = "https://api.binance.com/api/v3/ticker/price?symbol="+ticker
        return float(requests.get(api_url).json()["price"])