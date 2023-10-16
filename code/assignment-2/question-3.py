import math

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

tickers = ["AAPL", "EBAY", "GOOG", "INTC", "MSFT", "ORCL"]
arithmetic_returns_column_name = "ArithmeticReturn"
logarithmic_returns_column_name = "LogReturn"

portfolio = {}
annual_expected_returns = []
annual_volatilities = []

for ticker in tickers:
    portfolio_snapshot = {}

    ticker_df = pd.read_csv("../../resources/assignment-2/question-3/"+ticker+".csv")[["Date", "Adj Close"]]
    ticker_df['PreviousAdjClose'] = ticker_df["Adj Close"].shift(1)

    ticker_df[arithmetic_returns_column_name] = (ticker_df["Adj Close"] / ticker_df["PreviousAdjClose"]) - 1
    ticker_df[logarithmic_returns_column_name] = np.log((ticker_df["Adj Close"] / ticker_df["PreviousAdjClose"]))

    arith_mean = ticker_df[arithmetic_returns_column_name].mean()
    arith_variance = ticker_df[arithmetic_returns_column_name].var()
    arith_skewness = ticker_df[arithmetic_returns_column_name].skew()
    arith_kurtosis = ticker_df[arithmetic_returns_column_name].kurtosis()

    log_mean = ticker_df[logarithmic_returns_column_name].mean()
    log_variance = ticker_df[logarithmic_returns_column_name].var()
    log_skewness = ticker_df[logarithmic_returns_column_name].skew()
    log_kurtosis = ticker_df[logarithmic_returns_column_name].kurtosis()

    value = 100 # Let's assume we put 100 bucks into this ticker on Jan 01, 2018
    value_vector = [100]
    for index, row in ticker_df.iterrows():
        if index > 0:
            value = value * (1 + row[arithmetic_returns_column_name])
            value_vector.append(value)

    ticker_df[ticker + "_Value"] = value_vector

    portfolio[ticker + "_Value"] = value_vector

    print(ticker, "Arithmetic Properties", f"Mean: {arith_mean}", f"Var: {arith_variance}", f"Skew: {arith_skewness}", f"Kurtosis: {arith_kurtosis}")
    print(ticker, "Log", f"Mean: {log_mean}", f"Var: {log_variance}", f"Skew: {log_skewness}", f"Kurtosis: {log_kurtosis}")

    # Now, the second part asking for yearly expected returns vs volatility graph
    ticker_df_yearly = ticker_df[ticker_df.index % 12 == 0][["Date", "Adj Close"]].reset_index(drop=True)
    ticker_df_yearly["PreviousAdjClose"] = ticker_df_yearly["Adj Close"].shift(1)
    ticker_df_yearly[logarithmic_returns_column_name] = np.log((ticker_df_yearly["Adj Close"] / ticker_df_yearly["PreviousAdjClose"]))
    annual_expected_returns.append(ticker_df_yearly[logarithmic_returns_column_name].mean())
    annual_volatilities.append(math.sqrt(ticker_df_yearly[logarithmic_returns_column_name].var()))


portfolio_df = pd.DataFrame(portfolio)
portfolio_df["TotalValue"] = portfolio_df.sum(axis=1)
portfolio_df["PreviousTotalValue"] = portfolio_df["TotalValue"].shift(1)
portfolio_df[arithmetic_returns_column_name] = (portfolio_df["TotalValue"] / portfolio_df["PreviousTotalValue"]) - 1
portfolio_df[logarithmic_returns_column_name] = np.log((portfolio_df["TotalValue"] / portfolio_df["PreviousTotalValue"]))
portfolio_df.to_csv("question3_portfolio.csv", index=False)

# Now, the second part asking for yearly expected returns vs volatility graph
portfolio_df_yearly = portfolio_df[portfolio_df.index % 12 == 0][["TotalValue"]].reset_index(drop=True)
portfolio_df_yearly["PreviousTotalValue"] = portfolio_df_yearly["TotalValue"].shift(1)
portfolio_df_yearly[logarithmic_returns_column_name] = np.log((portfolio_df_yearly["TotalValue"] / portfolio_df_yearly["PreviousTotalValue"]))
annual_expected_returns.append(portfolio_df_yearly[logarithmic_returns_column_name].mean())
annual_volatilities.append(math.sqrt(portfolio_df_yearly[logarithmic_returns_column_name].var()))
tickers.append("MyPortfolio")

fig, ax = plt.subplots()
ax.scatter(annual_expected_returns, annual_volatilities)
ax.set_xlabel("Annual Expected Returns")
ax.set_ylabel("Annual Expected Volatility")
for i, txt in enumerate(tickers):
    ax.annotate(txt, (annual_expected_returns[i], annual_volatilities[i]))
plt.show()

# For the code, please visit https://github.com/capatazche/cfrm-501
# The portfolio seems to bring the best of both worlds compared the individual stocks.
# It seems to have a better return than most the individual stocks,
# while also having a very low volatility compared to the individual stocks.
