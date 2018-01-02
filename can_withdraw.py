import bitgrail
from datetime import datetime, timedelta

client = bitgrail.Client("api key","secret key")

# maybe use thread pool I dunno
eth_history = client.withdraw_history("eth")
ltc_history = client.withdraw_history("ltc")

ltcbtc_bitgrail = client.last_price("BTC-LTC")
ethbtc_bitgrail = client.last_price("BTC-ETH")

one_day_ago = (datetime.today() - timedelta(days=1))

total_btc = 0

# I dont know how bitgrail handles this fluctuating prices
for key in eth_history['response']:
    transaction = eth_history['response'][key]
    d = datetime.fromtimestamp(int(transaction["date"])) - timedelta(days=1)
    if d.timestamp() >= round(one_day_ago.timestamp()):
        total_btc += float(transaction['amount']) * ethbtc_bitgrail

for key in ltc_history['response']:
    transaction = ltc_history['response'][key]
    d = datetime.fromtimestamp(int(transaction["date"])) - timedelta(days=1)
    if d.timestamp() >= round(one_day_ago.timestamp()):
        total_btc += float(transaction['amount']) * ltcbtc_bitgrail

print(total_btc)
print("You can withdraw {} ETH".format(0.5/ethbtc_bitgrail))
print("You can withdraw {} LTC".format(0.5/ltcbtc_bitgrail))

test = {
    "response": {
        "1": {
            "amount": "10",
            "date": datetime.today().timestamp(),
            "status": "Completed"
        },
        "2": {
            "amount": "1.19928289",
            "date": "1514622767",
            "status": "Completed"
        }
    },
    "success": 1
}