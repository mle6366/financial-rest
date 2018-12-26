from flask import (
    Flask
)
from flask import request
from flask import jsonify
from flask import Response
from service import Service
from py_utils.rest_utils.client_bad_request import ClientBadRequest

# Create the application instance
app = Flask(__name__)

service = Service(app.logger)


@app.route('/portfolio/raw')
def get_portfolio_raw():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return: the raw portfolio from s3 as csv
    """
    response = service.get_portfolio_raw()
    resp = Response(response)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/portfolio')
def get_portfolio():
    """
    :return: the portfolio transformed for Plotly.js'
    points:
    [{
        x: [1, 2, 3],
        y: [3, 0, 2]
    }, ...
    ]
    """
    start = request.args.get('start')
    end = request.args.get('end')
    app.logger.info('start parameter received: {}'.format(start))
    app.logger.info('end parameter received: {}'.format(end))
    response = service.get_portfolio(start, end)
    resp = Response(response, mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/portfolio/refresh')
def refresh():
    """
    Refreshes portfolio data with the latest in s3
    :return: the portfolio from s3 as json
    """
    response = service.refresh_portfolio()
    resp = Response(response, mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/portfolio/normalize')
def get_normalized_portfolio():
    """
    :return: normalized portfolio as json
    """
    start = request.args.get('start')
    end = request.args.get('end')
    app.logger.info('start parameter received: {}'.format(start))
    app.logger.info('end parameter received: {}'.format(end))
    response = service.get_portfolio_normalized(start, end)
    resp = Response(response, mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/portfolio/daily-returns')
def get_daily_returns():
    """
    :return: daily returns of the portfolio, as json
    """
    start = request.args.get('start')
    end = request.args.get('end')
    app.logger.info('start parameter received: {}'.format(start))
    app.logger.info('end parameter received: {}'.format(end))
    response = service.get_portfolio_daily_returns(start, end)
    resp = Response(response, mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.errorhandler(ClientBadRequest)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
