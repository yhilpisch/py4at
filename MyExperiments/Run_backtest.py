import numpy as np

from MyExperiments.DCA_bot import DCABot
from MyExperiments.Generating_test_Data import generate_simpel_sample_momentum
from Three_commasDCA_safety_order_calc import *
from scipy.optimize import brute
import matplotlib.pyplot as plt

def save_settings():
    start_base_size = 10
    safety_order_size = (10, 50)
    max_active_safety_trades_count = 10  # uninteresting
    safety_order_volume_scale = (1, 1.5)
    price_deviation = (1, 10)
    max_safety_trades_count = (1, 100)
    safety_order_step_scale = (1, 1.5)

    fix_params = (start_base_size, max_active_safety_trades_count)
    rranges = (safety_order_size, safety_order_volume_scale,
            price_deviation, max_safety_trades_count, safety_order_step_scale)
    # result = btc_test.optimize_parameters(rranges, fix_params)


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
    lala = SaftyOrder(data, 0.01)
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


def backtest():
    data = get_data_from_file('2019-03-04', '2022-01-06', "Binance_BTCUSDT_1h_format.csv")
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
    result["sum_profit"] = result["Profit"].cumsum()
    win = result['Profit'].iloc[-1] - result["uPNL"].cumsum().iloc[-1]
    print(result)
    print("End")


def back_overfitting():
    data = get_data_from_file('2021-03-04', '2022-01-06', "Binance_BTCUSDT_1h_format.csv")
    #data = generate_simpel_sample_momentum()
    btc_test = DCABot(data, 0.01)
    btc_test.get_signals()
    # args

    start_base_size = 10
    safety_order_size = 20
    max_active_safety_trades_count = 10  # uninteresting
    safety_order_volume_scale = (1, 1.5, .1)
    price_deviation = (1, 2, .1)
    max_safety_trades_count = (1, 15, 1)
    safety_order_step_scale = (1, 1.5, .1)

    fix_params = (start_base_size, safety_order_size, max_active_safety_trades_count)
    rranges = (safety_order_volume_scale, price_deviation, max_safety_trades_count, safety_order_step_scale)

    result = btc_test.optimize_parameters(rranges, fix_params)
    print(result)
    print("end")


def test_back_overfitting():
    data = get_data_from_file('2021-03-04', '2022-01-06', "Binance_BTCUSDT_1h_format.csv")
    #data = generate_simpel_sample_momentum()
    btc_test = DCABot(data, 0.01)
    btc_test.get_signals()
    kwargs = {"start_base_size": 10,
              "safety_order_size": 20,
              "max_active_safety_trades_count": 10,  # uninteresting
              "safety_order_volume_scale": 1.4,
              "price_deviation": 1.8,
              "max_safety_trades_count": 13,
              "safety_order_step_scale": 1}
    result = btc_test.calc_times_for_each_signal(kwargs)
    print("Profit Total: " + str(result["Profit"].sum()))
    print("Deals Total: " + str(len(result)))
    print("End")


if __name__ == '__main__':
    try:
        # fake_data_test()
        # real_data_test()
        # backtest()
        #back_overfitting()
        test_back_overfitting()
    except:
        print("Error")
        raise

