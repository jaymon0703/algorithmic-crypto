import threading


from BitcoinArbitrage import BitcoinArbitrage
from IceCubedExchange import IceCubedExchange
from LunoExchange import LunoExchange


with open('__Log__.txt', 'w') as file:
    file.flush()


lunoExchange = LunoExchange('Luno', 'https://api.mybitx.com/api/1/', 'XBTZAR', 'keyId', 'keySecret')
iceCubedExchange = IceCubedExchange('IceCube', 'https://ice3x.com/api/v1/', '3', 'keyId', 'keySecret')

buyLunoSellIceCubedPair = BitcoinArbitrage(lunoExchange, iceCubedExchange)
buyIceCubedSellLunoPair = BitcoinArbitrage(iceCubedExchange, lunoExchange)


def bitcoinArbitrage():
    bitcoinArbitrageThread()
    threading.Timer(10, bitcoinArbitrage).start()


def bitcoinArbitrageThread():
    global lunoExchange
    global iceCubedExchange
    global buyLunoSellIceCubedPair
    global buyIceCubedSellLunoPair

    try:
        lunoExchange.getOrderBook()
        iceCubedExchange.getOrderBook()
        buyLunoSellIceCubedPair.executeArbitrage()
        buyIceCubedSellLunoPair.executeArbitrage()
    except:
        raise


bitcoinArbitrage()

