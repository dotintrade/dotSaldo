import os
import time
from binance.client import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

INTERVALO_SEGUNDOS = 10

# Conexión a Binance
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

print("Conectado a Binance")

def obtener_saldo_en_eur():
    balances = client.get_account()['balances']
    resumen = []
    total_eur = 0.0

    print("Entra en obtener_saldo_en_eur")

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
    print(f"\nTOTAL: {total_eur:.2f} €\n")
    print("Sale en obtener_saldo_en_eur")

    return "\n".join(resumen)

if __name__ == "__main__":

    while True:
        
        print("Antes obtener saldo")
        mensaje = obtener_saldo_en_eur()
        print("Despues obtener saldo")

        time.sleep(INTERVALO_SEGUNDOS)
