import datetime
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq,approx_fprime

class Pricer_Black76():
    def __init__(self,maturity_date:datetime,rf:float,strike:float ) -> None:
        self._maturity_date=maturity_date
        self._rf=rf
        self._strike=strike
        
        pass

    def PV(self,price_date:datetime,future:float, volality:float):
        
        t= (self._maturity_date- price_date).days/365 #act/365 with no holiday

        # Black76 model, use future price
        # https://en.wikipedia.org/wiki/Black_model
        d1= (np.log(future)-np.log(self._strike)+ (volality**2/2)*t)/(volality*np.sqrt(t))
        d2= d1-(volality*np.sqrt(t))

        call=np.exp(-self._rf*t)*(future*norm.cdf(d1)- self._strike*norm.cdf(d2))
        put= np.exp(-self._rf*t)*( self._strike*norm.cdf(-d2)-future *norm.cdf(-d1))                                                                                 
        
        return (call,put)

    def implied_vol(self,price_date:datetime,future:float, option:float,use_call:bool=True):

        #error function to minimize
        if use_call:
            err=lambda x: self.PV(price_date,future,x)[0]-option
        else:
            err=lambda x: self.PV(price_date,future,x)[1]-option

        # use bi-sec method
        # https://docs.scipy.org/doc/scipy/tutorial/optimize.html#root-finding
        implied_vol= brentq(err,0.01,100)
        
        return implied_vol
    
