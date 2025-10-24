import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, date

# --- Config ---
API_KEY = 'QwznCIMoAuFPf2M1chnINcXmd9TzGxAQ' 

# --- API Helpers ---
def get_real_time_price(symbol: str):
    """
    Fetches previous close (latest available aggregate) for the symbol from Polygon.io.
    Note: /v2/aggs/ticker/{symbol}/prev returns the most recent aggregate (prev close).
    """
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol.upper()}/prev'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            return r.json()
        return {'Error': f"API request failed with status code: {r.status_code}"}
    except requests.exceptions.RequestException as e:
        return {'Error': f"Network error: {e}"}

def get_historical_price(symbol: str, from_date: str, to_date: str, multiplier: int, timespan: str):
    """
    Fetches historical aggregates for a symbol using Polygon.io range endpoint.
    Example:
      /v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from}/{to}
    """
    symbol = symbol.upper()
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/"
        f"{multiplier}/{timespan}/{from_date}/{to_date}"
        f"?adjusted=true&sort=asc&limit=50000&apiKey={API_KEY}"
    )
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            return r.json()
        return {'Error': f"API request failed with status code: {r.status_code}"}
    except requests.exceptions.RequestException as e:
        return {'Error': f"Network error: {e}"}

# --- UI Helpers ---
def interval_to_polygon_params(interval_label: str):
    """
    Map user-friendly interval to (multiplier, timespan).
    """
    mapping = {
        "1 minute": (1, "minute"),
        "5 minute": (5, "minute"),
        "15 minute": (15, "minute"),
        "30 minute": (30, "minute"),
        "1 hour": (1, "hour"),
    }
    return mapping.get(interval_label)

def make_candlestick(df: pd.DataFrame, title: str):
    fig = go.Figure(
        data=[go.Candlestick(
            x=df.index,
            open=df['o'],
            high=df['h'],
            low=df['l'],
            close=df['c']
        )]
    )
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

def render_stock_panel(symbol: str, interval_choice: str, from_date: date | None, to_date: date | None):
    """
    Render one stock panel (either real-time prev or historical range).
    """
    if not symbol:
        st.info("Enter a symbol to view data.")
        return

    try:
        if interval_choice == "Real-time":
            data = get_real_time_price(symbol)
            if 'Error' in data:
                st.error(data['Error'])
                return
            if not data.get('results'):
                st.warning("No data returned.")
                return
            df = pd.DataFrame([data['results'][0]])
            # Polygon 't' is ms for aggs
            if 't' in df.columns:
                df['t'] = pd.to_datetime(df['t'], unit='ms')
                df.set_index('t', inplace=True)
            st.write(f"**{symbol.upper()} (latest: {df.index[-1] if not df.empty else 'N/A'})**")
        else:
            params = interval_to_polygon_params(interval_choice)
            if not params:
                st.error("Invalid interval selected.")
                return
            # dates to str
            f_str = from_date.strftime("%Y-%m-%d")
            t_str = to_date.strftime("%Y-%m-%d")
            data = get_historical_price(symbol, f_str, t_str, *params)
            if 'Error' in data:
                st.error(data['Error'])
                return
            results = data.get('results', [])
            if not results:
                st.warning("No data returned for the selected range.")
                return
            df = pd.DataFrame(results)
            # Polygon aggregates: timestamp 't' is in ms
            df['t'] = pd.to_datetime(df['t'], unit='ms')
            df.set_index('t', inplace=True)
            st.write(f"**{symbol.upper()} ({f_str} → {t_str})**")

        st.caption("Candlestick shows OHLC per selected interval.")
        fig = make_candlestick(df, f"{symbol.upper()} Candlestick")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- App ---
def main():
    st.title("US Stock Viewer")

    # Inputs for two symbols
    col_syms = st.columns(2)
    with col_syms[0]:
        symbol1 = st.text_input("Use Only Stock Symbol 1:", key="sym1")
    with col_syms[1]:
        symbol2 = st.text_input("Use Only Stock Symbol 2:", key="sym2")

    # Interval choice (shared)
    interval_options = ["Real-time", "1 minute", "5 minute", "15 minute", "30 minute", "1 hour"]
    interval_choice = st.selectbox("Select Time Interval:", interval_options)

    # Date pickers only when historical
    from_dt = None
    to_dt = None
    if interval_choice != "Real-time":
        today = datetime.today().date()
        col_dates = st.columns(2)
        with col_dates[0]:
            from_dt = st.date_input("From Date:", value=date(2023, 11, 28), key="from")
        with col_dates[1]:
            to_dt = st.date_input("To Date:", value=today, key="to")
        if from_dt > to_dt:
            st.error("From Date must be on or before To Date.")
            return

    # Render side-by-side panels
    c1, c2 = st.columns(2)
    with c1:
        with st.spinner("Fetching data for Symbol 1..."):
            render_stock_panel(symbol1, interval_choice, from_dt, to_dt)
    with c2:
        with st.spinner("Fetching data for Symbol 2..."):
            render_stock_panel(symbol2, interval_choice, from_dt, to_dt)

if __name__ == "__main__":
    main()
