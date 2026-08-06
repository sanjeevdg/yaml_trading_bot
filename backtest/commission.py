class Commission:

    def __init__(self, commission=0.001):

        self.rate = commission

    def calculate(self, value):

        return value * self.rate
