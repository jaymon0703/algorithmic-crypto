class BitcoinAdapter:
    def load_order_book(self, bitcoin_security, order_book):
        order_book.reset_book()
        return order_book

    def create_limit_order(self, bitcoin_security, order_decision):
        order_decision.set_id(0)
        return order_decision
