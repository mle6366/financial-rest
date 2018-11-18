from flask import (
    Flask
)
from service import Service

# Create the application instance
app = Flask(__name__)

service = Service()

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return: hello world string'
    """
    return 'hello world'

@app.route('/get-portfolio')
def get_portfolio():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return: the raw portfolio as csv'
    """
    return service.get_portfolio()

@app.route('/get-plotly-portfolio')
def get_portfolio_transformed():
    """
    :return: the portfolio transformed for Plotly.js'
    points:
    [{
        x: [1, 2, 3],
        y: [3, 0, 2]
    }, ...
    ]
    """
    return service.get_portfolio_transformed()


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
