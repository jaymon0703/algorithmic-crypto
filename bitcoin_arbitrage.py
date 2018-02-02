import base64
import datetime
import json
import threading
import urllib.parse
import urllib.request

class bitcoin_security:
    def __init__(self, exchange_id, exchange_url, security_id, username, password):
        self.exchange_id = exchange_id
        self.exchange_url = exchange_url
        self.security_id = security_id
        self.username = username
        self.password = password
        self.bids = {}
        self.asks = {}
        self.order_id = 0
        self.transaction_id = 0

    def __str__(self):
        return "'exchange_id':'{}', 'security_id':'{}', 'bids':'{}', 'asks':'{}'".format(self.exchange_id, self.security_id, self.bids, self.asks)

    def load_order_book(self):
        pass

    def post_limit_order(self):
        pass

class bitcoin_luno(bitcoin_security):
    def load_order_book(self):
        self.bids = {}
        self.asks = {}
        http_get_url = '{}orderbook?pair={}'.format(self.exchange_url, self.security_id)
        http_get_request = urllib.request.Request(http_get_url)
        http_get_response = urllib.request.urlopen(http_get_request).read().decode('utf-8')
        json_data = json.loads(http_get_response)
        for bid in json_data['bids']:
            bid_price = float(bid['price'])
            bid_volume = float(bid['volume'])
            if bid_price not in self.bids:
                self.bids[bid_price] = bid_volume
            else:
                self.bids[bid_price] = self.bids[bid_price] + bid_volume
        for ask in json_data['asks']:
            ask_price = float(ask['price'])
            ask_volume = float(ask['volume'])
            if ask_price not in self.asks:
                self.asks[ask_price] = ask_volume
            else:
                self.asks[ask_price] = self.asks[ask_price] + ask_volume

    def post_limit_order(self, type, volume, price):
        http_auth_data = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        http_post_data = {'pair' : self.security_id, 'type' : type, 'volume' : volume, 'price' : price}
        http_post_data = urllib.parse.urlencode(http_post_data)
        http_post_url = '{}postorder'.format(self.exchange_url)
        http_post_request = urllib.request.Request(http_post_url, http_post_data)
        http_post_request.add_header("Authorization", "Basic %s" % http_auth_data)
        http_post_response = urllib.request.urlopen(http_post_request).read().decode('utf-8')
        json_data = json.loads(http_post_response)
        self.order_id = json_data['order_id']

class bitcoin_ice_cube(bitcoin_security):
    def load_order_book(self):
        self.bids = {}
        self.asks = {}
        http_get_url = '{}orderbook/info?pair_id={}'.format(self.exchange_url, self.security_id)
        http_get_request = urllib.request.Request(http_get_url)
        http_get_response = urllib.request.urlopen(http_get_request).read().decode('utf-8')
        json_data = json.loads(http_get_response)
        for bid in json_data['response']['entities']['bids']:
            bid_price = float(bid['price'])
            bid_volume = float(bid['amount'])
            if bid_price not in self.bids:
                self.bids[bid_price] = bid_volume
            else:
                self.bids[bid_price] = self.bids[bid_price] + bid_volume
        for ask in json_data['response']['entities']['asks']:
            ask_price = float(ask['price'])
            ask_volume = float(ask['amount'])
            if ask_price not in self.asks:
                self.asks[ask_price] = ask_volume
            else:
                self.asks[ask_price] = self.asks[ask_price] + ask_volume

    def post_limit_order(self, type, volume, price):
        http_auth_data = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        http_post_data = {'nonce' : self.password, 'pair_id' : self.security_id, 'type' : type, 'volume' : volume, 'price' : price}
        http_post_data = urllib.parse.urlencode(http_post_data)
        http_post_url = '{}order /new'.format(self.exchange_url)
        http_post_request = urllib.request.Request(http_post_url, http_post_data)
        http_post_request.add_header("Authorization", "Basic %s" % http_auth_data)
        http_post_response = urllib.request.urlopen(http_post_request).read().decode('utf-8')
        json_data = json.loads(http_post_response)
        self.order_id = json_data['response']['entity']['order_id']
        self.transaction_id = json_data['response']['entity']['transaction_id']

