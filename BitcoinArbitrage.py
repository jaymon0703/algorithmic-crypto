import datetime


class BitcoinArbitrage:
    def __init__(self, buySecurity, sellSecurity):
        self.buySecurity = buySecurity
        self.sellSecurity = sellSecurity
        self.lastPriceDifference = 0.0
        self.lastSwitchableVolume = 0.0


    def executeArbitrage(self):
        buySecurityAsks = list(self.buySecurity.asks.items())
        sellSecurityBids = list(self.sellSecurity.bids.items())
        buySecurityAskPrice = buySecurityAsks[0][0]
        buySecurityAskVolume = buySecurityAsks[0][1]
        sellSecurityBidPrice = sellSecurityBids[0][0]
        sellSecurityBidVolume = sellSecurityBids[0][1]
        priceDifference = sellSecurityBidPrice - buySecurityAskPrice
        percentageDifference = priceDifference / sellSecurityBidPrice * 100
        switchableVolume = min(buySecurityAskVolume, sellSecurityBidVolume)
        if (percentageDifference > 0.0 and switchableVolume > 0.0) and \
                (priceDifference != self.lastPriceDifference or
                 switchableVolume != self.lastSwitchableVolume):
            with open('__Log__.txt', 'a') as file:
                file.write('--------------------------------------------------------------------\n')
                file.write("'timestamp':'{}'\n".format(datetime.datetime.now().isoformat()))
                file.write("'percentageDifference':'{}', 'switchableVolume':'{}'\n".format(percentageDifference, switchableVolume))
                file.write("{}->ask='{}@{}'\n".format(self.buySecurity.exchangeId, buySecurityAskVolume, buySecurityAskPrice))
                file.write("{}->bid='{}@{}'\n".format(self.sellSecurity.exchangeId, sellSecurityBidVolume, sellSecurityBidPrice))
                file.write("{}->buy('{}@{}')\n".format(self.buySecurity.exchangeId, switchableVolume, buySecurityAskPrice))
                file.write("{}->sell('{}@{}')\n".format(self.sellSecurity.exchangeId, switchableVolume, sellSecurityBidPrice))
                file.write('--------------------------------------------------------------------\n')
                self.lastPriceDifference = priceDifference
                self.lastSwitchableVolume = switchableVolume

