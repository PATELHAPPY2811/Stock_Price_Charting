

# 📈 Real-time Two-Stock Price Dashboard with Streamlit and Polygon.io

This project is a **Streamlit web application** that allows users to visualize **real-time and historical stock price data** for **two different stocks at the same time**, using the **Polygon.io API**.

---

## 🚀 Features

* **🔹 Compare Two Stocks Simultaneously:**
  View two stock charts side-by-side in real time or over a chosen historical date range.

* **📊 Interactive Candlestick Charts:**
  Get deep insights from visually appealing candlestick charts showing **Open, High, Low, and Close** prices.

* **🕐 Real-time & Historical Modes:**

  * Real-time mode shows the latest available price.
  * Historical mode lets you explore data for custom date ranges.

* **⚙️ Polygon.io API Integration:**
  Retrieves accurate and up-to-date market data for selected symbols.

* **📁 Powered by Pandas & Plotly:**
  Smooth data processing with Pandas and rich visualizations via Plotly.

* **💪 Robust Error Handling:**
  Detects invalid symbols, API errors, and connectivity issues gracefully.

---

## 🧰 Tech Stack

* [Streamlit](https://streamlit.io/) — Interactive Python web app framework
* [Polygon.io](https://polygon.io/) — Market data API
* [Pandas](https://pandas.pydata.org/) — Data manipulation
* [Plotly](https://plotly.com/python/) — Interactive charting

---

## ⚡ Getting Started

### **1️⃣ Prerequisites**

Ensure you have **Python 3.10+** and the following libraries installed:

```bash
pip install streamlit pandas requests plotly
```

---

### **2️⃣ Clone the Repository**

```bash
git clone https://github.com/your-username/stock_price_charting.git
cd stock_price_charting
```

*(Replace `your-username` with your GitHub handle.)*

---

### **3️⃣ Get Your API Key**

* Sign up for a free account at [Polygon.io](https://polygon.io/).
* Copy your **API key**.
* Store it securely in `.streamlit/secrets.toml`:

```toml
POLYGON_API_KEY = "your_real_key_here"
```

> ⚠️ Do **not** hardcode your API key in the script.

---

### **4️⃣ Run the Application**

```bash
streamlit run app.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501).

---

## 💻 Usage

1. Enter **two stock symbols** (e.g., `AMD`, `NVDA`).
2. Choose a **time interval**:

   * `Real-time`, `1 minute`, `5 minute`, `15 minute`, `30 minute`, or `1 hour`
3. If not in real-time mode, pick a **date range**.
4. The app will:

   * Fetch both datasets from Polygon.io
   * Display **two interactive candlestick charts side-by-side**
   * Provide summary information for each symbol

---

## 🌐 Deployment on Streamlit Cloud

1. Push your project to GitHub.
2. Visit [StockPriceChart](https://stockpricecharting-20072054.streamlit.app/).
3. Connect your GitHub repo and deploy.
4. Add your API key in **App → Settings → Secrets**:

```
POLYGON_API_KEY="your_real_key_here"
```

5. Hit **Deploy** — your app will go live instantly!

---

## 💡 Tips & Enhancements

* Add in-code comments to improve readability.
* Customize chart themes or layouts with Plotly.
* Explore **websocket streaming** for live updates.
* Integrate technical indicators like moving averages or Bollinger Bands.

---

## 🤝 Contributing

Contributions are welcome!
If you’d like to suggest improvements or fix bugs:

1. Fork the repo
2. Create a new branch (`feature/your-feature-name`)
3. Commit your changes
4. Submit a pull request 🚀

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

### ✨ Author

**Happy Patel**
💼 *Business Analyst*
🌐 [LinkedIn](https://github.com/PATELHAPPY2811)

