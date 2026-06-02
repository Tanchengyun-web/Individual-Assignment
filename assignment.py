import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define 5 Bursa Malaysia Stocks
stock_tickers = ["1155.KL", "1066.KL", "6012.KL", "5347.KL", "1295.KL"]
stock_names = {
    "1155.KL": "Malayan Banking Bhd",
    "1066.KL": "RHB Bank Berhad",
    "6012.KL": "Maxis Berhad",
    "5347.KL": "Tenaga Nasional Berhad",
    "1295.KL": "Public Bank Bhd"
}

start_date = "2026-01-01"  
end_date = "2026-02-01"
stock_data = yf.download(stock_tickers, start=start_date, end=end_date)
close_prices = stock_data["Close"]

def calculate_stock_metrics(ticker, close_df):
    """Calculate all required metrics for a single stock"""
    latest_close = close_df[ticker].iloc[-1]
    prev_close = close_df[ticker].iloc[-2]
    
    daily_return = latest_close - prev_close

    shares = 1000 / prev_close

    total_return = daily_return * shares
    return_pct = (total_return / 1000) * 100
    
    return {
        "Ticker": ticker,
        "Company Name": stock_names[ticker],
        "Previous Close (RM)": round(prev_close, 2),
        "Latest Close (RM)": round(latest_close, 2),
        "Daily Return (RM)": round(daily_return, 2),
        "Shares (RM1000)": round(shares, 2),
        "Estimated Total Return (RM)": round(total_return, 2),
        "Return Percentage (%)": round(return_pct, 2)
    }


portfolio = []
for ticker in stock_tickers:
    metrics = calculate_stock_metrics(ticker, close_prices)
    portfolio.append(metrics)

df = pd.DataFrame(portfolio)
print("="*80)
print("QUESTION 1: FULL STOCK PORTFOLIO METRICS")
print("="*80)
print(df.to_string(index=False))

sliced_df = df[["Ticker", "Previous Close (RM)", "Latest Close (RM)", 
                "Estimated Total Return (RM)", "Return Percentage (%)"]]

print("\n" + "="*80)
print("QUESTION 2a: SLICED PORTFOLIO SUMMARY")
print("="*80)
print(sliced_df.to_string(index=False))

def classify_performance(pct):
    if pct < 0:
        return "Negative Return"
    elif 0 <= pct <= 2:
        return "Moderate Return"
    else:
        return "High Return"

df["Performance Category"] = df["Return Percentage (%)"].apply(classify_performance)

grouped = df.groupby("Performance Category")["Estimated Total Return (RM)"].mean().reset_index()
grouped = grouped.rename(columns={"Estimated Total Return (RM)": "Average Total Return (RM)"})

print("\n" + "="*80)
print("QUESTION 2b: GROUPBY PERFORMANCE ANALYSIS")
print("="*80)
print(grouped.to_string(index=False))

plt.rcParams["font.size"] = 10

plt.figure(figsize=(12, 6))
for ticker in stock_tickers:
    plt.plot(close_prices.index, close_prices[ticker], label=stock_names[ticker])

plt.title("1-Month Closing Price Trend of 5 Bursa Malaysia Stocks", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Closing Price (RM)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
plt.bar(df["Ticker"], df["Return Percentage (%)"], color=["blue", "green", "orange", "red", "purple"])
plt.title("Return Percentage Comparison of 5 Stocks", fontsize=14)
plt.xlabel("Stock Ticker")
plt.ylabel("Return Percentage (%)")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.show()


print("\n✅ All analysis completed! Charts will pop up automatically.")
