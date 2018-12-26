# financial-rest

## Summary
RESTful api to serve the portfolio data and portfolio transformations / calculations.

## Stack
- python 3.5
- flask

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
`curl -i -X GET -H "Authorization: <auth token>" https://lt311mje5d.execute-api.us-west-2.amazonaws.com/prod/portfolio`

## TODO
- clean up transform_util. It sucks atm.
- return times in epoch ms not microseconds - WONT DO, Needed for dataframe slice
- unit tests for transform_util: DONE
- standard response messages for 4xx, 5xx: 4xx DONE, 5xx Needed
- create endpoints for the following: - holdings to be done in a separate microservice

1. `GET /portfolio?start={}&end={}`
2. `GET /normalized?symbols=[]&start={}&end={}`
3. `GET /returns?symbols=[]&type=[day \ month \year ]&start={}&end={}`
4. `GET /risk` using Sharpe ratio
5. `GET /holding/{id}` where id = Symbol. Example: holding/AAPL
6. `GET /holdings`
7. `GET /allocations` 