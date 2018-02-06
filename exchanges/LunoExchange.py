from exchanges.BitcoinExchange import BitcoinExchange

import base64
import json
import urllib


class LunoExchange(BitcoinExchange):
    def __init__(self, exchange_id, exchange_url, security_id, user_id, user_secret):
        super().__init__(exchange_id, exchange_url, security_id, user_id, user_secret)

    def load_order_book(self):
        bids = {}
        asks = {}
        http_get_url = '{}orderbook?pair={}' \
            .format(self.exchange_url, self.security_id)
        http_get_request = urllib.request.Request(http_get_url)
        http_get_response = urllib.request.urlopen(http_get_request)
        if http_get_response.code == 200:
            json_data = json.loads(http_get_response.read().decode('utf-8'))
            for bid in json_data['bids']:
                bid_price = float(bid['price'])
                bid_volume = float(bid['volume'])
                if bid_price not in bids:
                    bids[bid_price] = bid_volume
                else:
                    bids[bid_price] = bids[bid_price] + bid_volume
            for ask in json_data['asks']:
                ask_price = float(ask['price'])
                ask_volume = float(ask['volume'])
                if ask_price not in asks:
                    asks[ask_price] = ask_volume
                else:
                    asks[ask_price] = asks[ask_price] + ask_volume
        self.order_book.set_bids(bids)
        self.order_book.set_asks(asks)

    def create_limit_order(self, type, volume, price):
        http_auth_data = '{}:{}' \
            .format(self.user_id, self.user_secret).replace('\n', '')
        http_auth_header = "Basic {}".format(base64.encodestring(http_auth_data))
        http_post_data = {'pair': self.security_id, 'type': type,
                          'volume': volume, 'price': price}
        http_post_data = urllib.parse.urlencode(http_post_data)
        http_post_url = '{}postorder'.format(self.exchange_url)
        http_post_request = urllib.request.Request(http_post_url, http_post_data)
        http_post_request.add_header("Authorization", http_auth_header)
        http_post_response = urllib.request.urlopen(http_post_request)
        if http_post_response.code == 200:
            json_data = json.loads(http_post_response.read().decode('utf-8'))
            order_id = json_data['order_id']
            self.switch_order.set_id(order_id)
