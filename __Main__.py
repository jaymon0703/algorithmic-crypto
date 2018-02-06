from execution.BitcoinArbitrage import BitcoinArbitrage
from exchanges.IceCubedExchange import IceCubedExchange
from exchanges.LunoExchange import LunoExchange

import threading

with open('__Log__.log', 'w') as file:
    file.flush()

luno_exchange = LunoExchange('Luno', 'https://api.mybitx.com/api/1/', 'XBTZAR', 'keyId', 'keySecret')
ice_cubed_exchange = IceCubedExchange('IceCubed', 'https://ice3x.com/api/v1/', '3', 'keyId', 'keySecret')

buy_luno_sell_ice_cubed_pair = BitcoinArbitrage(luno_exchange, ice_cubed_exchange)
buy_ice_cubed_sell_luno_pair = BitcoinArbitrage(ice_cubed_exchange, luno_exchange)


def bitcoin_arbitrage():
    bitcoin_arbitrage_thread()
    threading.Timer(10, bitcoin_arbitrage).start()


def bitcoin_arbitrage_thread():
    global luno_exchange
    global ice_cubed_exchange
    global buy_luno_sell_ice_cubed_pair
    global buy_ice_cubed_sell_luno_pair

    try:
        luno_exchange.load_order_book()
        ice_cubed_exchange.load_order_book()
        buy_luno_sell_ice_cubed_pair.calculate_switch_order()
        buy_ice_cubed_sell_luno_pair.calculate_switch_order()
    except:
        raise


bitcoin_arbitrage()
