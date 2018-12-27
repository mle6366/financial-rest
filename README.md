# Portfolio API

## Summary
(WIP) RESTful api to serve the portfolio data for [plotly-js](https://plot.ly/javascript/).

Currently supports dataframe-to-json plotly-js transformation, normalization (pictured below), and daily return calculations.
Future work includes Sharpe ratio, bollinger bands, and scatter-plot support (passing in symbols as args for comparison against the portfolio.)

![plotly-js graphing the portfolio](https://github.com/mle6366/financial-rest/blob/master/example/plotly-ui.png "Portfolio data graphed in Plotly.js")

This is a small part of a larger, on-going financial data project. The larger project leverages multiple
interconnected [serverless](https://serverless.com/framework/) components deployed in AWS. Within that environment,
this API is deployed and handles requests via the [serverless wsgi plugin](https://www.npmjs.com/package/serverless-wsgi) 
and is protected behind API Gateway and our [Custom OAuth Authorizer](https://github.com/ExpanseLLC/lambda_authorizer/wiki).

This README only includes how to run this as a standalone Flask app.

## Notes
Reference `tests/data` for the portfolio data format


## Getting Started

Set env variables.
Add the whitelisted domains as `CORS_DOMAINS` for your client(s). In this example, we are whitelisting everything.

```bash

export BUCKET="foo-bucket"
export KEY="bar"
export CORS_DOMAINS="*"

```

Install and run the application.

```
python3 -m venv .venv/

source .venv/bin/activate

pip3 install -r requirements.txt

python3 router.py
```

## Stack / Technologies
- python 3.5
- flask
- pandas
- aws s3


## Contract

- Get the portfolio transformed for [plotly.js](https://plot.ly/javascript/)

`curl -i -X GET http://{host}:5000/portfolio?start=2018-07-13&end=2018-12-26`

- Get the portfolio in raw csv 

`curl -i -X GET http://{host}:5000/portfolio/raw`

- Get the normalized portfolio

`curl -i -X GET http://{host}:5000/portfolio/normalize`

- Get the daily returns of the portfolio

`curl -i -X GET http://{host}:5000/portfolio/daily-returns`

- Reload the portfolio (which is stored in service memory as a dataframe) from s3 with the latest data

`curl -i -X GET http://{host}:5000/portfolio/refresh`

## API Gateway / Lambda Calls

`curl -i -X GET -H "Authorization: <auth token>" https://{host}.execute-api.us-west-2.amazonaws.com/prod/portfolio`

## TODO
- clean up transform_util. 
- return times in epoch ms not microseconds - WONT DO, Needed for dataframe slice
- unit tests for transform_util: DONE
- standard response messages for 4xx, 5xx: 4xx DONE, 5xx Needed
- create endpoints for the following: - holdings to be done in a separate microservice
