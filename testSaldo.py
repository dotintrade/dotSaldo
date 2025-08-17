import os
import time
from binance.client import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

INTERVALO_SEGUNDOS = 10
UMBRAL_EUR = 3800.0

# Conexión a Binance
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

print("Conectado a Binance")

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

    return "\n".join(resumen), total_eur


if __name__ == "__main__":
    while True:
        mensaje, total = obtener_saldo_en_eur()

        # Mostrar saldo solo si supera el umbral
        if total >= UMBRAL_EUR:
            print(mensaje)
        else:
            print(f"Saldo total ({total:.2f} €) por debajo del umbral ({UMBRAL_EUR} €).")

        time.sleep(INTERVALO_SEGUNDOS)
