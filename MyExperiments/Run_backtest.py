import numpy as np

from MyExperiments.DCA_bot import DCABot
from MyExperiments.Generating_test_Data import generate_simpel_sample_momentum
from Three_commasDCA_safety_order_calc import *


def real_data_test():
    data = get_data_from_file('2021-10-04', '2022-01-06', "Binance_BTCUSDT_minute.csv")
    lala = SaftyOrder(data, 0.01)
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
    print(result)
    print("End")


def fake_data_test():
    data = generate_simpel_sample_momentum()
    data["buy"][0] = np.nan
    data["buy"][100] = 1
    lala = SaftyOrder(data, 0.01)
    kwargs = {"start_base_size": 10,
              "safety_order_size": 20,
              "max_active_safety_trades_count": 10,  # uninteresting
              "safety_order_volume_scale": 1.1,
              "price_deviation": 1,
              "max_safety_trades_count": 10,
              "safety_order_step_scale": 1}
    result = lala.calc_times_for_each_signal(kwargs)
    print(result)
    print("End")

def backtest():
    data = get_data_from_file('2021-10-04', '2022-01-06', "Binance_BTCUSDT_1h_format.csv")
    btc_test = DCABot(data, 0.01)
    btc_test.get_signals()
    kwargs = {"start_base_size": 10,
              "safety_order_size": 20,
              "max_active_safety_trades_count": 10,  # uninteresting
              "safety_order_volume_scale": 1.3,
              "price_deviation": 1,
              "max_safety_trades_count": 10,
              "safety_order_step_scale": 1.3}
    result = btc_test.calc_times_for_each_signal(kwargs)
    # btc_test.plot_results()
    print(result)
    print("End")

if __name__ == '__main__':
    # real_data_test()
    # fake_data_test()
    backtest()
