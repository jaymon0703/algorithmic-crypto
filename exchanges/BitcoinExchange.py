from orders.OrderBook import OrderBook
from orders.SwitchOrder import SwitchOrder


class BitcoinExchange:
    def __init__(self, exchange_id, exchange_url, security_id, user_id, user_secret):
        self.exchange_id = exchange_id
        self.exchange_url = exchange_url
        self.security_id = security_id
        self.user_id = user_id
        self.user_secret = user_secret
        self.order_book = OrderBook(self)
        self.switch_order = SwitchOrder(self)

    def __str__(self):
        return "'exchange_id':'{}', 'exchange_url':'{}', 'security_id':'{}', 'user_id':'{}', 'user_secret':'{}'" \
            .format(self.exchange_id, self.exchange_url, self.security_id, self.user_id, self.user_secret)

    def load_order_book(self):
        pass

    def create_limit_order(self, type, volume, price):
        pass

    def create_buy_order(self, volume, price):
        self.create_limit_order("BID", volume, price)
        self.switch_order.set_order_details("BID", volume, price)

    def create_sell_order(self, volume, price):
        self.create_limit_order("ASK", volume, price)
        self.switch_order.set_order("ASK", volume, price)
