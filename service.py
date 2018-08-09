import pandas as pd


class Service:
    def __init__(self):
        self.file = 'data/portfolio.csv'

    def get_portfolio(self):
        return self.file