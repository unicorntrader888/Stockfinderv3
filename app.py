import streamlit as st
from scanner import scan_stocks

st.set_page_config(page_title="StockFinder V3", layout="wide")
st.title("🔍 Stock Finder App")

setup = st.selectbox(
    "Choose a Setup",
    [
        "200 EMA Support",
        "30 SMA Support",
        "30 SMA CIP",
        "ATH Breakout",
        "30 + 200 Combo"
    ]
)

timeframe = st.selectbox("Choose Timeframe", ["2H", "Daily"])

if st.button("Scan"):
    matches = scan_stocks(setup, timeframe)
    if matches:
        st.success(f"Found {len(matches)} matching stocks:")
        for stock in matches:
            st.subheader(stock["symbol"])
            st.image(stock["chart"])
    else:
        st.warning("No matching stocks found.")
