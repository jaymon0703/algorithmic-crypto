class BitcoinExchange:
    def __init__(self, exchangeId, exchangeUrl, securityId, userId, userSecret):
        self.exchangeId = exchangeId
        self.exchangeUrl = exchangeUrl
        self.securityId = securityId
        self.userId = userId
        self.userSecret = userSecret


    def __str__(self):
        return "'exchangeId':'{}', 'exchangeUrl':'{}', 'securityId':'{}', 'userId':'{}', 'userSecret':'{}'"\
            .format(self.exchangeId, self.exchangeUrl, self.securityId, self.userId, self.userSecret)


    def getOrderBook(self):
        pass


    def createOrder(self, type, volume, price):
        pass

