import requests
import bitgrail
import bittrex
import sys
from gemini import gemini


print("How much BTC to arbitrage")
if len(sys.argv) <= 0:
    btc = float(input())
else: 
    btc = sys.argv[1]

# clients
public_bitgrail = bitgrail.Client("","")
public_bittrex = bittrex.ClientWrapper(bittrex.Client("", ""))
public_gemini = gemini.ClientWrapper(gemini.Client("",""))

# bitgrail
ltcbtc_bitgrail = public_bitgrail.last_price("BTC-LTC")
ethbtc_bitgrail = public_bitgrail.last_price("BTC-ETH")

# gemini 
ethbtc_gemini = public_gemini.last_price("ethbtc")
btcusd_gemini = public_gemini.last_price("btcusd")

# bittrex
btcusdt_bittrex = public_bittrex.last_price("USDT-BTC")
ltcbtc_bittrex = public_bittrex.last_price("BTC-LTC")

def transact_with_fee(currency):
    return currency * .998

def convert_currency(currency, rate):
    return currency * transact_with_fee(rate)

def eth_arbitrage(btc):
    eth_withdraw_fee = .05

    print("ETHBTC bitgrail: " + str(ethbtc_bitgrail))
    print("ETHBTC gemini: " + str(ethbtc_gemini))
    print("BTCUSD gemini: " + str(btcusd_gemini))
    eth = ((btc) / ethbtc_bitgrail) 

    btc_after_arbitrage = convert_currency(eth - eth_withdraw_fee, ethbtc_gemini)
    usd = convert_currency(btc_after_arbitrage, btcusd_gemini)
    profit = usd - convert_currency(btc, btcusd_gemini)

    print(profit)
    pct = profit/usd
    print(str(round(pct * 100,2)) + "%")

def ltc_arbitrage(btc):
    ltc_withdraw_fee = .02
    btc_transfer_fee = .001  
    print("LTCBTC bitgrail: " + str(ltcbtc_bitgrail))
    print("LTCBTC bittrex: " + str(ltcbtc_bittrex))
    print("BTCUSDT bittrex: " + str(btcusdt_bittrex))
    print("BTCUSD Gemini: " + str(btcusd_gemini))
    eth = ((btc) / ltcbtc_bitgrail) 

    btc_after_arbitrage = convert_currency(eth - ltc_withdraw_fee, ltcbtc_bittrex)

    # Cashout on bittrex
    print("---------------------------")
    print("Cashing BTC to USDT on Bittrex")
    usd = convert_currency(btc_after_arbitrage, btcusdt_bittrex)
    profit = usd - convert_currency(btc, btcusdt_bittrex)

    print(profit)
    pct = profit/usd
    print(str(round(pct * 100,2)) + "%")
    print("-----------------")
    print("OR Send To Gemini")
    usd = convert_currency(btc_after_arbitrage - btc_transfer_fee, btcusd_gemini)
    profit = usd - convert_currency(btc, btcusd_gemini)

    print(profit)
    pct = profit/usd
    print(str(round(pct * 100,2)) + "%")

print("====================")
eth_arbitrage(btc)
print("===================")
ltc_arbitrage(btc)