import base64
import json
import urllib.parse
import urllib.request


from BitcoinExchange import BitcoinExchange


class LunoExchange(BitcoinExchange):
    def __init__(self, exchangeId, exchangeUrl, securityId, userId, userSecret):
        super().__init__(exchangeId, exchangeUrl, securityId, userId, userSecret)
        self.bids = {}
        self.asks = {}
        self.orderId = 0
        self.transactionId = 0


    def getOrderBook(self):
        self.bids = {}
        self.asks = {}
        httpGetUrl = '{}orderbook?pair={}'.format(self.exchangeUrl, self.securityId)
        httpGetRequest = urllib.request.Request(httpGetUrl)
        httpGetResponse = urllib.request.urlopen(httpGetRequest).read().decode('utf-8')
        jsonData = json.loads(httpGetResponse)
        for bid in jsonData['bids']:
            bidPrice = float(bid['price'])
            bidVolume = float(bid['volume'])
            if bidPrice not in self.bids:
                self.bids[bidPrice] = bidVolume
            else:
                self.bids[bidPrice] = self.bids[bidPrice] + bidVolume
        for ask in jsonData['asks']:
            askPrice = float(ask['price'])
            askVolume = float(ask['volume'])
            if askPrice not in self.asks:
                self.asks[askPrice] = askVolume
            else:
                self.asks[askPrice] = self.asks[askPrice] + askVolume


    def createOrder(self, type, volume, price):
        httpAuthData = base64.encodestring('%s:%s'.format(self.userId, self.userSecret)).replace('\n', '')
        httpPostData = {'pair': self.securityId, 'type': type, 'volume': volume, 'price': price}
        httpPostData = urllib.parse.urlencode(httpPostData)
        httpPostUrl = '{}postorder'.format(self.exchangeUrl)
        httpPostRequest = urllib.request.Request(httpPostUrl, httpPostData)
        httpPostRequest.add_header("Authorization", "Basic %s".format(httpAuthData))
        httpPostResponse = urllib.request.urlopen(httpPostRequest).read().decode('utf-8')
        jsonData = json.loads(httpPostResponse)
        self.orderId = jsonData['order_id']
        self.transactionId = jsonData['order_id']

