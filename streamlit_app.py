import datetime
import os

from dotenv import load_dotenv

from app.main import main, get_proportion_of_days_passed
import streamlit as st

# Load the environment variables
load_dotenv()

# Set up the page
start_date = os.environ.get("START_DATE")
end_date = os.environ.get("END_DATE")
fig, data_df, metrics_df = main(start_date)

days_passed, days, percent = get_proportion_of_days_passed(start_date, end_date)

# Display the page
st.set_page_config(layout="wide", page_title="Tabula Tickers November 2024 Comp")
st.progress(percent, text=f"Day {days_passed} / {days}")
st.write("")
st.write("")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="1st", value=f'{metrics_df.iloc[0]["name"]} ({metrics_df.iloc[0]["symbol"]})', delta="{}%".format(metrics_df.iloc[0]["percent_change"]))
col2.metric(label="2nd", value=f'{metrics_df.iloc[1]["name"]} ({metrics_df.iloc[1]["symbol"]})', delta="{}%".format(metrics_df.iloc[1]["percent_change"]))
col3.metric(label="3rd", value=f'{metrics_df.iloc[2]["name"]} ({metrics_df.iloc[2]["symbol"]})', delta="{}%".format(metrics_df.iloc[2]["percent_change"]))
col4.metric(label="4th", value=f'{metrics_df.iloc[3]["name"]} ({metrics_df.iloc[3]["symbol"]})', delta="{}%".format(metrics_df.iloc[3]["percent_change"]))
col5.metric(label="5th", value=f'{metrics_df.iloc[4]["name"]} ({metrics_df.iloc[4]["symbol"]})', delta="{}%".format(metrics_df.iloc[4]["percent_change"]))
st.plotly_chart(fig)
tab1, tab2 = st.tabs(["📊 Data", "📈 Ranking"])
tab1.dataframe(data_df, use_container_width=True)
tab2.dataframe(metrics_df, use_container_width=True)
