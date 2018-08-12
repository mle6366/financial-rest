import pandas as pd
import logging
import boto3
from portfolio_client import PortfolioClient


class Service:
    '''
    When this is ported to the serverless project,
    the PortfolioClient will be imported from the shared py utils package
    '''
    def __init__(self):
        logging.info("Instantiating Service. First time load of portfolio from s3 . . .")
        s3 = boto3.client('s3', region_name='us-west-2')
        client = PortfolioClient(s3)
        self.portfolio = client.get_portfolio_from_bucket()

    def get_portfolio(self):
        return self.portfolio