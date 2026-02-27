import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import yfinance as yf
from scipy.stats import norm

#sets up start and end dates
years = 15
endDate = dt.datetime.now()
startDate= endDate - dt.timedelta(days = 365*years)

#tickers 
tickers = ['SPY', 'BND', 'GLD', 'QQQ', 'VWO', 'DUOL']

#download the dailey adjusted close prices 
adj_close_df = pd.DataFrame()
for ticker in tickers: 
    data = yf.download(ticker,start = startDate,end = endDate)
    adj_close_df[ticker] = data['Close']

#calculate the dailey ln-returns
ln_returns = np.log(adj_close_df/adj_close_df.shift(1))
ln_returns = ln_returns.dropna()

#calculates the coveriance of the ln_returns
cov_matrix = ln_returns.cov()

#define function to calculate the future returns based on the past returns
def expected_return(weights, ln_returns):
    return np.sum(ln_returns.mean()*weights)

#define a function to calculate the protfolio standard deviation
def standard_deviation(weight, cov_matrix):
    variance = weight.T @ cov_matrix @ weight
    return np.sqrt(variance)

def random_z_score():
    return np.random.normal(0,1)

#Simulation
portfolio_value = 100000
weights = np.array([1/len(tickers)]*len(tickers))
portfolio_expected_return = expected_return(weights, ln_returns)
portfolio_standard_deviation = standard_deviation(weights, cov_matrix)

days = 10

def scenario_gain_loss(port_value, port_e_r, port_s_d, z_score, days):
    return port_value * port_e_r * days + port_value * port_s_d * z_score * np.sqrt(days)

simulation = 10000
scenarioReturns = []

for i in range(simulation):
    z_score = random_z_score()
    scenarioReturns.append(scenario_gain_loss(portfolio_value, portfolio_expected_return , portfolio_standard_deviation , z_score, days))

#evaluation
confidence_interval = 0.95
VaR = -np.percentile(scenarioReturns, 100*(1-confidence_interval))

def plot():
    plt.hist(scenarioReturns, bins=50, density = True )
    plt.xlabel("scenario Gain/Loss in $")
    plt.ylabel("Frequency")
    plt.title(f"Dist of Portfolio over {days} Days")
    plt.axvline(-VaR, color='r', linestyle='dashed', label=f"VaR at {confidence_interval}%")
    plt.legend()
    plt.show()
    return


def main():
    print("portfolio value", portfolio_value)
    print("days:", days)
    print("confidence level:", confidence_interval)
    print(VaR)
    plot()
    return


if __name__ == "__main__":
    main()