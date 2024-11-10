# Stock Tracker Comp.

A small web application for tracking a group of stocks between two dates.

## Setup

The application uses alpaca.markets for real time market data and requires .env variables ```ALPACA_API_KEY``` and ```ALPACA_SECRET_KEY```

Additionally requires two date .env variables of the form ```%Y-%m-%d```. ```START_DATE``` and ```END_DATE```

```stock_picks.json``` contains a list of values with "name" and "symbol" attributes used to query the market data and assign the 'results' with the person.
Optionally includes an "img" attribute for a filename contained in the "img" folder. The image will be your 'current' marker on the graph.

https://stocktracker-tabula-tickers.streamlit.app/
