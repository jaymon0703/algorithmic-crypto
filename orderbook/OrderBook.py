import json


class OrderBook:
    def __init__(self, bitcoin_security):
        self.bitcoin_security = bitcoin_security
        self.bids = {}
        self.asks = {}

    def __str__(self):
        return json.dumps(self)

    def reset(self):
        self.bids = {}
        self.asks = {}

    def append_bid(self, bid_price, bid_volume):
        if bid_price not in self.bids:
            self.bids[bid_price] = bid_volume
        else:
            self.bids[bid_price] = self.bids[bid_price] + bid_volume

    def append_ask(self, ask_price, ask_volume):
        if ask_price not in self.asks:
            self.asks[ask_price] = ask_volume
        else:
            self.asks[ask_price] = self.asks[ask_price] + ask_volume
