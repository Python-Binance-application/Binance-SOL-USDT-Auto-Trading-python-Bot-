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

info = config.client.get_symbol_info(config.symbol)

for f in info['filters']:
    if f['filterType'] == 'PRICE_FILTER':
        print("Tick size:", f['tickSize'])
