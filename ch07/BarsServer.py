#
# Python Script to Serve
# Random Bars Data
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq  
import math
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5556')

while True:
    bars = [random.random() * 100 for _ in range(8)]  
    msg = ' '.join([f'{bar:.3f}' for bar in bars])  
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random() * 2)
