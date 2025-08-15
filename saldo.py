import os
import time
import requests
from binance.client import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
INTERVALO_SEGUNDOS = 3600  # cada hora

# Conexión a Binance
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def obtener_saldo_en_eur():
    balances = client.get_account()['balances']
    resumen = []
    total_eur = 0.0

    for b in balances:
        asset = b['asset']
        free = float(b['free'])
        locked = float(b['locked'])
        cantidad = free + locked

        if cantidad > 0 and asset != "EUR":
            try:
                # Intentar par directo a EUR
                precio = client.get_symbol_ticker(symbol=f"{asset}EUR")['price']
            except:
                try:
                    # Si no hay par EUR, pasar a USDT y luego a EUR
                    precio_usdt = float(client.get_symbol_ticker(symbol=f"{asset}USDT")['price'])
                    precio_eur = float(client.get_symbol_ticker(symbol="EURUSDT")['price'])
                    precio = precio_usdt / precio_eur
                except:
                    continue

            valor_eur = cantidad * float(precio)
            total_eur += valor_eur
            resumen.append(f"{asset}: {cantidad:.6f} ≈ {valor_eur:.2f} €")

    resumen.append(f"\nTOTAL: {total_eur:.2f} €")
    return "\n".join(resumen)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})

if __name__ == "__main__":
    while True:
        try:
            mensaje = obtener_saldo_en_eur()
            enviar_telegram(mensaje)
            print("Mensaje enviado a Telegram")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(INTERVALO_SEGUNDOS)
