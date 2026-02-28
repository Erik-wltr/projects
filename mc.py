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

#simulations parameter
portfolio_value = 100000

days = 10
confidence_interval = 0.95

simulation = 10000

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

#gives random z score to simulate randomness 
def random_z_score():
    return np.random.normal(0,1)

#Simulation

weights = np.array([1/len(tickers)]*len(tickers))
portfolio_expected_return = expected_return(weights, ln_returns)
portfolio_standard_deviation = standard_deviation(weights, cov_matrix)

def scenario_gain_loss(port_value, port_e_r, port_s_d, z_score, days):
    return port_value * port_e_r * days + port_value * port_s_d * z_score * np.sqrt(days)

scenarioReturns = []

for i in range(simulation):
    z_score = random_z_score()
    scenarioReturns.append(scenario_gain_loss(portfolio_value, portfolio_expected_return , portfolio_standard_deviation , z_score, days))

#evaluation

VaR = -np.percentile(scenarioReturns, 100*(1-confidence_interval))

def calculate_ES(scenarioReturns, VaR):
    shortfalls = []
    for i in range(len(scenarioReturns)):
        item = scenarioReturns[i]
        if item <= -VaR:
            shortfalls.append(item)
    return np.average(shortfalls)

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
    print("The initial portfolio value is: "+ str(portfolio_value)+"$")
    print("The VaR for a period of" , str(days), "days and a confidence interval of", str(confidence_interval*100), "% is", end =" ")
    print(str(round(VaR,2))+"$")
    print("The expected Shortfall is " + str(round(calculate_ES(scenarioReturns, VaR),2))+"$")
    #plot()
    return


if __name__ == "__main__":
    main()