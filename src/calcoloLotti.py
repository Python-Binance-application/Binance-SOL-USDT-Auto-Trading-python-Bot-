# IMPORT LIBRERIE
import matplotlib.pyplot as plt
import ta
import os
from binance.client import Client
from pprint import pprint
import config
import checkPosition

def get_size():
    min_acquistabile = round (10 /config.current_price,2)
    esp = size_esposizione()
    rischio = size_rischio()
    print(f"stopLoss : {config.stop_loss}\n")
    print(f"entryprice: {config.current_price}\n")
    print(f"sizeEsposizione: {esp}\nsizeRischio:{rischio} con balance {config.balance}")
    config.net_pos = min(size_esposizione(), size_rischio())
    if (config.net_pos <= min_acquistabile): # dollari è il minimo acquistabile
        config.net_pos = min_acquistabile
    
    
    
    
    
    
def size_esposizione():
    return round(config.balance * config.esposizione / config.current_price,2)
        
    
def size_rischio():
    pips = abs(config.stop_loss - config.current_price)
    return round((config.balance * config.rischio)/pips,2)
    
