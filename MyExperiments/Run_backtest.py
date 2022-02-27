import os
import time
from pathlib import Path

from MyExperiments.Generating_test_Data import get_data_from_file
from MyExperiments import Three_commasDCA_safety_order_calc
from MyExperiments.DCA_bot import DCABot
from MyExperiments.telegramBot import send_message as tb_print

def backtest():
    data = Three_commasDCA_safety_order_calc.get_data_from_file('2019-03-04', '2022-01-06',
                                                                "Binance_BTCUSDT_1h_format.csv")
    btc_test = DCABot(data, profit_percent)
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
    return result


def back_overfitting():
    data = Three_commasDCA_safety_order_calc.get_data_from_file('2019-02-04', '2022-02-13',
                                                                "Binance_BTCUSDT_1h_format.csv")
    # data = generate_simpel_sample_momentum()
    btc_test = DCABot(data, profit_percent, capital_deal_limit)
    btc_test.get_signals()
    # args

    start_base_size = 100
    safety_order_size = 20
    max_active_safety_trades_count = 10  # uninteresting
    safety_order_volume_scale = (1, 1.8, .1)
    price_deviation = (1, 2, .1)
    max_safety_trades_count = (1, 25, 1)
    safety_order_step_scale = (1, 1.2, .05)

    fix_params = (start_base_size, safety_order_size, max_active_safety_trades_count)
    rranges = (safety_order_volume_scale, price_deviation, max_safety_trades_count, safety_order_step_scale)

    result = btc_test.optimize_parameters(rranges, fix_params)
    return result


def check_back_overfitting(file_name):
    data = get_data_from_file('2019-02-04', '2022-02-13', file_name)
    # data = Three_commasDCA_safety_order_calc.generate_simpel_sample_momentum()
    btc_test = DCABot(data, profit_percent, capital_deal_limit)
    btc_test.get_signals_general()
    kwargs = {"start_base_size": 10,
              "safety_order_size": 20,
              "max_active_safety_trades_count": 10,  # uninteresting
              "safety_order_volume_scale": 1.4,
              "price_deviation": 1.4,
              "max_safety_trades_count": 9,
              "safety_order_step_scale": 1.}
    result = btc_test.calc_times_for_each_signal(kwargs)
    tb_print("coin: " + file_name)
    tb_print("Profit Total: " + str(result["Profit"].sum()))
    tb_print("uPNL Total: " + str(result["uPNL"].sum()))
    tb_print("duration longest: " + str(result["duration"].max()))
    tb_print("max safety trades: " + str(result["max_safety_trades_counter"].max()))
    tb_print("Deals Total: " + str(len(result)))
    return result


profit_percent = 0.01
capital_deal_limit = 1100


def run_backtesting_main():
    t = time.process_time()
    start = time.time()

    for path in Path(os.getcwd() + '/MyExperiments/historyCryptoData/').glob("*.csv"):
        try:
            tb_print("Calculating...")
            #r = back_overfitting()
            r = check_back_overfitting(path.name)
            #tb_print(r)
        except:
            tb_print("Error")
            raise
        finally:
            end = time.time()
            elapsed_time = time.process_time() - t
            tb_print("elapsed time: " + str(end - start) + " : hour " + str(elapsed_time))
            tb_print("-------------------------------------------------------------------------")

    end = time.time()
    elapsed_time = time.process_time() - t
    tb_print("Total elapsed time: " + str(end - start) + " : hour " + str(elapsed_time))
