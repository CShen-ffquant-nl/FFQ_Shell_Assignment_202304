import datetime
from pytest import  fail
import pytest
from src.pricer.pricer_Black76 import Pricer_Black76
import numpy as np

@pytest.fixture()
def setting():
  input={}
  input["spot"]=300
  input["strike"]=250
  input["maturity"]=datetime.date(2024,1,1)
  input["price_date"]=datetime.date(2023,1,1)
  input["vol"]=0.15
  input["rf"]=0.03
  input["call"]=58.81976813699321
  input["put"]= 1.4311515241202117
  input["future"]=input["spot"]*np.exp(input["rf"]*(input["maturity"]- input["price_date"]).days/365)
  return input

  

class Test_Black76:
    def test_Black76_PV(self,setting):
        try:
            black76=Pricer_Black76(setting["maturity"],setting["rf"],setting["strike"])
            call,put=black76.PV(setting["price_date"],setting["future"],setting["vol"])

            assert np.abs(call-setting["call"]) < 1e-6
            assert np.abs(put-setting["put"]) < 1e-6
            
        except Exception as e:
            fail(str(e))


    def test_Black76_Implied_Vol(self,setting):
        try:
            black76=Pricer_Black76(setting["maturity"],setting["rf"],setting["strike"])
            vol=black76.implied_vol(setting["price_date"],setting["future"],setting["put"],False)

            assert np.abs(vol-setting["vol"]) < 1e-6
            
        except Exception as e:
            fail(str(e))
