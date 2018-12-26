
class ClientBadRequest(Exception):
    status = 400

    def __init__(self, message, status=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        if status is not None:
            self.status = status

    def to_dict(self):
        r = {'payload': self.payload, 'message': self.message}
        return r