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
import OpenClose
import config
import calcoloLotti

#Variabili Globali per entry
ADXSoglia = 30
RSIthresDWN = 30
RSIthresUP = 70
atrMultiplier = 2.5

cont = 5
max_diff = 3

def check_entry(df_all):
    #print("Check Entry")
    if config.net_pos != 0:
        return  # Nessuna posizione aperta
    last_candle = df_all.iloc[-1]
    ConditionEntryLong = last_candle['Ema_fast'] > last_candle['Ema_slow'] and last_candle['Adx'] > ADXSoglia
    ConditionEntryShort = last_candle['Ema_fast'] < last_candle['Ema_slow'] and last_candle['Adx'] > ADXSoglia
    
    stop_loss_long = config.current_price - (last_candle['Atr'] * atrMultiplier)
    stop_loss_short = config.current_price + (last_candle['Atr'] * atrMultiplier)
    
    check = exit_diff(df_all)
    
    if (ConditionEntryLong and check!= 1):
        config.stop_loss = stop_loss_long
        config.point_edit =  stop_loss_short
        config.entry_price = config.current_price
        calcoloLotti.get_size()
        OpenClose.apri_operazione("BUY")
    if (ConditionEntryShort and check!= 2):
        config.stop_loss = stop_loss_short
        config.point_edit =  stop_loss_long
        config.entry_price = config.current_price
        calcoloLotti.get_size()
        OpenClose.apri_operazione("SHORT")
        


        
def exit_atr():
    get_margin_position()

    if config.net_pos == 0:
        return  # Nessuna posizione aperta

    price = config.current_price
    sl = config.stop_loss
    point = config.point_edit
    entry = config.entry_price

    # LONG
    if config.net_pos > 0:
        if price <= sl:
            OpenClose.chiudi_posizione()
            return
        
        # Break-even trigger
        if price >= point and sl < entry:
            config.stop_loss = entry
            OpenClose.gestire_limit("EDIT")
            config.exit_diff_able = True

    # SHORT
    elif config.net_pos < 0:
        if price >= sl:
            OpenClose.chiudi_posizione()
            return

        # Break-even trigger
        if price <= point and sl > entry:
            config.stop_loss = entry
            OpenClose.gestire_limit("EDIT")
            config.exit_diff_able = True


#deve essere controllato ogni candela chiusa
def exit_diff(df_all):
    global cont, max_diff
    if config.net_pos == 0:
        return  # Nessuna posizione aperta

    num = 0


    # ciclo da 1 a cont (esclusivo range va fino a cont-1 perché accediamo a [i+1])
    for i in range(1, cont):
        if df_all['Ema_fast'].iloc[-(i)] < df_all['Ema_fast'].iloc[-(i + 1)]:
            num += 1
            
    if config.net_pos > 0 and num >= max_diff:
        print("📉 Chiudo LONG con SELL...")
        OpenClose.chiudi_posizione()
        return 1

    elif config.net_pos < 0 and num < max_diff:
        print("📈 Chiudo SHORT con BUY...")
        OpenClose.chiudi_posizione()
        return 2
    return 0
 
 
 

# >>> 4) Funzione per ottenere posizione aperta su margin account
def get_margin_position():
    config.net_pos = 0
    info = config.client.get_margin_account()
    for asset in info['userAssets']:
        if asset['asset'] == config.symbol.replace("USDT",""):
            borrowed = float(asset['borrowed'])
            net = float(asset['netAsset'])
            free = float(asset['free'])
            if abs(net) < 1e-6:
                config.net_pos = 0
            else:
                config.net_pos = net

        
    



