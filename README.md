# financial-rest

## Summary
RESTful api to serve the portfolio data and portfolio transformations / calculations.

## Stack
- python 3.5
- flask

## Contract

- Get the portfolio transformed for [plotly.js](https://plot.ly/javascript/)
`curl -i -X GET http://{host}:5000/get-plotly-portfolio`

- Get the portfolio in raw csv 
`curl -i -X GET http://{host}:5000/get-portfolio`

## TODO
- clean up transform_util. It sucks atm.
- return times in epoch ms not microseconds
- unit tests for transform_util
- standard response messages for 4xx, 5xx
- create endpoints for the following:

1. `GET /portfolio?start={}&end={}`
2. `GET /normalized?symbols=[]&start={}&end={}`
3. `GET /returns?symbols=[]&type=[day \ month \year ]&start={}&end={}`
4. `GET /risk` using Sharpe ratio
5. `GET /holding/{id}` where id = Symbol. Example: holding/AAPL
6. `GET /holdings`
7. `GET /allocations` 