import os

from dotenv import load_dotenv

from app.main import main
import streamlit as st

# Load the environment variables
load_dotenv()

# Set up the page
start_date = os.environ.get("START_DATE")
fig, df, metrics = main(start_date)

st.set_page_config(layout="wide", page_title="Tabula Tickers November 2024 Comp")
col1, col2, col3 = st.columns(3)
col1.metric(label="1st", value=metrics[0]["name"], delta="{}%".format(metrics[0]["percent_change"]))
col2.metric(label="2nd", value=metrics[1]["name"], delta="{}%".format(metrics[1]["percent_change"]))
col3.metric(label="3rd", value=metrics[2]["name"], delta="{}%".format(metrics[2]["percent_change"]))
st.plotly_chart(fig)
st.caption("Fig. below: Percentage changes from initial close price November 4th.")
st.dataframe(df, use_container_width=True)
