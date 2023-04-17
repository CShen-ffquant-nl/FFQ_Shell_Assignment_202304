"""
Test class for src/pricer/pricer_BlackScholes.py
"""
import datetime
from pytest import fail
import pytest
from src.pricer.pricer_BlackScholes import Pricer_BS
import numpy as np


@pytest.fixture()
def setting():
    input = {}
    input["spot"] = 300
    input["strike"] = 250
    input["maturity"] = datetime.date(2024, 1, 1)
    input["price_date"] = datetime.date(2023, 1, 1)
    input["vol"] = 0.15
    input["rf"] = 0.03
    input["dividend"] = 0.02
    input["carry benefit"] = -0.01
    input["call"] = 56.0513371339575
    input["put"] = 1.6477703963341277
    # note: future price will includes dividend information
    # note: as long as diviend + carry benefit is same the option price is same.
    input["future"] = input["spot"] * np.exp((input["rf"] - input["dividend"]) * (input["maturity"] - input["price_date"]).days / 365)
    return input


class Test_Black76:
    def test_BS_PV_future(self, setting):
        try:
            black76 = Pricer_BS(setting["maturity"], setting["rf"], setting["strike"], setting["dividend"], setting["carry benefit"])
            call, put = black76.PV(setting["price_date"], setting["future"], setting["vol"], use_future=True)

            assert np.abs(call - setting["call"]) < 1e-6
            assert np.abs(put - setting["put"]) < 1e-6

        except Exception as e:
            fail(str(e))

    def test_BS_PV_spot(self, setting):
        try:
            black76 = Pricer_BS(setting["maturity"], setting["rf"], setting["strike"], setting["dividend"], setting["carry benefit"])
            call, put = black76.PV(setting["price_date"], setting["spot"], setting["vol"], use_future=False)

            assert np.abs(call - setting["call"]) < 1e-6
            assert np.abs(put - setting["put"]) < 1e-6

        except Exception as e:
            fail(str(e))

    def test_BS_Implied_Vol_future(self, setting):
        try:
            black76 = Pricer_BS(setting["maturity"], setting["rf"], setting["strike"], setting["dividend"], setting["carry benefit"])
            vol = black76.implied_vol(setting["price_date"], setting["future"], setting["put"], use_call=False, use_future=True)

            assert np.abs(vol - setting["vol"]) < 1e-6

        except Exception as e:
            fail(str(e))

    def test_BS_Implied_Vol_spot(self, setting):
        try:
            black76 = Pricer_BS(setting["maturity"], setting["rf"], setting["strike"], setting["dividend"], setting["carry benefit"])
            vol = black76.implied_vol(setting["price_date"], setting["spot"], setting["put"], use_call=False, use_future=False)

            assert np.abs(vol - setting["vol"]) < 1e-6

        except Exception as e:
            fail(str(e))
