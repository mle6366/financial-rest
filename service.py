import logging
import boto3
import numpy as np
from transform_util import TranformUtil
from portfolio_client import PortfolioClient
from dataframe_util import DataframeUtil
from calc_utils import CalcUtils


class Service:
    '''
    When this is ported to the serverless project,
    the PortfolioClient will be imported from the shared py utils package
    '''
    def __init__(self):
        self.transformer = TranformUtil()
        self.dataframeUtil = DataframeUtil()
        self.calcUtil = CalcUtils()
        logging.info("Instantiating Service. First time load of portfolio from s3 . . .")
        s3 = boto3.client('s3', region_name='us-west-2')
        self.client = PortfolioClient(s3)
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)

    def get_portfolio_raw(self):
        return self.portfolio

    def get_portfolio(self):
        return self.transformer.plotly_tranform(self.portfolio_df)

    def refresh_portfolio(self):
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)
        return self.transformer.plotly_tranform(self.portfolio_df)

    def get_portfolio_normalized(self):
        normalized = self.calcUtil.normalize(self.portfolio_df)
        return self.transformer.plotly_tranform(normalized)

    def get_portfolio_daily_returns(self):
        dr = self.calcUtil.get_daily_returns(self.portfolio_df)
        return self.transformer.plotly_tranform(dr)