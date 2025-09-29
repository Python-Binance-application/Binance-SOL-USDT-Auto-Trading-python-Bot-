from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, ORDER_TYPE_STOP_LOSS_LIMIT, TIME_IN_FORCE_GTC
from pprint import pprint
import config
import checkPosition
import time
from telegramBot import bot_telegram

def get_side_enum(side_str):
    if side_str.upper() == "BUY":
        return SIDE_BUY
    elif side_str.upper() == "SELL":
        return SIDE_SELL
    else:
        raise ValueError("Valore 'side' non valido: usa 'BUY' o 'SELL'")


#aprire operazioni LONG-SHORT
def apri_operazione(azione):

    data = f"\n📘 Posizione netta su {config.symbol}: {config.net_pos}"
    bot_telegram(data)
    
    data = f"\n🟢 Apro LONG su {config.symbol} con {config.net_pos} lotti..."
    bot_telegram(data)
    
    if config.net_pos != 0:
        ordine = config.client.create_margin_order(
            symbol=config.symbol,
            side=get_side_enum(azione),
            type=ORDER_TYPE_MARKET,
            quantity=config.net_pos,
            isIsolated='FALSE',
            sideEffectType='MARGIN_BUY'
        )
        time.sleep(1)
        config.azione = azione
        time.sleep(5)
        gestire_limit("ADD")
        pprint(ordine)
    else:
        data = "⚠️ Impossibile aprire ordine: posizione nulla"
        bot_telegram(data)

def trova_ordine_limit():
    orders = config.client.get_open_margin_orders(symbol=config.symbol, isIsolated='FALSE')
    for order in orders:
        if order['type'] == 'STOP_LOSS_LIMIT':
            return order
    return None



# Piazzare uno stop loss come ordine LIMIT
def gestire_limit(order_action):
    if order_action == "ADD":
        if config.azione.upper() == "BUY":
            side = SIDE_SELL  # chiude long
            pips = abs(config.current_price - config.stop_loss) * 2
            stop_price = round(config.stop_loss - pips, 2)
        else:
            side = SIDE_BUY  # chiude short
            pips = abs(config.current_price - config.stop_loss)  * 2
            stop_price = round(config.stop_loss + pips, 2)
        #checkPosition.get_margin_position()
        data = f"\n📘 Posizione netta su {config.symbol}: {config.net_pos}"
        bot_telegram(data)
        
        try:
            if config.net_pos != 0:
                data = f"⛔️ Imposto STOP LOSS: stop trigger a {stop_price}, limite a {config.stop_loss} , quantita : {config.net_pos}"
                bot_telegram(data)
                order = config.client.create_margin_order(
                    symbol=config.symbol,
                    side=side,
                    type=ORDER_TYPE_STOP_LOSS_LIMIT,
                    quantity=round(abs(config.net_pos), 2),
                    price=str(round(stop_price, 3)),      # Appena toccato viene submesso l'ordine
                    stopPrice=str(round(config.stop_loss, 3)),  # fino a quando non supera questo livello è sempre nel book
                    timeInForce=TIME_IN_FORCE_GTC,
                    isIsolated='FALSE',
                    sideEffectType='AUTO_REPAY'
                )
                pprint(order)
            else:
                data = "⚠️ Nessuna posizione aperta, impossibile impostare lo stop loss."
                bot_telegram(data)
        except Exception as e:
            data = f"❌ Errore durante l'apertura margin': {e}"
            bot_telegram(data)

    elif order_action == "EDIT":
        data = "Vado a modificare lo stop losss"
        bot_telegram(data)
        
        check = gestire_limit("CANCEL")
        time.sleep(1)
        if check:
            
            gestire_limit("ADD")
                
                
    elif order_action == "CANCEL":
        try:
            data = "elimino l'ordine limit che trovo"
            bot_telegram(data)
            
            order = trova_ordine_limit()
            if order:
                result = config.client.cancel_margin_order(symbol=config.symbol, orderId=order['orderId'], isIsolated='FALSE')
                data = f"🗑️ Ordine LIMIT cancellato: ID={order['orderId']}"
                bot_telegram(data)
                return True
            else:
                data = "Non ho trovato ordine limit"
                bot_telegram(data)
                
                return False
        except Exception as e:
            data = f"❌ Errore durante la cancellazione: {e}"
            bot_telegram(data)
            
    
        

#chiudere operazioni
def chiudi_posizione():
    gestire_limit("CANCEL")
    time.sleep(1)
    checkPosition.get_margin_position()
    
    data = f"\n📘 Posizione netta su {config.symbol}: {config.net_pos}"
    bot_telegram(data)
    try:
        if config.net_pos > 0 :
            data = "📉 Chiudo LONG con SELL..."
            bot_telegram(data)
            
            ordine = config.client.create_margin_order(
                symbol=config.symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=abs(config.net_pos),
                isIsolated='FALSE',
                sideEffectType='AUTO_REPAY'
            )
            pprint(ordine)
        elif config.net_pos < 0:
            data = "📈 Chiudo SHORT con BUY..."
            bot_telegram(data)
            
            ordine = config.client.create_margin_order(
                symbol=config.symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=abs(config.net_pos),
                isIsolated='FALSE',
                sideEffectType='AUTO_REPAY'
            )
            pprint(ordine)
        
        else:
            data = "⚠️ Nessuna posizione aperta da chiudere."
            bot_telegram(data)
        config.net_pos = 0
        config.update_balance()
    
    except Exception as e:
        data = f"❌ Errore durante la chiusura delle posizioni: {e}"
        bot_telegram(data)


