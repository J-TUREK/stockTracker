import json
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
from PIL import Image
from alpaca.data import TimeFrame, TimeFrameUnit
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest


class HistoricalDataAlpacaClient:
    """
    AlpacaClient is a wrapper class for the Alpaca API. It provides access to the StockHistoricalDataClient class.
    """
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.client = StockHistoricalDataClient(self.api_key, self.secret_key)


def get_stock_list(stock_picks) -> list:
    """
    Return only the stock symbols from the STOCK_PICKS list.
    :return: list
    """
    return [stock["symbol"] for stock in stock_picks]


def format_response_df(data) -> pd.DataFrame:
    """
    Format the data to a DataFrame and return it.
    :param data: pd.DataFrame
    :return: pd.DataFrame
    """
    df = data.df
    # Get index and 'close' columns only
    df = df[['close']]
    # Re-index the DataFrame to separate the index into 'symbol' and 'timestamp' columns
    df = df.reset_index()
    # Convert the timestamp column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # I now have a DataFrame with the following columns: 'symbol', 'timestamp', 'close'
    # I want to now calculate the percent change for each stock from the START_DATE
    # For each grouping, determine the 'close' on the first day, or the START_DATE
    df['initial_close'] = df.groupby('symbol')['close'].transform('first')
    # Calculate the percent change from the initial close
    df['percent_change'] = (df['close'] - df['initial_close']) / df['initial_close'] * 100
    # Plot the percent change for each stock
    df = df.pivot(index='timestamp', columns='symbol', values='percent_change')
    # Back-fill the NaN values with the previous value
    df = df.ffill()

    # Based on the final row, order the columns in order of size
    last_row = df.iloc[-1]
    last_row = last_row.sort_values(ascending=False)
    df = df[last_row.index]
    return df


def get_img(symbol, stock_picks):
    """
    Get the image for the stock symbol.
    :param symbol: str
    :param stock_picks: list
    :return: str
    """
    for stock in stock_picks:
        if stock["symbol"] == symbol:
            img_name = stock.get("img")
            if not img_name:
                return None
            return Image.open(f"./img/{img_name}")
    return None


def get_name(symbol, stock_picks):
    """
    Get the name for the stock symbol.
    :param symbol: str
    :param stock_picks: list
    :return: str
    """
    for stock in stock_picks:
        if stock["symbol"] == symbol:
            return stock.get("name")
    return None


def read_stock_picks():
    # Read the .json file stock_picks.json
    with open("stock_picks.json", "r") as file:
        stock_picks = json.load(file)
    return stock_picks


def get_performance_metrics(df, stock_picks):
    """
    Get the top three stocks based on the last row of the DataFrame.
    :param df: pd.DataFrame
    :param stock_picks: list
    :return: pd.DataFrame
    """
    last_row = df.iloc[-1]
    series = last_row.sort_values(ascending=False)
    metrics = []
    rank = 1
    for s in series.items():
        symbol = s[0]
        name = get_name(s[0], stock_picks)
        percent_change = round(s[1], 1)
        metrics.append({"name": name, "symbol": symbol, "percent_change": percent_change})
        rank += 1

    metrics_df = pd.DataFrame(metrics)
    metrics_df.index = metrics_df.index + 1
    return metrics_df


def get_proportion_of_days_passed(start_date_str, end_date_str):
    today = datetime.now()
    # Calculate the number of days between the start and end date
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    days = (end_date - datetime.strptime(start_date_str, "%Y-%m-%d")).days
    # Calculate the percentage of days that have passed since the start date
    days_passed = (today - datetime.strptime(start_date_str, "%Y-%m-%d")).days
    percent = round(days_passed / days * 100, 1) / 100

    if percent > 1:
        percent = 1.

    return days_passed, days, percent


def main(start_date, end_date=None):
    stock_picks = read_stock_picks()
    client = HistoricalDataAlpacaClient()
    today = datetime.now()
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    if end_date >= today:
        # You cannot query data for a future date
        end_date = None

    symbols = get_stock_list(stock_picks)
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame(6, TimeFrameUnit.Hour),
        start=datetime.strptime(start_date, "%Y-%m-%d"),
        end=end_date
    )
    data = client.client.get_stock_bars(request_params)
    formatted_df = format_response_df(data)

    # Show the plot
    fig = px.line(formatted_df, labels={'value': 'Percent Change (%)'}, markers=True)

    # Get the x value as the last value in the index in the DataFrame
    last_x = formatted_df.index[-1]

    # Loop through unique y-values (assuming each line is represented by a column)
    for symbol in formatted_df.columns[0:]:
        last_y = formatted_df[symbol].iloc[-1]  # Get the last y value for each line
        image = get_img(symbol, stock_picks)
        # Add an image at the last node for each line
        fig.add_layout_image(
            dict(
                source=image,
                x=last_x,
                y=last_y,
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                sizex=3*24*60*60*1000,  # When you have a date type xaxis, the image sizex is given in miliseconds
                sizey=4
            )
        )

    # Update the legend to show the name of the person who picked the stock
    fig.for_each_trace(lambda trace: trace.update(name=f"{trace.name} ({get_name(trace.name, stock_picks)})"))
    # Update the legend title
    fig.update_layout(legend_title_text='Ticker')

    metrics_df = get_performance_metrics(formatted_df, stock_picks)
    # Sort the formatted_df by reverse index
    formatted_df = formatted_df.iloc[::-1]
    return fig, formatted_df, metrics_df


if __name__ == "__main__":
    main("2024-11-04")
