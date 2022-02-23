import math
import sys

import Three_commasDCA_safety_order_calc

sys.path.append('/Users/hans/Documents/Github/GiannisTraidingReserching/MyExperiments')

from unittest import TestCase
import pytest
from parameterized import parameterized, parameterized_class
from MyExperiments.Generating_test_Data import generate_simpel_sample_momentum
from MyExperiments.Three_commasDCA_safety_order_calc import SaftyOrder
from MyExperiments.DCA_bot import DCABot


class TestDCABotLimitReal(TestCase):
    def setUp(self):
        self.real_chart_data = Three_commasDCA_safety_order_calc.get_data_from_file('2021-10-04', '2022-02-13',
                                                                                    "Binance_BTCUSDT_1h_format.csv")
        self.real_data_dca_bot = DCABot(self.real_chart_data, 0.01, 2000)
        self.real_data_dca_bot.get_signals()

    @parameterized.expand([
        [1.1, 1, 18, 1, 32.5573, -18.8991],
        [1., 1, 35, 1.1, 18.9, -370.861],
    ])
    def test_calc_times_for_each_signal(self, safety_order_volume_scale, price_deviation, max_safety_trades_count,
                                        safety_order_step_scale, revenue, profit):
        kwargs = {"start_base_size": 10,
                  "safety_order_size": 20,
                  "max_active_safety_trades_count": 10,  # uninteresting
                  "safety_order_volume_scale": safety_order_volume_scale,
                  "price_deviation": price_deviation,
                  "max_safety_trades_count": max_safety_trades_count,
                  "safety_order_step_scale": safety_order_step_scale}

        result = self.real_data_dca_bot.calc_times_for_each_signal(kwargs)

        r_revenue = result["Profit"].sum()
        r_profit = result['Profit'].sum() - result["uPNL"].sum()
        self.assertEqual(r_revenue, pytest.approx(revenue, 0.001))  # add assertion here
        self.assertEqual(r_profit, pytest.approx(profit, 0.001))
