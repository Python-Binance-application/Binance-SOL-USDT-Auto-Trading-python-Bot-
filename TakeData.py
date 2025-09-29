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
import checkPosition
import config
import OpenClose
from telegramBot import bot_telegram



def get_current_price():
    try:
        ticker = config.client.get_symbol_ticker(symbol = config.symbol)
        price = float (ticker['price'])
        if(config.net_pos != 0):
            print("controllo se point o stop raggiunti")
            checkPosition.exit_atr()
            # Breakeven logic
        return price
    except Exception as e:
        print("Timeout. Riprovo...")
        time.sleep(5)
        return get_current_price()
    

def get_df_update(df_new, df_all):
        # Calcolo solo su righe nuove
        df_new['Ema_fast'] = ta.trend.EMAIndicator(close=df_all['Close'], window=7).ema_indicator().loc[df_new.index].round(2)
        df_new['Ema_slow'] = ta.trend.EMAIndicator(close=df_all['Close'], window=21).ema_indicator().loc[df_new.index].round(2)
        df_new['Rsi'] = ta.momentum.RSIIndicator(close=df_all['Close'], window=14).rsi().loc[df_new.index].round(2)
        df_new['Atr'] = ta.volatility.AverageTrueRange(
            high=df_all['High'], low=df_all['Low'], close=df_all['Close'], window=14
        ).average_true_range().loc[df_new.index].round(2)
        df_new['Adx'] = ta.trend.ADXIndicator(
            high=df_all['High'], low=df_all['Low'], close=df_all['Close'], window=30
        ).adx().loc[df_new.index].round(2)
        df_all.update(df_new)
        return df_all


def update_data_5M():
    # Carica i dati esistenti (se esiste)
    try:
        df_old = pd.read_csv(config.filename, parse_dates=['Timestamp'], index_col='Timestamp')
    except FileNotFoundError:
        df_old = pd.DataFrame()
        
    # Calcola timestamp dell'ultima candela salvata
    if not df_old.empty:
        start_dt = df_old.index[-2]
    else:
        start_dt = datetime.utcnow() - timedelta(days=1)

    # Scarica nuove candele da quel punto fino a ora
    end_dt = datetime.utcnow()
    try:
        klines = config.client.get_historical_klines(
            config.symbol,
            config.tf,
            start_str=start_dt.strftime("%d %b %Y %H:%M:%S"),
            end_str=end_dt.strftime("%d %b %Y %H:%M:%S")  # <-- AGGIUNGI SPAZIO QUI
            )
    except Exception as e:
        print("Presa Dati Errore")
    if not klines:
        print("Nessun nuovo dato da aggiornare.")
        return

    # Nuovo DataFrame
    df_new = pd.DataFrame(klines, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume',
                                           'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])

    df_new['Timestamp'] = pd.to_datetime(df_new['Timestamp'], unit='ms')
    df_new.set_index('Timestamp', inplace=True)
    df_new = df_new.drop(['close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'], axis=1)
    df_new = df_new.astype('float64')
    
    
    # Unisci i due DataFrame ed elimina eventuali duplicati
    df_all = pd.concat([df_old, df_new])
    df_all = df_all[~df_all.index.duplicated(keep='last')]
    # Se è la prima volta, calcola su tutto
    if df_old.empty:
        df_all = get_df_update(df_all, df_all)
    else:
        df_all = get_df_update(df_new, df_all)
        
    df_all = df_all.iloc[-250:]
    df_all.dropna(inplace=True)
    
    # controlliamo se è condizione di entry
    checkPosition.get_margin_position()
    window = df_all.iloc[-7: -1]
    if  config.net_pos == 0:
        bot_telegram("Check se devo entrare")
        checkPosition.check_entry(window)

    else:
        print("Check se dobbiamo uscire")
        checkPosition.exit_diff(window)
    
    try:
        df_all.to_csv(config.filename, index=True)
        data = f"Dati aggiornati fino a {df_all.index[-1]}"
        bot_telegram(data)
    except Exception as e:
        print(f"Errore nel salvataggio CSV: {e}")
    

    
