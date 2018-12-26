import boto3
import numpy as np
import datetime
from transform_util import TranformUtil
from portfolio_client import PortfolioClient
from dataframe_util import DataframeUtil
from calc_utils import CalcUtils
from client_bad_request import ClientBadRequest


class Service:
    '''
    When this is ported to the serverless project,
    the PortfolioClient will be imported from the shared py utils package
    '''
    def __init__(self, logger):
        # if date_range is None:
        now = datetime.datetime.now()
        self.start = "{0:%Y-%m-%d}".format(now - datetime.timedelta(30, 0))
        self.end = "{0:%Y-%m-%d}".format(now)
        self.transformer = TranformUtil()
        self.dataframeUtil = DataframeUtil()
        self.calcUtil = CalcUtils()
        self.logger = logger
        logger.info("Instantiating Service. First time load of portfolio from s3 . . .")
        s3 = boto3.client('s3', region_name='us-west-2')
        self.client = PortfolioClient(s3)
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)

    def get_portfolio_raw(self):
        return self.portfolio

    def get_portfolio(self, start, end):
        self.validate_dates(start, end)
        if start is None and end is None:
            start = self.start
            end = self.end
        return self.transformer.plotly_tranform(self.portfolio_df.ix[start:end])

    def refresh_portfolio(self):
        self.portfolio = self.client.get_portfolio_from_bucket()
        self.portfolio_df = self.dataframeUtil.handle_csv_bytestream(self.portfolio, np.float32)
        return self.transformer.plotly_tranform(self.portfolio_df)

    def get_portfolio_normalized(self, start, end):
        self.validate_dates(start, end)
        if start is None and end is None:
            start = self.start
            end = self.end
        normalized = self.calcUtil.normalize(self.portfolio_df.ix[start:end])
        return self.transformer.plotly_tranform(normalized)

    def get_portfolio_daily_returns(self, start, end):
        self.validate_dates(start, end)
        if start is None and end is None:
            start = self.start
            end = self.end
        dr = self.calcUtil.get_daily_returns(self.portfolio_df.ix[start:end])
        return self.transformer.plotly_tranform(dr)

    def validate_dates(self, start=None, end=None):
        fmt = "%Y-%m-%d"
        message = "Bad Request. Must provide valid start and end date."
        if start is None and end is None:
            return

        try:
            start = datetime.datetime.strptime(start, fmt)
            end = datetime.datetime.strptime(end, fmt)
        except Exception as e:
            self.logger.error("Portfolio Service Exception: {}".format(str(e)))
            raise ClientBadRequest(message, status=400, payload=str(e))

        if start > end:
            raise ClientBadRequest(message, status=400,
                                   payload="Start date must be before end date.")

