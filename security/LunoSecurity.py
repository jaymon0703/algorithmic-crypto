from integration.LunoAdapter import LunoAdapter
from security.BitcoinSecurity import BitcoinSecurity


class LunoSecurity(BitcoinSecurity):
    def execute_order_book(self):
        LunoAdapter().load_order_book(self, self.order_book)

    def execute_order_decision(self):
        LunoAdapter().create_limit_order(self, self.order_decision)
