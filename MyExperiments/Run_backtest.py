import os
import time
from pathlib import Path

from MyExperiments.Generating_test_Data import get_data_from_file
from MyExperiments.DCA_bot import DCABot
from MyExperiments.telegramBot import send_message as tb_print


def back_overfitting(start_date, end_date, file_name):
    data = get_data_from_file(start_date, end_date, file_name)
    # data = generate_simpel_sample_momentum()
    btc_test = DCABot(data, profit_percent, capital_deal_limit)
    btc_test.get_signals_general()

    if btc_test.signal_amount == 0:
        tb_print("No Signals")
        return

    # args
    start_base_size = 100
    safety_order_size = 20
    max_active_safety_trades_count = 10  # uninteresting
    safety_order_volume_scale = (1, 2.1, .1)
    price_deviation = (1, 2, .1)
    max_safety_trades_count = (1, 19, 1)
    safety_order_step_scale = (1, 1.2, .05)

    fix_params = (start_base_size, safety_order_size, max_active_safety_trades_count)
    rranges = (safety_order_volume_scale, price_deviation, max_safety_trades_count, safety_order_step_scale)

    tb_print("coin: " + file_name)
    result = btc_test.optimize_parameters(rranges, fix_params)
    tb_print(str(result))
    return result


def check_back_overfitting(start_date, end_date, file_name):
    data = get_data_from_file(start_date, end_date, file_name)
    # data = Three_commasDCA_safety_order_calc.generate_simpel_sample_momentum()
    btc_test = DCABot(data, profit_percent, capital_deal_limit)
    btc_test.get_signals_general()

    if btc_test.signal_amount == 0:
        tb_print("No Signals")
        return

    result = btc_test.calc_times_for_each_signal(overfitting_kwargs)

    tb_print("coin: " + file_name)
    tb_print("Profit Total: " + str(result["Profit"].sum()))
    tb_print("uPNL Total: " + str(result["uPNL"].sum()))
    tb_print("duration longest: " + str(result["duration"].max()))
    tb_print("max safety trades: " + str(result["max_safety_trades_counter"].max()))
    tb_print("Deals Total: " + str(len(result)))
    return result


overfitting_kwargs = {"start_base_size": 10,
                      "safety_order_size": 20,
                      "max_active_safety_trades_count": 10,  # uninteresting
                      "safety_order_volume_scale": 1.9,
                      "price_deviation": 1.8,
                      "max_safety_trades_count": 4,
                      "safety_order_step_scale": 1.}
profit_percent = 0.01
capital_deal_limit = 700


def run_backtesting_main():
    #debug
    t = time.process_time()
    start = time.time()

    date_periods = ('2021-10-04', '2022-02-13')
    tb_print("Date period: start {start} : end {end}".format(start=date_periods[0], end=date_periods[1]))
    tb_print("args" + str(overfitting_kwargs))
    tb_print("---###---####----START----####---###---", flush=True)

    for path in Path(os.getcwd() + '/MyExperiments/historyCryptoData/').glob("*.csv"):
        try:
            #r = back_overfitting(*date_periods, path.name)
            r = check_back_overfitting(*date_periods, path.name)
        except:
            tb_print("Error")
            raise
        finally:
            end = time.time()
            elapsed_time = time.process_time() - t
            tb_print("elapsed time: " + str(end - start) + " : hour " + str(elapsed_time) + "\n" +
                     "---------------####---------------", flush=True)

    end = time.time()
    elapsed_time = time.process_time() - t
    tb_print("Total elapsed time: " + str(end - start) + " : hour " + str(elapsed_time), flush=True)
