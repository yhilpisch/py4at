import math
import sys
from unittest import TestCase

sys.path.append('/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments')

import pytest

from MyExperiments.Generating_test_Data import get_data_from_file
from MyExperiments.Three_commasDCA_safety_order_calc import SaftyOrder


class TestDataGeneration(TestCase):
    def test_get_data_from_file(self):

        data = get_data_from_file('2021-10-04', '2022-01-06', "Binance_BTCUSDT_1h_format.csv")
        lala = SaftyOrder(data, 0.01, math.inf)
        lala.get_signals()
        lala.plot_results()
        kwargs = {"start_base_size": 10,
                  "safety_order_size": 20,
                  "max_active_safety_trades_count": 10,  # uninteresting
                  "safety_order_volume_scale": 1.3,
                  "price_deviation": 1,
                  "max_safety_trades_count": 10,
                  "safety_order_step_scale": 1.3}
        result = lala.calc_times_for_each_signal(kwargs)
        self.assertEqual(result["Price_Exit"].iloc[-1], pytest.approx( 47848.14953, 0.1))  # add assertion here

