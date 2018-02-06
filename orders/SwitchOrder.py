class SwitchOrder:
    def __init__(self, exchange):
        self.exchange = exchange
        self.type = ''
        self.volume = 0.0
        self.price = 0.0
        self.id = 0

    def __str__(self):
        return "'exchange_id':'{}', 'security_id':'{}', 'type':'{}', 'volume':'{}', 'price':'{}', 'id':'{}'" \
            .format(self.exchange_id, self.security_id, self.type, self.volume, self.price, self.id)

    def set_order(self, type, volume, price):
        self.type = type
        self.volume = volume
        self.price = price

    def set_id(self, id):
        self.id = id
