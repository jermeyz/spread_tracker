import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

st.title('Spread Tracker')

# Title and user input
st.title("Stock Price Chart with Altair")

# Allow user to input stock ticker and date range
ticker = st.text_input("Enter the stock ticker:", "AAPL")
start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

# Fetch stock data
if ticker:
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)  # Reset index to use date as a column

    # Check if data is available
    if not stock_data.empty:
        # Create Altair line chart
        line_chart_left = (
            alt.Chart(stock_data)
            .mark_rule().encode(
                x='Date:T',
                y='Low:Q',
                y2='High:Q'
            ) + alt.Chart(stock_data).mark_bar().encode(
                x='Date:T',
                y='Open:Q',
                y2='Close:Q',
                color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red")),
                tooltip=['Date:T', 'Open:Q', 'High:Q', 'Low:Q', 'Close:Q']
            )
            .encode(
                x='Date:T',
                y=alt.Y('Close:Q', title='Closing Price', axis=alt.Axis(titleColor='blue', orient='left')),
                tooltip=['Date:T', 'Close:Q']
            )
            .properties(
                title=f"{ticker} Stock Prices",
                width=700,
                height=400
            )
        )

        # Create a duplicate line chart with y-axis on the right
        line_chart_right = (
            alt.Chart(stock_data)
            .mark_rule().encode(
                x='Date:T',
                y='Low:Q',
                y2='High:Q'
            ) + alt.Chart(stock_data).mark_bar().encode(
                x='Date:T',
                y='Open:Q',
                y2='Close:Q',
                color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red")),
                tooltip=['Date:T', 'Open:Q', 'High:Q', 'Low:Q', 'Close:Q']
            )
            .encode(
                x='Date:T',
                y=alt.Y('Close:Q', title='Closing Price', axis=alt.Axis(titleColor='blue', orient='right')),
                tooltip=['Date:T', 'Close:Q']
            )
            .properties(
                width=700,
                height=400
            )
        )
        # Create a vertical bar at the specified date
        bar = (
            alt.Chart(pd.DataFrame({'Date': ['2024/11/04']}))
            .mark_rule(color='red', size=2)  # Red bar with thickness
            .encode(x='Date:T')
        )

        # Optional: Specify the start and end dates for the highlight box
        highlight_start = st.date_input("Highlight box start date:", pd.to_datetime("2024-07-01"))
        highlight_end = st.date_input("Highlight box end date:", pd.to_datetime("2024-07-15"))

        # Input for box y-axis range
        box_y_min = st.number_input("Box minimum y-value:", value=150.0)
        box_y_max = st.number_input("Box maximum y-value:", value=200.0)

        box = (
            alt.Chart(pd.DataFrame({
                'start': [highlight_start],
                'end': [highlight_end],
                'y_min': [box_y_min],
                'y_max': [box_y_max]
            }))
            .mark_rect(color='lightblue', opacity=0.3)  # Light blue box with transparency
            .encode(
                x='start:T',
                x2='end:T',
                y='y_min:Q',
                y2='y_max:Q'
            )
        )

        # Layer the line chart and bar
        layered_chart = (box + line_chart_left + line_chart_right + bar).interactive()

        st.altair_chart(layered_chart, use_container_width=True)
    else:
        st.write("No data available for the selected range.")