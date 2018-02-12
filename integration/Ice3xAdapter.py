import base64
import json
import urllib

from integration.BitcoinAdapter import BitcoinAdapter


class Ice3xAdapter(BitcoinAdapter):
    def load_order_book(self, bitcoin_security, order_book):
        order_book.reset_book()
        http_get_url = '{}orderbook/info?pair_id={}' \
            .format(bitcoin_security.exchange_url, bitcoin_security.security_id)
        http_get_request = urllib.request.Request(http_get_url)
        http_get_response = urllib.request.urlopen(http_get_request)
        if http_get_response.code == 200:
            json_data = json.loads(http_get_response.read().decode('utf-8'))
            for bid in json_data['response']['entities']['bids']:
                bid_price = float(bid['price'])
                bid_volume = float(bid['amount'])
                order_book.append_bid(bid_price, bid_volume)
            for ask in json_data['response']['entities']['asks']:
                ask_price = float(ask['price'])
                ask_volume = float(ask['amount'])
                order_book.append_ask(ask_price, ask_volume)
        return order_book

    def create_limit_order(self, bitcoin_security, order_decision):
        http_auth_data = '{}:{}' \
            .format(bitcoin_security.user_id, bitcoin_security.user_secret) \
            .replace('\n', '')
        http_auth_header = "Basic {}".format(base64.encodestring(http_auth_data))
        http_post_data = {'nonce': bitcoin_security.user_secret,
                          'pair_id': bitcoin_security.security_id,
                          'type': order_decision.order_type,
                          'volume': order_decision.order_volume,
                          'price': order_decision.order_price}
        http_post_data = urllib.parse.urlencode(http_post_data)
        http_post_url = '{}order/new'.format(bitcoin_security.exchange_url)
        http_post_request = urllib.request.Request(http_post_url, http_post_data)
        http_post_request.add_header("Authorization", http_auth_header)
        http_post_response = urllib.request.urlopen(http_post_request)
        if http_post_response.code == 200:
            json_data = json.loads(http_post_response.read().decode('utf-8'))
            order_id = json_data['response']['entity']['order_id']
            order_decision.set_id(order_id)
        return order_decision
