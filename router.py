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

    :return:        the rendered template 'home.html'
    """
    return 'hello world'

@app.route('/get-portfolio')
def get_portfolio():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return service.get_portfolio()


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
