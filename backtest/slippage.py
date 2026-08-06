class Slippage:

    def __init__(self, slippage=0.0005):

        self.rate = slippage

    def apply(self, price):

        return price * (1 + self.rate)
