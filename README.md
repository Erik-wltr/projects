# Monte Carlo Value-at-Risk (VaR) and Expected Shortfall (ES) Simulation


This project implements a Monte Carlo simulation to estimate the Value-at-Risk (VaR) and Expected Shortfall (ES) of a diversified portfolio over a 90-day horizon at a 95% confidence level.

The objective is to quantify potential downside risk using historical return statistics.


### Portfolio Specification:

Assets (sourced from Yahoo Finance, adjusted closing prices):

SPY,
BND,
GLD,
QQQ,
VWO,
DUOL

Portfolio Value: $100,000

Equal weighting across all assets

### Methodology:

Historical adjusted closing prices are retrieved and daily log returns are computed.

The mean return vector and covariance matrix of asset returns are estimated.

Portfolio expected return and volatility are derived based on equal weights.

10,000 Monte Carlo simulations are performed over a 90-day horizon using random draws from a standard normal distribution.

A distribution of simulated portfolio values is generated.

The 95% Value-at-Risk (VaR) and Expected Shortfall (ES) are calculated from the simulated profit & loss distribution.

The resulting gain/loss distribution is visualized to illustrate tail risk.

### Risk Metrics:

Value-at-Risk (95%): Estimated loss threshold not exceeded with 95% confidence.

Expected Shortfall (95%): Average loss conditional on losses exceeding the VaR threshold.

### Key Assumptions:

Asset returns follow a normal distribution

Historical covariance structure remains stable

No regime shifts or tail-risk modeling included
