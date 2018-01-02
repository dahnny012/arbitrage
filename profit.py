import requests
import bitgrail
import bittrex
import binance
import sys
from gemini import gemini
from multiprocessing import Pool
import time

# clients
public_bitgrail = bitgrail.Client("","")
public_bittrex = bittrex.ClientWrapper(bittrex.Client("", ""))
public_gemini = gemini.ClientWrapper(gemini.Client("",""))
public_binance = binance.Client()

work_map = {
    'binance': {
        'btcusd': [public_binance.last_price, "BTCUSDT"],
        'btceth': [public_binance.last_price, "ETHBTC"],
        'btcltc': [public_binance.last_price, "LTCBTC"],
    },
    'bitgrail': {
        'btcltc': [public_bitgrail.last_price, "BTC-LTC"],
        'btceth': [public_bitgrail.last_price, "BTC-ETH"],
    },
    'gemini':{
        'btcusd': [public_gemini.last_price,"btcusd"],
        'btceth': [public_gemini.last_price,"ethbtc"],
        'ethusd': [public_gemini.last_price,"ethusd"]
    },
    'bittrex':{
        'btcusd': [public_bittrex.last_price,"USDT-BTC"],
        'btcltc': [public_bittrex.last_price,"BTC-LTC"],
    }
}

def transact_with_fee(currency):
    return currency * .998

def convert_currency(currency, rate):
    return currency * transact_with_fee(rate)

def eth_arbitrage(btc):
    eth_withdraw_fee = .05

    print("ETHBTC bitgrail: " + str(work_map['bitgrail']['btceth']))
    print("ETHBTC gemini: " + str(work_map['gemini']['btceth']))
    print("BTCUSD gemini: " + str(work_map['gemini']['btcusd']))
    eth = ((btc) / work_map['bitgrail']['btceth']) 

    # Gemini
    btc_after_arbitrage = convert_currency(eth - eth_withdraw_fee, work_map['gemini']['btceth'])
    usd = convert_currency(btc_after_arbitrage, work_map['gemini']['btcusd'])
    profit = usd - convert_currency(btc, work_map['gemini']['btcusd'])

    print(profit)
    pct = profit/usd
    print(str(round(pct * 100,2)) + "%")

    print("-------------Checking Binance----------")
    btc_after_arbitrage = convert_currency(eth - eth_withdraw_fee, work_map['binance']['btceth'])
    usd = convert_currency(btc_after_arbitrage,  work_map['binance']['btcusd'])
    profit = usd - convert_currency(btc, work_map['binance']['btcusd'])
    print(profit)
    print(str(round(profit/usd * 100,2)) + "%")
    print("====================")
    return pct

def ltc_arbitrage(btc):
    ltc_withdraw_fee = .02
    btc_transfer_fee = .001  
    print("LTCBTC bitgrail: " + str(work_map['bitgrail']['btcltc']))
    print("LTCBTC bittrex: " + str(work_map['bittrex']['btcltc']))
    print("BTCUSDT bittrex: " + str(work_map['bittrex']['btcusd']))
    print("BTCUSD Gemini: " + str(work_map['gemini']['btcusd']))
    eth = ((btc) / work_map['bitgrail']['btcltc']) 

    btc_after_arbitrage = convert_currency(eth - ltc_withdraw_fee, work_map['bittrex']['btcltc'])

    # Cashout on bittrex
    print("---------------------------")
    print("Cashing BTC to USDT on Bittrex")
    usd = convert_currency(btc_after_arbitrage, work_map['bittrex']['btcusd'])
    profit = usd - convert_currency(btc, work_map['bittrex']['btcusd'])

    print(profit)
    pct = profit/usd
    print(str(round(pct * 100,2)) + "%")


    # Cashout on Binance
    print("---------------------------")
    print("Cashing BTC to USDT on Binance")
    btc_after_arbitrage = convert_currency(eth - ltc_withdraw_fee, work_map['binance']['btcltc'])
    usd = convert_currency(btc_after_arbitrage, work_map['binance']['btcusd'])
    profit = usd - convert_currency(btc, work_map['binance']['btcusd'])

    print(profit)
    pct = profit/usd
    print(str(round(pct * 100,2)) + "%")
    print("====================")
    return pct

class ProfitCalulator():
    def __init__(self, btc):
        self.rates =  {
            "eth": eth_arbitrage(btc),
            "ltc": ltc_arbitrage(btc)
        }
    
    def arbitrage_available(self, desired_rate):
        filtered = {}
        for key in self.rates:
            if(self.rates[key] >= desired_rate):
                filtered[key] = self.rates[key]
        if len(filtered.keys()) > 0:
            return self.find_max_rate(filtered) # probably not optimized but its like 2 tickers lol
        return filtered

    def find_max_rate(self, arbitrage_map):
        """ a) create a list of the dict's keys and values; 
            b) return the key with the max value"""  
        v=list(arbitrage_map.values())
        k=list(arbitrage_map.keys())
        max_key =  k[v.index(max(v))]
        max_value = str(round(arbitrage_map[max_key] * 100, 2)) + "%"
        print("Recommended Currency: {0}, at rate {1}".format(max_key, max_value))
        new_arbitrage_map = {}
        new_arbitrage_map[max_key] = max_value
        return new_arbitrage_map

def process_work(keys):
    work = work_map[keys[0]][keys[1]]
    fn = work[0]
    param = work[1]
    data = fn(param)
    return data



if __name__ == '__main__':
    if 'profit' not in sys.modules:
        if len(sys.argv) <= 1:
            print("How much BTC to arbitrage")
            btc = float(input())
            start = time.time()
            p = Pool(8) # my cpu has 4 cores 8 threads.
            work = []
            for exchange in work_map:
                for ticker in work_map[exchange]:
                    work.append([exchange, ticker])
            done_work = p.map(process_work, work)
            for exchange in work_map:
                for ticker in work_map[exchange]:
                    work_map[exchange][ticker] = done_work.pop(0)
            print("====================")
            eth_arbitrage(btc)
            ltc_arbitrage(btc)
            
        else: 
            btc = float(sys.argv[1])

