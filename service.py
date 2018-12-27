"""
 Expanse, LLC
 http://expansellc.io

 Copyright 2018
 Released under the Apache 2 license
 https://www.apache.org/licenses/LICENSE-2.0

 @authors Meghan Erickson
"""
import boto3
import numpy as np
import datetime
from py_utils.transformer import Transformer
from py_utils.portfolio_client import PortfolioClient
from py_utils.dataframe_util import DataframeUtil
from py_utils.calc import Calc
from py_utils.date_validation import DateValidation


class Service:
    def __init__(self, logger):
        # if date_range is None:
        now = datetime.datetime.now()
        self.start = '{0:%Y-%m-%d}'.format(now - datetime.timedelta(30, 0))
        self.end = '{0:%Y-%m-%d}'.format(now)
        self.transformer = Transformer()
        self.dataframeUtil = DataframeUtil()
        self.dateValidation = DateValidation()
        self.calcUtil = Calc()
        self.logger = logger
        logger.info('Instantiating Service. First time load of portfolio from s3 . . .')
        s3 = boto3.client('s3', region_name='us-west-2')
        self.client = PortfolioClient(s3)
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)

    def get_portfolio_raw(self):
        return self.portfolio

    def get_portfolio(self, start, end):
        self.dateValidation.validate_dates(start, end)
        if start is None and end is None:
            start = self.start
            end = self.end
        return self.transformer.plotly_tranform(self.portfolio_df.ix[start:end])

    def refresh_portfolio(self):
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)
        return self.transformer.plotly_tranform(self.portfolio_df)

    def get_portfolio_normalized(self, start, end):
        self.dateValidation.validate_dates(start, end)
        if start is None and end is None:
            start = self.start
            end = self.end
        normalized = self.calcUtil.normalize(self.portfolio_df.ix[start:end])
        return self.transformer.plotly_tranform(normalized)

    def get_portfolio_daily_returns(self, start, end):
        self.dateValidation.validate_dates(start, end)
        if start is None and end is None:
            start = self.start
            end = self.end
        dr = self.calcUtil.get_daily_returns(self.portfolio_df.ix[start:end])
        return self.transformer.plotly_tranform(dr)