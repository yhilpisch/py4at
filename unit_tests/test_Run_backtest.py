from unittest import TestCase
import pytest
from numpy import array
from parameterized import parameterized, parameterized_class
from MyExperiments.Generating_test_Data import generate_simpel_sample_momentum
from MyExperiments.Three_commasDCA_safety_order_calc import SaftyOrder
from MyExperiments import Three_commasDCA_safety_order_calc
from MyExperiments.DCA_bot import DCABot


class TestRunner(TestCase):
    def setUp(self):
        self.real_chart_data = Three_commasDCA_safety_order_calc.get_data_from_file('2021-10-04', '2022-02-13',                                                                "Binance_BTCUSDT_1h_format.csv")
        self.real_data_dca_bot = DCABot(self.real_chart_data, 0.01)
        self.real_data_dca_bot.get_signals()

        self.chart_data = generate_simpel_sample_momentum()
        self.test_dca_bot = DCABot(self.chart_data, 0.01)

    @parameterized.expand([
        [(1, 2, 1), (1, 2, 1), (1, 3, 1), (1, 2, 1), [1, 1, 1, 1], -28.82976],
        [(1, 1.1, .1), (1, 1.2, .1), (1, 5, 1), (1, 1.2, .1), [1.1, 1.1, 1.0, 1.0], -28.25342],
    ])
    def test_real_back_overfitting(self, safety_order_volume_scale, price_deviation, max_safety_trades_count,
                              safety_order_step_scale, expected_result, expected_amount):
        start_base_size = 10
        safety_order_size = 20
        max_active_safety_trades_count = 10  # uninteresting

        fix_params = (start_base_size, safety_order_size, max_active_safety_trades_count)
        rranges = (safety_order_volume_scale, price_deviation, max_safety_trades_count, safety_order_step_scale)

        result = self.real_data_dca_bot.optimize_parameters(rranges, fix_params)
        (np_array, amount) = result
        self.assertEqual(np_array.tolist(), expected_result)
        self.assertEqual(amount, pytest.approx(expected_amount, 0.01))


    @parameterized.expand([
        [(1, 2, 1), (1, 2, 1), (1, 3, 1), (1, 2, 1), [1, 1, 2, 1], 0.5],
        [(1, 1.1, .1), (1, 1.2, .1), (1, 5, 1), (1, 1.2, .1), [1.1, 1, 4, 1], 1.12102],
    ])
    def test_fake_back_overfitting(self, safety_order_volume_scale, price_deviation, max_safety_trades_count,
                              safety_order_step_scale, expected_result, expected_amount):
        start_base_size = 10
        safety_order_size = 20
        max_active_safety_trades_count = 10  # uninteresting

        fix_params = (start_base_size, safety_order_size, max_active_safety_trades_count)
        rranges = (safety_order_volume_scale, price_deviation, max_safety_trades_count, safety_order_step_scale)

        result = self.test_dca_bot.optimize_parameters(rranges, fix_params)
        (np_array, amount) = result
        self.assertEqual(np_array.tolist(), expected_result)
        self.assertEqual(amount, pytest.approx(expected_amount, 0.01))