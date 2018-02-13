import datetime


class BitcoinArbitrage:
    def __init__(self, buy_security, sell_security):
        self.buy_security = buy_security
        self.sell_security = sell_security
        self.last_price_difference = 0.0
        self.last_switchable_volume = 0.0

    def calculate_switch_order(self):
        buy_security_asks = list(self.buy_security.order_book.asks.items())
        sell_security_bids = list(self.sell_security.order_book.bids.items())
        buy_security_ask_price = buy_security_asks[0][0]
        buy_security_ask_volume = buy_security_asks[0][1]
        sell_security_bid_price = sell_security_bids[0][0]
        sell_security_bid_volume = sell_security_bids[0][1]
        price_difference = sell_security_bid_price - buy_security_ask_price
        percentage_difference = price_difference / sell_security_bid_price * 100
        switchable_volume = min(buy_security_ask_volume, sell_security_bid_volume)
        if (percentage_difference > 0.0 and switchable_volume > 0.0) and \
                (price_difference != self.last_price_difference or
                 switchable_volume != self.last_switchable_volume):
            with open('__Log__.log', 'a') as file:
                self.last_price_difference = price_difference
                self.last_switchable_volume = switchable_volume
                file.write('--------------------------------------------------------------------\n')
                file.write("'timestamp':'{}'\n".format(datetime.datetime.now().isoformat()))
                file.write("'percentage_difference':'{}', 'switchable_volume':'{}'\n"
                           .format(percentage_difference, switchable_volume))
                file.write("{}->ask='{}@{}'\n"
                           .format(self.buy_security.exchange_id, buy_security_ask_volume, buy_security_ask_price))
                file.write("{}->bid='{}@{}'\n"
                           .format(self.sell_security.exchange_id, sell_security_bid_volume, sell_security_bid_price))
                file.write("{}->buy('{}@{}')\n"
                           .format(self.buy_security.exchange_id, switchable_volume, buy_security_ask_price))
                file.write("{}->sell('{}@{}')\n"
                           .format(self.sell_security.exchange_id, switchable_volume, sell_security_bid_price))
                file.write('--------------------------------------------------------------------\n')
                self.buy_security.set_order_decision("BID", switchable_volume, buy_security_ask_price)
                self.sell_security.set_order_decision("ASK", switchable_volume, sell_security_bid_price)

    def execute_switch_order(self):
        # self.buy_security.execute_order_decision()
        # self.sell_security.execute_order_decision()
        pass