class bitcoin_pair:
    def __init__(self, bitcoin_security_1, bitcoin_security_2):
        self.bitcoin_security_1 = bitcoin_security_1
        self.bitcoin_security_2 = bitcoin_security_2
        self.last_price_difference = 0.0
        self.last_minimum_volume = 0.0

    def check_arbitrage(self):
        bitcoin_security_1_bids = list(self.bitcoin_security_1.bids.items())
        bitcoin_security_2_asks = list(self.bitcoin_security_2.asks.items())
        bitcoin_security_1_bid_price = bitcoin_security_1_bids[0][0]
        bitcoin_security_1_bid_volume = bitcoin_security_1_bids[0][1]
        bitcoin_security_2_ask_price = bitcoin_security_2_asks[0][0]
        bitcoin_security_2_ask_volume = bitcoin_security_2_asks[0][1]
        price_difference = bitcoin_security_1_bid_price - bitcoin_security_2_ask_price
        percentage_difference = price_difference / bitcoin_security_1_bid_price * 100
        minimum_volume = min(bitcoin_security_1_bid_volume, bitcoin_security_2_ask_volume)
        if percentage_difference > 0.0 and minimum_volume > 0.0\
        and (price_difference != self.last_price_difference or minimum_volume != self.last_minimum_volume):
            with open('bitcoin_arbitrage.txt', 'a') as file:
                file.write('--------------------------------------------------------------------\n')
                file.write("'timestamp':'{}'\n".format(datetime.datetime.now().isoformat()))
                file.write("'percentage_difference':'{}', 'minimum_volume':'{}'\n".format(percentage_difference, minimum_volume))
                file.write("{}->bid='{}@{}'\n".format(self.bitcoin_security_1.exchange_id, bitcoin_security_1_bid_volume, bitcoin_security_1_bid_price))
                file.write("{}->ask='{}@{}'\n".format(self.bitcoin_security_2.exchange_id, bitcoin_security_2_ask_volume, bitcoin_security_2_ask_price))
                file.write("{}->sell('{}@{}')\n".format(self.bitcoin_security_1.exchange_id, minimum_volume, bitcoin_security_1_bid_price))
                file.write("{}->buy('{}@{}')\n".format(self.bitcoin_security_2.exchange_id, minimum_volume, bitcoin_security_2_ask_price))
                file.write('--------------------------------------------------------------------\n')
                self.last_price_difference = price_difference
                self.last_minimum_volume = minimum_volume

with open('bitcoin_arbitrage.txt', 'w') as file:
    file.flush()

bitcoin_security_1 = bitcoin_luno('Luno', 'https://api.mybitx.com/api/1/', 'XBTZAR', 'username', 'password')
bitcoin_security_2 = bitcoin_ice_cube('IceCube', 'https://ice3x.com/api/v1/', '3', 'username', 'password')

bitcoin_pair_1 = bitcoin_pair(bitcoin_security_1, bitcoin_security_2)
bitcoin_pair_2 = bitcoin_pair(bitcoin_security_2, bitcoin_security_1)

def bit_coin_arbitrage():
    bit_coin_arbitrage_internal()
    threading.Timer(10, bit_coin_arbitrage).start()

def bit_coin_arbitrage_internal():
    global bitcoin_security_1
    global bitcoin_security_2
    global bitcoin_pair_1
    global bitcoin_pair_2

    try:
        bitcoin_security_1.load_order_book()
        bitcoin_security_2.load_order_book()
        bitcoin_pair_1.check_arbitrage()
        bitcoin_pair_2.check_arbitrage()
    except:
        raise

bit_coin_arbitrage()
