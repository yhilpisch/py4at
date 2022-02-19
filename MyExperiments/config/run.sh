#!/bin/bash

telegram-send -g "Run Run_backtest.py"
OUTPUT=$(python /runfolder/MyExperiments/Run_backtest.py); telegram-send -g "${OUTPUT}"
shutdown
