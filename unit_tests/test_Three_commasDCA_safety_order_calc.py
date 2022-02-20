import sys


sys.path.append('/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments')

from unittest import TestCase
import pytest
from parameterized import parameterized, parameterized_class
from MyExperiments.Generating_test_Data import generate_simpel_sample_momentum
from MyExperiments.Three_commasDCA_safety_order_calc import SaftyOrder


class TestSaftyOrder(TestCase):
    def setUp(self):
        self.chart_data = generate_simpel_sample_momentum()
        self.dca_bot = SaftyOrder(self.chart_data, 0.01)


    @parameterized.expand([
        [1.7, 1, 17, 1, 85.23193, 236335.78911],
        [1, 1, 5, 1, 98.21888, 110],
        [2, 1, 5, 1, 96.81728, 630],
        [2, 2, 5, 1, 92.66732, 630],
        [1.1, 1, 6, 1.1, 96.62711, 164.31220],
        [1.3, 2, 6, 1.1, 90.75307, 265.12060],
    ])
    def test_calc_times_for_each_signal(self, safety_order_volume_scale, price_deviation, max_safety_trades_count,
                                    safety_order_step_scale, expected_price_exit, expected_payed_sum):
        kwargs = {"start_base_size": 10,
                  "safety_order_size": 20,
                  "max_active_safety_trades_count": 10,  # uninteresting
                  "safety_order_volume_scale": safety_order_volume_scale,
                  "price_deviation": price_deviation,
                  "max_safety_trades_count": max_safety_trades_count,
                  "safety_order_step_scale": safety_order_step_scale}

        result = self.dca_bot.calc_times_for_each_signal(kwargs)
        self.assertEqual(result["Price_Exit"][0], pytest.approx(expected_price_exit, 0.001) )  # add assertion here
        self.assertEqual(result["Payed Deal Sum"].iloc[-1], pytest.approx(expected_payed_sum, 0.001) )
