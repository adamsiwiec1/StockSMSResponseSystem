import time


class Stock(object):

    def __init__(self, raw, name, acronym, price, float_price, floor, ceiling):
        self.raw = raw,
        self.name = name.upper()
        self.acronym = acronym
        self.price = price
        self.float_price = float_price
        self.floor = floor
        self.ceiling = ceiling
        self.count = 0
        self.limitCount = 0

    def alert_count(self):
        self.count += 1

    def reset_count(self):
        self.count = 0

    def limit_count(self):
        self.limitCount += 1

    def reset_limit_count(self):
        self.limitCount = 0