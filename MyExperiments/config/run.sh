#!/bin/bash

#telegram-send -g "Run Run_backtest.py"
#cd /runfolder || exit
# OUTPUT=$(python main_run.py); telegram-send -g "${OUTPUT}"

stdbuf -oL python script.py > OUTPUT

echo logout