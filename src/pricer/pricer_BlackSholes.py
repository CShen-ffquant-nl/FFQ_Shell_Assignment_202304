"""
Option Pricer engine based on Black 76 model
reference: https://en.wikipedia.org/wiki/Black_model
Note: BlackScholes model, use spot price with dividend included

"""
import datetime
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq


class Pricer_BS:
    '''
    init model with contract paramters and calibrated values
    '''
    def __init__(self, maturity_date: datetime, rf: float, strike: float,dividend:float=0) -> None:

        self._maturity_date = maturity_date
        self._rf = rf
        self._strike = strike
        self._dividend=dividend


    '''
    return both call and put option present value based on price(as-of) date,  spot price and (implied) volatility
    '''
    def PV(self, price_date: datetime, spot: float, volality: float):

        t = (self._maturity_date - price_date).days / 365  # act/365 with no holiday

        d1 = (np.log(spot/self._strike) + t*(self._rf - self._dividend + volality**2 / 2))  / (volality * np.sqrt(t))
        d2 = d1 - (volality * np.sqrt(t))

        call = spot*np.exp(-self._dividend * t) * norm.cdf(d1) - self._strike * np.exp(-self._rf * t) *norm.cdf(d2)
        put = self._strike *np.exp(-self._rf * t) *  norm.cdf(-d2) - np.exp(-self._dividend * t) *spot *  norm.cdf(-d1)

        return (call, put)

    '''
    return implied volality from either call or put option based on price(as-of) date,  spot price and market price of option
    '''
    def implied_vol(self, price_date: datetime, future: float, option: float, use_call: bool = True):

        # error function to minimize
        if use_call:
            err = lambda x: self.PV(price_date, future, x)[0] - option
        else:
            err = lambda x: self.PV(price_date, future, x)[1] - option

        # use bi-sec method. 
        # NOTE the upper limit is set to 100. may need adjust when used for cryto currency :D
        # https://docs.scipy.org/doc/scipy/tutorial/optimize.html#root-finding
        implied_vol = brentq(err, 0.01, 100)

        return implied_vol
