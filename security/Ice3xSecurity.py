from integration.Ice3xAdapter import Ice3xAdapter
from security.BitcoinSecurity import BitcoinSecurity


class Ice3xSecurity(BitcoinSecurity):
    def execute_order_book(self):
        Ice3xAdapter().load_order_book(self, self.order_book)

    def execute_order_decision(self):
        Ice3xAdapter().create_limit_order(self, self.order_decision)
