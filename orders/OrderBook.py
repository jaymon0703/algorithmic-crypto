class OrderBook:
    def __init__(self, exchange):
        self.exchange = exchange
        self.bids = {}
        self.asks = {}

    def __str__(self):
        return "'exchange_id':'{}', 'security_id':'{}', 'bids':'{}', 'asks':'{}'" \
            .format(self.exchange_id, self.security_id, self.bids, self.asks)

    def set_bids(self, bids):
        self.bids = bids

    def set_asks(self, asks):
        self.asks = asks
