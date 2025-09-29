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
    if now.minute % 2 == 0 and (now.second > 0 and now.second < 5):
        TakeData.update_data_5M()
    config.current_price = TakeData.get_current_price()
    #apertura e chiusura operazioni
    if now.minute == 14 and now.second > 0 and now.second < 5 and config.net_pos == 0:
        config.stop_loss = config.current_price + 10
        calcoloLotti.get_size()
        OpenClose.apri_operazione("SELL")
    if now.minute == 15 and now.second > 0 and now.second < 5 and config.net_pos != 0:
        config.stop_loss = config.current_price + 40
        OpenClose.gestire_limit("EDIT")
    if now.minute == 16 and now.second > 0 and now.second < 5 and config.net_pos != 0:
        OpenClose.chiudi_posizione()
    print(f"Current Price solusdt: {config.current_price}")
    time.sleep (1)
        
    
