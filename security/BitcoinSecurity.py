from orderbook.OrderBook import OrderBook
from orderbook.OrderDecision import OrderDecision


class BitcoinSecurity:
    def __init__(self, exchange_id, exchange_url, security_id, user_id, user_secret):
        self.exchange_id = exchange_id
        self.exchange_url = exchange_url
        self.security_id = security_id
        self.user_id = user_id
        self.user_secret = user_secret
        self.order_book = OrderBook(self)
        self.order_decision = OrderDecision(self)

    def __str__(self):
        return "'exchange_id':'{}', 'exchange_url':'{}', 'security_id':'{}', 'user_id':'{}', 'user_secret':'{}'" \
            .format(self.exchange_id, self.exchange_url, self.security_id, self.user_id, self.user_secret)

    def execute_order_book(self):
        pass

    def execute_order_decision(self):
        pass

    def set_order_decision(self, order_type, order_volume, order_price):
        self.order_decision.set_order_type(order_type)
        self.order_decision.set_order_volume(order_volume)
        self.order_decision.set_order_price(order_price)
