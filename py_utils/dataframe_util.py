import pandas as pd
import numpy as np
from io import StringIO
import logging
import datetime


class DataframeUtil:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self):
        now = datetime.datetime.now()
        start = "{0:%Y-%m-%d}".format(now - datetime.timedelta(7, 0))
        end = "{0:%Y-%m-%d}".format(now)
        self.date_range = pd.date_range(start, end)

    def handle_csv_bytestream(self, csv_bytestream, datatype=np.float64):
        '''
        This will tranform the s3 csv_bytestream response
        into a valid dataframe,
        or return an empty dataframe if the csv is malformed.

        :param csv_bytestream: bystream response from Boto S3
        :param datatype: numpy datatype, like np.float32
        :return: pandas Dataframe
        '''
        s = str(csv_bytestream, 'utf-8')

        # allows for buffered reading of the String
        buffered_string = StringIO(s)

        try:
            df = pd.read_csv(buffered_string,
                             dtype=datatype,
                             index_col='timestamp',
                             parse_dates=True)
        except Exception as e:
            logging.error('DataframeUtil: Error parsing s3 csv into dataframe. '
                          ' {}'.format(e))
            df = pd.DataFrame(index=self.date_range)
        return df
