import pandas as pd

arith_returns_col_name = "ArithmeticReturn"

ticker_df = pd.read_csv("../../resources/assignment-2/question-4/MSFT_question4.csv")[["Date", "Adj Close"]]
ticker_df["PreviousAdjClose"] = ticker_df["Adj Close"].shift(1)

ticker_df[arith_returns_col_name] = (ticker_df["Adj Close"] / ticker_df["PreviousAdjClose"]) - 1

arith_mean = ticker_df[arith_returns_col_name].mean()
arith_variance = ticker_df[arith_returns_col_name].var()
arith_skewness = ticker_df[arith_returns_col_name].skew()
arith_kurtosis = ticker_df[arith_returns_col_name].kurtosis()

print("Arithmetic Properties", f"Mean: {arith_mean}", f"Var: {arith_variance}", f"Skew: {arith_skewness}", f"Kurtosis: {arith_kurtosis}")
