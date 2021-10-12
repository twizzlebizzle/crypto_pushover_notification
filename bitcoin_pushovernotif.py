import json
import urllib.request
import requests


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

btc_address = [BITCOIN ADDRESS HERE]
eth_address = [ETH ADDRESS HERE]

def retrieve_BTC_balance(address):
 url = "https://blockchain.info/rawaddr/"+address
 r = requests.get(url)
 cont = json.loads(r.content.decode('utf-8'))
 amount = (cont["final_balance"])/100000000
 return amount

def retrieve_ETH_balance(address):
 url = "https://api.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey=YourApiKeyToken"
 r = requests.get(url)
 cont = json.loads(r.content.decode('utf-8'))
 amount = (cont["result"])
 amount2 = int(amount)/1000000000000000000
 return amount2

def retrieveBTCETHprice(currency):
 url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH'
 parameters = {
   'convert':'GBP'
 }
 headers = {
   'Accepts': 'application/json',
   'X-CMC_PRO_API_KEY': [API KEY],
 }

 session = Session()
 session.headers.update(headers)

 response = session.get(url, params=parameters)
 data = json.loads(response.text)

 format1 = data["data"]
 format2 = format1[currency]
 format3 = format2["quote"]
 format4 = format3["GBP"]
 format5 = format4["price"]

 return format5

currentbtcvalue = int(retrieveBTCETHprice("BTC")*retrieve_BTC_balance(btc_address))
currentethvalue = int(retrieveBTCETHprice("ETH")*retrieve_ETH_balance(eth_address))
currentbtcprice = int(retrieveBTCETHprice("BTC"))
totalvalue = currentbtcvalue+currentethvalue


outputstring = "Bitcoin Price: £{0}  -  Crypto Value: £{1}".format(currentbtcprice, totalvalue)

import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": [TOKEN HERE],
    "user": [TOKEN HERE],
    "message": outputstring,
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
