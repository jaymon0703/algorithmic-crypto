import base64
import json
import urllib.parse
import urllib.request


from BitcoinExchange import BitcoinExchange


class IceCubedExchange(BitcoinExchange):
    def __init__(self, exchangeId, exchangeUrl, securityId, userId, userSecret):
        super().__init__(exchangeId, exchangeUrl, securityId, userId, userSecret)
        self.bids = {}
        self.asks = {}
        self.orderId = 0
        self.transactionId = 0


    def getOrderBook(self):
        self.bids = {}
        self.asks = {}
        httpGetUrl = '{}orderbook/info?pair_id={}'.format(self.exchangeUrl, self.securityId)
        httpGetRequest = urllib.request.Request(httpGetUrl)
        httpGetResponse = urllib.request.urlopen(httpGetRequest).read().decode('utf-8')
        jsonData = json.loads(httpGetResponse)
        for bid in jsonData['response']['entities']['bids']:
            bidPrice = float(bid['price'])
            bidVolume = float(bid['amount'])
            if bidPrice not in self.bids:
                self.bids[bidPrice] = bidVolume
            else:
                self.bids[bidPrice] = self.bids[bidPrice] + bidVolume
        for ask in jsonData['response']['entities']['asks']:
            askPrice = float(ask['price'])
            askVolume = float(ask['amount'])
            if askPrice not in self.asks:
                self.asks[askPrice] = askVolume
            else:
                self.asks[askPrice] = self.asks[askPrice] + askVolume


    def createOrder(self, type, volume, price):
        httpAuthData = base64.encodestring('%s:%s'.format(self.userId, self.userSecret)).replace('\n', '')
        httpPostData = {'nonce': self.userSecret, 'pair_id': self.securityId,
                          'type': type, 'volume': volume, 'price': price}
        httpPostData = urllib.parse.urlencode(httpPostData)
        httpPostUrl = '{}order /new'.format(self.exchangeUrl)
        httpPostRequest = urllib.request.Request(httpPostUrl, httpPostData)
        httpPostRequest.add_header("Authorization", "Basic %s".format(httpAuthData))
        httpPostResponse = urllib.request.urlopen(httpPostRequest).read().decode('utf-8')
        jsonData = json.loads(httpPostResponse)
        self.orderId = jsonData['response']['entity']['order_id']
        self.transactionId = jsonData['response']['entity']['transaction_id']

