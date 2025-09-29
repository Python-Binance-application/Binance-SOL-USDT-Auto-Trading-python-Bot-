# 🤖 Binance Trading Bot

Un bot di trading automatico per Binance che utilizza strategie basate su indicatori tecnici (EMA, ADX, RSI, ATR) con notifiche Telegram in tempo reale.

## 📋 Descrizione

Questo bot esegue operazioni di trading automatico su Binance Margin Trading utilizzando una strategia trend-following basata su:
- **EMA (Exponential Moving Average)**: Fast (7) e Slow (21)
- **ADX (Average Directional Index)**: Per misurare la forza del trend
- **ATR (Average True Range)**: Per calcolare stop loss dinamici
- **RSI (Relative Strength Index)**: Per identificare condizioni di ipercomprato/ipervenduto

### ⚙️ Caratteristiche principali

- ✅ Trading automatico su Binance Margin
- ✅ Gestione automatica dello stop loss con trailing
- ✅ Sistema di breakeven
- ✅ Notifiche Telegram in tempo reale
- ✅ Gestione del rischio e position sizing
- ✅ Supporto per operazioni LONG e SHORT
- ✅ Analisi tecnica su timeframe di 5 minuti

## 🚀 Installazione

### Prerequisiti

- Python 3.8 o superiore
- Account Binance con Margin Trading abilitato
- Bot Telegram (opzionale, per notifiche)

### Setup

1. **Clona il repository**
```bash
git clone https://github.com/tuo-username/binance-trading-bot.git
cd binance-trading-bot
```

2. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

3. **Configura le API Keys**

Modifica il file `config.py` e inserisci le tue credenziali:

```python
api_key = "LA_TUA_API_KEY_BINANCE"
api_secret = "LA_TUA_API_SECRET_BINANCE"

# Per notifiche Telegram
BOT_TOKEN = 'IL_TUO_BOT_TOKEN'
CHAT_ID = 'IL_TUO_CHAT_ID'
```

4. **Configura i parametri di trading**

Nel file `config.py` puoi modificare:
- `symbol`: coppia di trading (default: "SOLUSDT")
- `tf`: timeframe (default: 5 minuti)
- `esposizione`: percentuale del balance da utilizzare (default: 0.25 = 25%)
- `rischio`: percentuale di rischio per trade (default: 0.01 = 1%)

## 📊 Utilizzo

### Avvio del bot

```bash
python main.py
```

### Test delle operazioni

Per testare apertura e chiusura posizioni senza rischi:

```bash
python "Test Operazione.py"
```

### Modalità di funzionamento

Il bot opera in un loop continuo che:
1. Monitora il prezzo ogni secondo
2. Aggiorna i dati e gli indicatori ogni 5 minuti
3. Verifica le condizioni di entry/exit
4. Gestisce automaticamente stop loss e breakeven
5. Invia notifiche Telegram per ogni operazione

## 📈 Strategia di Trading

### Condizioni di Entry

**LONG**:
- EMA Fast > EMA Slow
- ADX > 30 (trend forte)

**SHORT**:
- EMA Fast < EMA Slow
- ADX > 30 (trend forte)

### Gestione del Rischio

- **Stop Loss**: Calcolato automaticamente usando ATR × 2.5
- **Position Sizing**: Basato su esposizione e rischio configurabili
- **Breakeven**: Attivato automaticamente quando il prezzo raggiunge un certo livello
- **Trailing Stop**: Modifica lo stop loss al raggiungimento del breakeven

### Condizioni di Exit

1. Stop loss raggiunto
2. Inversione del trend (basata su divergenza EMA)
3. Chiusura manuale

## 📁 Struttura del Progetto

```
├── main.py                 # File principale per avviare il bot
├── config.py              # Configurazioni e variabili globali
├── TakeData.py            # Gestione dati e calcolo indicatori
├── checkPosition.py       # Logica di entry/exit e monitoraggio posizioni
├── OpenClose.py           # Esecuzione ordini su Binance
├── calcoloLotti.py        # Calcolo position size
├── telegramBot.py         # Gestione notifiche Telegram
├── Test.py                # Script di test vari
└── Test Operazione.py     # Test apertura/chiusura posizioni
```

## ⚠️ Avvertenze

> **ATTENZIONE**: Questo bot opera con denaro reale. L'uso del margin trading comporta rischi significativi, inclusa la possibilità di perdere più del capitale investito.

- ⚠️ Testa sempre la strategia in un ambiente demo prima di usare denaro reale
- ⚠️ Non investire più di quanto puoi permetterti di perdere
- ⚠️ Monitora regolarmente le operazioni del bot
- ⚠️ Assicurati di comprendere i rischi del margin trading
- ⚠️ Le performance passate non garantiscono risultati futuri

## 🔒 Sicurezza

- Non condividere mai le tue API keys
- Usa API keys con permessi limitati (solo trading, no withdrawal)
- Abilita la whitelist IP su Binance
- Mantieni aggiornate le dipendenze per sicurezza

## 🛠️ Configurazione Avanzata

### Parametri Entry (in `checkPosition.py`)

```python
ADXSoglia = 30          # Soglia minima ADX per entry
RSIthresDWN = 30        # RSI oversold
RSIthresUP = 70         # RSI overbought
atrMultiplier = 2.5     # Moltiplicatore ATR per stop loss
```

### Parametri Exit Diff

```python
cont = 5                # Numero di candele da analizzare
max_diff = 3            # Soglia per exit su divergenza
```

## 🐛 Troubleshooting

### Errore di connessione a Binance
- Verifica le API keys
- Controlla la connessione internet
- Assicurati che l'IP sia whitelistato su Binance

### Ordini non eseguiti
- Verifica che il Margin Trading sia abilitato
- Controlla di avere fondi sufficienti
- Verifica i limiti minimi di ordine per la coppia

### Notifiche Telegram non funzionanti
- Verifica il BOT_TOKEN
- Controlla il CHAT_ID
- Assicurati di aver avviato una conversazione con il bot

## 📝 TODO / Miglioramenti Futuri

- [ ] Backtesting su dati storici
- [ ] Dashboard web per monitoraggio
- [ ] Supporto multi-symbol
- [ ] Stop loss trailing dinamico
- [ ] Gestione take profit multipli
- [ ] Logging avanzato
- [ ] Database per storico operazioni

## 🤝 Contribuire

Le pull request sono benvenute! Per modifiche importanti, apri prima un issue per discutere cosa vorresti cambiare.

## 📄 Licenza

[MIT](./MIT-License)

## 📧 Contatti

Per domande o supporto, apri un issue su GitHub.

---

**Disclaimer**: Questo software è fornito "così com'è", senza garanzie di alcun tipo. Gli autori non sono responsabili per eventuali perdite finanziarie derivanti dall'uso di questo bot.
