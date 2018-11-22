import logging
import boto3
import numpy as np
from transform_util import TranformUtil
from portfolio_client import PortfolioClient
from dataframe_util import DataframeUtil



class Service:
    '''
    When this is ported to the serverless project,
    the PortfolioClient will be imported from the shared py utils package
    '''
    def __init__(self):
        self.transformer = TranformUtil()
        self.dataframeUtil = DataframeUtil()
        logging.info("Instantiating Service. First time load of portfolio from s3 . . .")
        s3 = boto3.client('s3', region_name='us-west-2')
        self.client = PortfolioClient(s3)
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)

    def get_portfolio(self):
        return self.portfolio

    def get_portfolio_transformed(self):
        return self.transformer.plotly_tranform(self.portfolio_df)

    def __refresh_portfolio(self):
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)