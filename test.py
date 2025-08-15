from binance.client import Client

API_KEY = 'SZ0wxoe0ye8LojIwS6X3zIsUYWBD1g3JON7zkSWTUKqjwFFQomPK099nmyLP7AV5'
API_SECRET = 'G0bU4Mpbdgnp7QiI630b3aABz7e7TOxLq9aCO0iQRMFHjiZNmwKezZygo7w3L8eS'

client = Client(API_KEY, API_SECRET)

symbolTicker = 'ATOMBTC'

infoCurrency = client.get_symbol_info(symbolTicker)

print(infoCurrency)

minQuantity = float(infoCurrency['filters'][1]['minQty'])
minPrice = infoCurrency['filters'][0]['minPrice']

print(minQuantity)
print(minPrice)
