import datetime
from py_utils.rest_utils.client_bad_request import ClientBadRequest


class DateValidation:

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