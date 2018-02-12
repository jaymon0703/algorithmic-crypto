class OrderDecision:
    def __init__(self, bitcoin_security):
        self.bitcoin_security = bitcoin_security
        self.order_type = ''
        self.order_volume = 0.0
        self.order_price = 0.0
        self.order_id = 0

    def __str__(self):
        return "'exchange_id':'{}', 'security_id':'{}', 'order_type':'{}', " \
               "'order_volume':'{}', 'order_price':'{}', 'order_id':'{}'" \
            .format(self.bitcoin_security.exchange_id, self.bitcoin_security.security_id,
                    self.order_type, self.order_volume, self.order_price, self.order_id)

    def reset_order_decision(self):
        self.order_type = ''
        self.order_volume = 0.0
        self.order_price = 0.0
        self.order_id = 0

    def set_order_id(self, order_id):
        self.order_id = order_id

    def set_order_type(self, order_type):
        self.order_type = order_type

    def set_order_volume(self, order_volume):
        self.order_volume = order_volume

    def set_order_price(self, order_price):
        self.order_price = order_price
