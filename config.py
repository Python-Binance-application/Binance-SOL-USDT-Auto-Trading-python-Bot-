from binance.client import Client
import checkPosition


symbol = "SOLUSDT"
tf=Client.KLINE_INTERVAL_5MINUTE
filename="solusdt.csv"
current_price = 0

balance = 0
esposizione = 0.25 #80%
rischio = 0.01 #1%

api_key = "la tua api"
api_secret = "la tua api"
client = 0

#verranno modificate durante l'esecuzione
stop_loss = -1
point_edit = -1
exit_diff_able = False
entry_price = 0
net_pos = 0


# buy o sell
azione = "BUY"
# minima quantità solo da acquistare
minimo_acquistabile = 0.05

#bot telegram
BOT_TOKEN = 'bot token di telegram'
CHAT_ID = 'id chat numerico'


def inizialize():
    reset_variabili_globali()
    get_connection_binance()
    update_balance()
    checkPosition.get_margin_position()

def reset_variabili_globali ():
    global stop_loss, point_edit, exit_diff_able, entry_price, net_pos
    stop_loss = -1
    point_edit = -1
    exit_diff_able = False
    entry_price = 0
    net_pos = 0
    
def get_connection_binance():
    global client
    client = Client(api_key, api_secret, requests_params={ 'timeout': 20 })



def update_balance():
    global balance
    # Ottieni informazioni sull'account margin
    margin_info = client.get_margin_account()

    # Estrai i dati relativi a USDT
    for asset in margin_info['userAssets']:
        free = float(asset['free'])
        if free > 0:
            aset = asset['asset']  #moneta
            borrowed = float(asset['borrowed']) # Presi a prestito
            interest = float(asset['interest']) # Interessi da pagare
            net = float(asset['netAsset'])      # Totale netto (free - borrowed)
            print(f"✅ {aset} disponibili: {free}")
            print(f"📌 Presi a prestito: {borrowed}")
            print(f"💰 Interessi: {interest}")
            print(f"📊 Totale netto: {net}")
            if aset == 'USDT':
                balance = round(free, 2)
        
async def scrivi_bot(data):
    bot = Bot(token=config.BOT_TOKEN)
    await bot.send_message(chat_id=config.CHAT_ID, text=data)
