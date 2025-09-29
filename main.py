# IMPORT LIBRERIE
import numpy as np
import matplotlib.pyplot as plt
import ta
from datetime import datetime, timedelta, UTC
import os
import time
from decimal import Decimal, ROUND_DOWN
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from pprint import pprint
import pandas as pd
import TakeData
import config
import calcoloLotti
import OpenClose
import checkPosition


config.inizialize();

while True:
    now = datetime.now(UTC)
    #prendere i dati continuamente
    if now.minute % 5 == 0  and (now.second > 1 and now.second < 6):
        TakeData.update_data_5M()
    config.current_price = TakeData.get_current_price()
    print(f"Current Price solusdt: {config.current_price}")
    
    time.sleep (1)
        
    
