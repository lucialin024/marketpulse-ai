# 📈 MarketPulse AI
### AI-Powered Financial Market Intelligence & Stock Monitoring Platform

An interactive financial analytics platform integrating **Python, SQL, financial market data, and Google Gemini AI** to monitor stock performance, detect unusual market activity, and analyze potential market-moving news.

**Tech Stack:** Python | SQL | SQLite | Pandas | Yahoo Finance | Google Gemini API | Streamlit | Plotly

**[View GitHub Repository](https://github.com/lucialin024/marketpulse-ai)**

---

## Dashboard Preview

*Dashboard screenshots will be added here.*

---

## Project Overview

MarketPulse AI is an independently developed financial market intelligence prototype designed to simplify stock monitoring, market signal detection, and financial news analysis.

The project was inspired by my experience working in investment analysis, where monitoring stock price movements, evaluating financial news, and tracking price targets often required reviewing multiple data sources.

I developed MarketPulse AI to explore how **Python automation, SQL analytics, and generative AI** could bring these tasks together in a more accessible and interactive platform.

The application combines historical market data analysis with AI-assisted news interpretation to support financial research and investment monitoring.

### Business Questions

- Which stocks have experienced the strongest or weakest historical performance?
- Which companies have recorded significant daily price movements?
- Are unusual price movements accompanied by elevated trading volume?
- How do short-term and long-term moving averages compare?
- How far is a stock's latest closing price from a user-defined price target?
- What potential financial implications can be identified from earnings announcements, regulatory developments, and other business news?

---

## Key Features

### 1. Stock Market Monitoring

- Monitor six publicly traded companies: AAPL, MSFT, NVDA, GOOGL, AMZN, and JPM
- Retrieve historical stock prices through Yahoo Finance
- Calculate daily percentage changes and period returns
- Track user-defined stock price targets
- Visualize historical performance through interactive Plotly charts
- Download historical market data as CSV files

### 2. Python ETL & SQL Database

Developed a Python ETL workflow to extract, transform, and load stock market data into SQLite.

**Extract**
- Retrieve historical prices and trading volume through the Yahoo Finance interface

**Transform**
- Clean and standardize price observations
- Calculate daily stock returns
- Prepare structured data for SQL storage

**Load**
- Store company information and historical prices in relational tables
- Maintain relationships through primary and foreign keys
- Prevent duplicate daily price records using SQL constraints and upserts

### 3. SQL Market Analytics

Built SQL queries using Common Table Expressions (CTEs), joins, aggregations, and window functions to perform financial analysis.

The dashboard includes:

**Stock Performance Rankings**
- Compare historical returns across monitored companies
- Rank stocks by percentage performance

**Moving Average Analysis**
- Calculate five-session and 20-session moving averages
- Compare short-term price trends against longer-term trends

**Significant Price Movements**
- Identify historical daily returns of at least ±3%
- Categorize large increases and decreases

**Unusual Trading Volume**
- Compare daily trading volume against the preceding 20-session average
- Flag trading sessions where volume reaches at least twice the historical average

### 4. Gemini AI Financial News Intelligence

Integrated the Google Gemini API to analyze user-provided financial headlines and articles.

The AI analyzer is designed to generate:

- **News Summary:** Concise explanation of the reported event
- **Sentiment Classification:** Positive, Negative, Neutral, or Mixed
- **Event Category:** Earnings, M&A, Regulation, Product Launch, Macroeconomic, Management, or Other
- **Potential Market Implications:** Possible effects on investor expectations
- **Risk Assessment:** Missing information and key uncertainties
- **Analyst Follow-Up:** Questions requiring additional research

The implementation includes API timeout controls and error handling for temporary service failures.

### 5. AI Demonstration Mode

Implemented a standalone demonstration mode that displays a clearly labeled, prewritten example of financial news analysis.

This allows users to explore the intended AI research workflow without requiring an active Gemini API connection.

**Important:** Demo Mode uses fictional news and prewritten analysis. It is not a live Gemini-generated response.

---

## System Architecture

The application consists of two complementary analytical workflows.

### Market Data Analytics

```text
Yahoo Finance
      |
      v
Python ETL Pipeline
      |
      v
SQLite Database
      |
      v
SQL Financial Analytics
      |
      v
Streamlit Dashboard
      |
      v
Market Rankings, Charts & Signals
```

### AI Financial News Analysis

```text
User-Provided Financial News
      |
      v
Streamlit News Input
      |
      v
Google Gemini API
      |
      v
News Classification & Analysis
      |
      v
AI Research Summary
```

The AI component is separate from the SQL analytics workflow, allowing core financial monitoring features to remain available when the Gemini service experiences errors.

---

## Financial Analytics Methodology

### Daily Return

Daily Return = (Current Closing Price / Previous Closing Price) − 1

### Period Return

Period Return = (Latest Closing Price / First Closing Price) − 1

### Price Target Upside / Downside

Upside / Downside = (Target Price / Latest Closing Price) − 1

### Moving Averages

The five-session and 20-session moving averages are calculated using SQL window functions over historical closing prices.

### Price Movement Signals

A significant historical price movement is defined as:

- Daily Return ≥ +3%: Large Increase
- Daily Return ≤ −3%: Large Decrease

### Unusual Volume Signals

Volume Ratio = Current Trading Volume / Previous 20-Session Average Volume

A signal is generated when the ratio is at least 2.0.

These thresholds are illustrative research rules, not validated trading strategies.

---

## Project Structure

```text
marketpulse-ai/
|
|-- dashboard/
|   |-- app.py
|
|-- src/
|   |-- 01_create_database.py
|   |-- 02_load_stock_prices.py
|   |-- 03_run_sql_analysis.py
|   |-- 04_test_gemini.py
|
|-- sql/
|   |-- 01_market_analysis.sql
|
|-- data/
|   |-- marketpulse.db (local, excluded from Git)
|
|-- assets/
|
|-- .streamlit/
|   |-- secrets.toml (local, excluded from Git)
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

---

## Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/lucialin024/marketpulse-ai.git
cd marketpulse-ai
```

### 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The Python dependencies include:

- streamlit
- pandas
- yfinance
- plotly
- google-genai

### 4. Initialize the SQLite Database

```bash
python src/01_create_database.py
```

### 5. Load Historical Stock Prices

```bash
python src/02_load_stock_prices.py
```

The ETL script retrieves historical market data and stores the processed observations in SQLite.

An internet connection and access to the data provider are required.

### 6. Configure Gemini API Access (Optional)

To enable live Gemini analysis, create:

`.streamlit/secrets.toml`

Add your private API key:

```toml
GEMINI_API_KEY = "YOUR_PRIVATE_API_KEY"
```

Do not upload this file or share the key publicly.

The application can run in Demo Mode without Gemini credentials.

### 7. Launch the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL displayed in Terminal.

---

## Technologies & Skills Demonstrated

| Category | Tools & Skills |
|---|---|
| Programming | Python, SQL |
| Data Engineering | ETL, Data Cleaning, API Integration |
| Database | SQLite, Joins, CTEs, Window Functions |
| Financial Analytics | Returns, Moving Averages, Volume Analysis |
| Generative AI | Gemini API, Prompt Engineering, News Classification |
| Visualization | Streamlit, Plotly, Interactive Dashboards |
| Application Development | API Error Handling, Caching, Demo Mode |
| Version Control | Git, GitHub |

---

## Limitations & Future Improvements

MarketPulse AI is an educational prototype rather than a production trading or investment monitoring system.

Current limitations include:

- Yahoo Finance data may be delayed, adjusted, incomplete, or subject to usage restrictions
- SQL data is stored locally and updated through a manually executed ETL script
- Gemini analyzes user-provided text rather than automatically retrieving verified news articles
- AI responses may contain inaccuracies or experience API timeouts
- Price movement and volume thresholds are rule-based and have not been validated as predictive signals
- Price targets are manually entered rather than independently estimated by the application

### Potential Future Enhancements

- Automated financial news retrieval
- Scheduled market data updates
- Historical news sentiment and price reaction analysis
- Persistent storage of AI-generated analyses
- Model evaluation and structured sentiment classification
- Automated alerts and notifications
- Cloud-hosted database integration

---

## Data Privacy & Disclaimer

This project was independently developed for educational and portfolio demonstration purposes.

It uses publicly accessible market-data interfaces and fictional demonstration content. No confidential employer data, proprietary investment materials, or internal company information are included.

Market data is subject to the relevant providers' terms and licensing restrictions.

The platform does not provide investment recommendations, financial advice, or guaranteed real-time market monitoring.

---

## Author

**Lucia Lin**

Financial Analytics | Python | SQL | Data Automation | Investment Research

[GitHub Profile](https://github.com/lucialin024)
