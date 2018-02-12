import threading

from arbitrage.BitcoinArbitrage import BitcoinArbitrage
from security.Ice3xSecurity import Ice3xSecurity
from security.LunoSecurity import LunoSecurity

with open('__Log__.log', 'w') as file:
    file.flush()

luno_security = LunoSecurity('Luno', 'https://api.mybitx.com/api/1/', 'XBTZAR', 'keyId', 'keySecret')
ice3x_security = Ice3xSecurity('Ice3x', 'https://ice3x.com/api/v1/', '3', 'keyId', 'keySecret')

buy_luno_sell_ice3x_pair = BitcoinArbitrage(luno_security, ice3x_security)
buy_ice3x_sell_luno_pair = BitcoinArbitrage(ice3x_security, luno_security)


def bitcoin_arbitrage():
    bitcoin_arbitrage_thread()
    threading.Timer(10, bitcoin_arbitrage).start()


def bitcoin_arbitrage_thread():
    global luno_security
    global ice3x_security
    global buy_luno_sell_ice3x_pair
    global buy_ice3x_sell_luno_pair

    try:
        luno_security.execute_order_book()
        ice3x_security.execute_order_book()
        buy_luno_sell_ice3x_pair.calculate_switch_order()
        buy_ice3x_sell_luno_pair.calculate_switch_order()
        buy_luno_sell_ice3x_pair.execute_switch_order()
        buy_ice3x_sell_luno_pair.execute_switch_order()
    except:
        raise


bitcoin_arbitrage()
