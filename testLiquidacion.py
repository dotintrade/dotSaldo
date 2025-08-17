import os
import time
import requests
from binance.client import Client
from dotenv import load_dotenv

# =============================
# Configuración
# =============================
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY_TESTNET")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET_TESTNET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHATID = os.getenv("TELEGRAM_CHATID")

UMBRAL_EUR = 3700.0          # Alerta normal
UMBRAL_EUR_PUMPEO = 3800.0   # Umbral para liquidación
INCLUDE_STABLES = True       # Vender también stablecoins
INTERVALO_SEGUNDOS = 360

DRY_RUN = False               # Ejecutar órdenes reales en Testnet

# =============================
# Conexión a Binance Testnet
# =============================
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
print("[TESTNET] Conectado a Binance Testnet")

# =============================
# Funciones del bot
# =============================
def obtener_saldo_en_eur():
    balances = client.get_account()['balances']
    resumen = []
    total_eur = 0.0

    for b in balances:
        asset = b['asset']
        free = float(b['free'])
        locked = float(b['locked'])
        cantidad = free + locked

        if cantidad > 0 and (INCLUDE_STABLES or asset not in ["USDT", "BUSD", "USDC", "DAI"]):
            try:
                precio = client.get_symbol_ticker(symbol=f"{asset}EUR")['price']
            except:
                try:
                    precio_usdt = float(client.get_symbol_ticker(symbol=f"{asset}USDT")['price'])
                    precio_eur = float(client.get_symbol_ticker(symbol="EURUSDT")['price'])
                    precio = precio_usdt / precio_eur
                except:
                    continue

            valor_eur = cantidad * float(precio)
            total_eur += valor_eur
            resumen.append(f"{asset}: {cantidad:.6f} ≈ {valor_eur:.2f} €")
    
    resumen.append(f"\nTOTAL: {total_eur:.2f} €\n")
    return "\n".join(resumen), total_eur

def enviar_telegram(mensaje):
    send_text = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHATID}&parse_mode=Markdown&text={mensaje}'
    response = requests.get(send_text)
    return response.json()

def cancelar_todas_las_ordenes():
    ok, fail = 0, 0
    for s in client.get_account()['balances']:
        symbol = s['asset']
        try:
            orders = client.get_open_orders(symbol=f"{symbol}EUR")
            for o in orders:
                if not DRY_RUN:
                    client.cancel_order(symbol=f"{symbol}EUR", orderId=o['orderId'])
            ok += len(orders)
        except:
            continue
    return ok, fail

def vender_todos():
    ok, fail = 0, 0
    detalle = []
    balances = client.get_account()['balances']
    for b in balances:
        asset = b['asset']
        free = float(b['free'])
        locked = float(b['locked'])
        cantidad = free + locked

        if cantidad > 0 and (INCLUDE_STABLES or asset not in ["USDT", "BUSD", "USDC", "DAI"]):
            symbol = f"{asset}EUR"
            try:
                if not DRY_RUN:
                    client.order_market_sell(symbol=symbol, quantity=cantidad)
                detalle.append(f"Venta simulada {cantidad} {asset}")
                ok += 1
            except Exception as e:
                detalle.append(f"Error vendiendo {asset}: {str(e)}")
                fail += 1
    return ok, fail, "\n".join(detalle)

# =============================
# Función de testeo real
# =============================
def test_liquidacion_real():
    mensaje, total = obtener_saldo_en_eur()
    enviar_telegram(f"[TESTNET] Saldo inicial: {total:.2f} €\n{mensaje}")
    print(f"[TESTNET] Saldo inicial: {total:.2f} €\n{mensaje}")

    if total >= UMBRAL_EUR_PUMPEO:
        enviar_telegram(f"[TESTNET] Umbral pumpeo alcanzado: {total:.2f} € >= {UMBRAL_EUR_PUMPEO}")
        print(f"[TESTNET] Umbral pumpeo alcanzado: {total:.2f} € >= {UMBRAL_EUR_PUMPEO}")

        ok_cancel, fail_cancel = cancelar_todas_las_ordenes()
        enviar_telegram(f"[TESTNET] Órdenes canceladas: {ok_cancel}")
        print(f"[TESTNET] Órdenes canceladas: {ok_cancel}")

        ok_sell, fail_sell, detalle = vender_todos()
        enviar_telegram(f"[TESTNET] Ventas ejecutadas: {ok_sell}, Fallos: {fail_sell}\n{detalle}")
        print(f"[TESTNET] Ventas ejecutadas: {ok_sell}, Fallos: {fail_sell}\n{detalle}")

        mensaje_post, total_post = obtener_saldo_en_eur()
        enviar_telegram(f"[TESTNET] Saldo post-venta: {total_post:.2f} €\n{mensaje_post}")
        print(f"[TESTNET] Saldo post-venta: {total_post:.2f} €\n{mensaje_post}")

    else:
        enviar_telegram(f"[TESTNET] Saldo ({total:.2f} €) por debajo del umbral de pumpeo ({UMBRAL_EUR_PUMPEO} €)")
        print(f"[TESTNET] Saldo ({total:.2f} €) por debajo del umbral de pumpeo ({UMBRAL_EUR_PUMPEO} €)")

# =============================
# Ejecutar test
# =============================
if __name__ == "__main__":
    test_liquidacion_real()
