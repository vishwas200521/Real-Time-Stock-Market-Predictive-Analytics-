import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def load_css():
    css_path = Path(__file__).parent / "styles.css"
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="Real-Time Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# LOAD DATA
# ======================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ======================================
# LOAD DATA
# ======================================

with st.spinner("📈 Loading Stock Market Data..."):
    df = pd.read_csv(DATA_DIR / "stock_features.csv")
    forecast = pd.read_csv(DATA_DIR / "forecast.csv")


df["Date"] = pd.to_datetime(df["Date"])
forecast["ds"] = pd.to_datetime(forecast["ds"])

# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("📊 Dashboard Controls")

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Date"].max().date()
)

df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

st.sidebar.markdown("---")

st.sidebar.header("📌 Project Information")

st.sidebar.write("**Real-Time Stock Market Predictive Analytics Dashboard**")

st.sidebar.markdown("""
### Technologies Used
- 🐍 Python
- 📊 Pandas
- 📈 Plotly
- 🤖 Prophet
- 🎨 Streamlit
""")
# ======================================
# HEADER
# ======================================

st.title("📈 Real-Time Stock Market Predictive Analytics Dashboard")

st.markdown(
"""
Interactive dashboard for historical stock analysis and
AI-powered stock price forecasting using **Facebook Prophet**.
"""
)

st.divider()

# ======================================
# KPI SECTION
# ======================================

current_price = df["Close"].iloc[-1]
highest_price = df["High"].max()
lowest_price = df["Low"].min()
average_volume = int(df["Volume"].mean())

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"${current_price:.2f}"
)

col2.metric(
    "Highest Price",
    f"${highest_price:.2f}"
)

col3.metric(
    "Lowest Price",
    f"${lowest_price:.2f}"
)

col4.metric(
    "Average Volume",
    f"{average_volume:,}"
)

st.divider()

# ======================================
# DASHBOARD TABS
# ======================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "📈 Technical Analysis",
    "🤖 AI Forecast",
    "📄 Dataset"
])
# ======================================
# HISTORICAL PRICE CHART
# ======================================
with tab1:

    st.subheader("📈 Historical Closing Price")

    price_chart = px.line(
        df,
        x="Date",
        y="Close",
        title="Historical Closing Price"
    )

    price_chart.update_layout(
        template="plotly_dark",
        height=550,
        title_x=0.3
    )

    st.plotly_chart(
        price_chart,
        width="stretch",
        key="historical_price"
    )

# ======================================
# CANDLESTICK CHART
# ======================================

st.divider()

st.subheader("📉 Candlestick Chart")

candlestick = go.Figure(
    data=[
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color="green",
            decreasing_line_color="red",
            name="OHLC"
        )
    ]
)

candlestick.update_layout(
    template="plotly_dark",
    height=650,
    xaxis_title="Date",
    yaxis_title="Price ($)",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    candlestick,
    width="stretch",
    key="candlestick_chart"
)
# ======================================
# MOVING AVERAGE CHART
# ======================================

st.divider()

st.subheader("📈 Moving Average Analysis")

ma_chart = go.Figure()

ma_chart.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Close"],
        name="Close Price",
        line=dict(width=2)
    )
)

ma_chart.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["MA20"],
        name="20-Day MA",
        line=dict(dash="dash")
    )
)

ma_chart.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["MA50"],
        name="50-Day MA",
        line=dict(dash="dot")
    )
)

ma_chart.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Date",
    yaxis_title="Price ($)"
)

st.plotly_chart(
    ma_chart,
    width="stretch",
    key="moving_average"
)
# ======================================
# TRADING VOLUME
# ======================================

st.divider()

st.subheader("📊 Daily Trading Volume")

volume_chart = px.bar(
    df,
    x="Date",
    y="Volume",
    title="Trading Volume"
)

volume_chart.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    volume_chart,
    width="stretch",
    key="volume_chart"
)
# ======================================
# DAILY RETURN
# ======================================

st.divider()

st.subheader("📉 Daily Return (%)")

return_chart = px.line(
    df,
    x="Date",
    y="Daily_Return",
    title="Daily Return"
)

return_chart.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    return_chart,
    width="stretch",
    key="daily_return"
)
# ======================================
# VOLATILITY
# ======================================

st.divider()

st.subheader("📊 Rolling Volatility")

vol_chart = px.line(
    df,
    x="Date",
    y="Volatility",
    title="20-Day Rolling Volatility"
)

vol_chart.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    vol_chart,
    width="stretch",
    key="volatility_chart"
)


st.divider()

st.subheader("📊 Forecast Summary")

future_price = forecast["yhat"].iloc[-1]
max_prediction = forecast["yhat"].max()
min_prediction = forecast["yhat"].min()
avg_prediction = forecast["yhat"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Final Forecast",
    f"${future_price:.2f}"
)

c2.metric(
    "Maximum Forecast",
    f"${max_prediction:.2f}"
)

c3.metric(
    "Minimum Forecast",
    f"${min_prediction:.2f}"
)

c4.metric(
    "Average Forecast",
    f"${avg_prediction:.2f}"
)
st.divider()

st.subheader("📋 Forecast Data")

forecast_display = forecast[
    ["ds","yhat","yhat_lower","yhat_upper"]
].copy()

forecast_display.columns = [
    "Date",
    "Predicted Price",
    "Lower Bound",
    "Upper Bound"
]

st.dataframe(
    forecast_display.tail(30),
    width="stretch",
    hide_index=True
)
st.divider()

st.subheader("📈 AI Insights")

current_price = df["Close"].iloc[-1]
predicted_price = forecast["yhat"].iloc[-1]

difference = predicted_price - current_price
percentage = (difference / current_price) * 100

if percentage > 0:
    st.success(
        f"📈 Prophet predicts a potential increase of {percentage:.2f}% over the forecast period."
    )
else:
    st.error(
        f"📉 Prophet predicts a potential decrease of {abs(percentage):.2f}% over the forecast period."
    )