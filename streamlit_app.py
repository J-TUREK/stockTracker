import os

from dotenv import load_dotenv

from app.main import main
import streamlit as st

# Load the environment variables
load_dotenv()

# Set up the page
start_date = os.environ.get("START_DATE")
fig, df = main(start_date)

st.set_page_config(layout="wide", page_title="Tabula Tickers November 2024 Comp")
st.plotly_chart(fig)
st.dataframe(df, use_container_width=True)
