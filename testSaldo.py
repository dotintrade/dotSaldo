import os
import time
import math
import requests
from decimal import Decimal
from binance.client import Client
from binance.enums import SIDE_SELL, ORDER_TYPE_MARKET
from dotenv import load_dotenv

# =============================
# Configuración
# =============================
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHATID = os.getenv("TELEGRAM_CHATID")

INTERVALO_SEGUNDOS = 1800
UMBRAL_EUR_ALERTA = 3800.0   # umbral de notificacion
UMBRAL_EUR_PUMPEO = 5500.0   # umbral de liquidacion

USE_TESTNET = False
INCLUDE_STABLES = False
DRY_RUN = False

# =============================
# Conexión Binance
# =============================
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=USE_TESTNET)
print("Conectado a Binance (testnet=%s)" % USE_TESTNET)

# =============================
# Funciones auxiliares
# =============================
def enviar_telegram(mensaje: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHATID, "text": mensaje}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"[Telegram] Error: {e}")

def get_all_tickers_map():
    tickers = client.get_all_tickers()
    return {t['symbol']: float(t['price']) for t in tickers}

def get_symbol_if_exists(symbol: str):
    try:
        return client.get_symbol_info(symbol)
    except:
        return None

def floor_step(value: float, step: float) -> float:
    if step <= 0:
        return value
    v = Decimal(str(value))
    s = Decimal(str(step))
    floored = (v // s) * s
    return float(floored)

def ajustar_cantidad(symbol_info: dict, qty: float) -> float:
    for f in symbol_info.get("filters", []):
        if f.get("filterType") in ("LOT_SIZE", "MARKET_LOT_SIZE"):
            step = float(f["stepSize"])
            min_qty = float(f["minQty"])
            qty = floor_step(qty, step)
            if qty < min_qty:
                return 0.0
            return qty
    return qty

def cumple_min_notional(symbol_info: dict, price: float, qty: float) -> bool:
    for f in symbol_info.get("filters", []):
        if f.get("filterType") in ("MIN_NOTIONAL", "NOTIONAL"):
            min_val = float(f.get("minNotional", f.get("notional", 0)))
            return qty * price >= min_val
    return True

def elegir_par(asset: str):
    if asset == "EUR":
        return None
    for s in (f"{asset}EUR", f"{asset}USDT"):
        if get_symbol_if_exists(s):
            return s
    return None

def obtener_saldo_en_eur():
    balances = client.get_account()["balances"]
    tickers = get_all_tickers_map()
    precio_eur_usdt = tickers.get("EURUSDT", None)
    total_eur = 0.0
    resumen = []
    for b in balances:
        asset = b["asset"]
        cantidad = float(b["free"]) + float(b["locked"])
        if cantidad <= 0:
            continue
        if asset == "EUR":
            total_eur += cantidad
            resumen.append(f"{asset}: {cantidad:.6f} ≈ {cantidad:.2f} €")
            continue
        precio = None
        if f"{asset}EUR" in tickers:
            precio = tickers[f"{asset}EUR"]
        elif f"{asset}USDT" in tickers and precio_eur_usdt:
            precio = tickers[f"{asset}USDT"] / precio_eur_usdt
        if precio:
            valor = cantidad * precio
            total_eur += valor
            resumen.append(f"{asset}: {cantidad:.6f} ≈ {valor:.2f} €")
    resumen.append(f"\nTOTAL: {total_eur:.2f} €\n")
    return "\n".join(resumen), total_eur

def cancelar_todas_las_ordenes():
    try:
        abiertas = client.get_open_orders()
        for o in abiertas:
            if DRY_RUN:
                print(f"[DRY_RUN] Cancelaría {o['orderId']} en {o['symbol']}")
            else:
                client.cancel_order(symbol=o["symbol"], orderId=o["orderId"])
                print(f"Cancelada {o['orderId']} en {o['symbol']}")
        return len(abiertas)
    except Exception as e:
        print(f"Error cancelando órdenes: {e}")
        return 0

def es_stable(asset: str):
    return asset in {"USDT", "BUSD", "USDC", "FDUSD", "TUSD", "DAI", "EUR"}

def vender_todos():
    logs = []
    ok, fail = 0, 0
    canceladas = cancelar_todas_las_ordenes()
    logs.append(f"Órdenes canceladas: {canceladas}")
    balances = client.get_account()["balances"]
    tickers = get_all_tickers_map()
    for b in balances:
        asset = b["asset"]
        qty_total = float(b["free"]) + float(b["locked"])
        if qty_total <= 0:
            continue
        if not INCLUDE_STABLES and es_stable(asset) and asset != "EUR":
            logs.append(f"Preservado {asset}: {qty_total}")
            continue
        if asset == "EUR":
            logs.append(f"Preservado EUR: {qty_total}")
            continue
        symbol = elegir_par(asset)
        if not symbol:
            logs.append(f"No par para {asset}")
            continue
        price = tickers.get(symbol, 0)
        if not price:
            logs.append(f"Sin precio {symbol}")
            continue
        info = get_symbol_if_exists(symbol)
        qty_adj = ajustar_cantidad(info, qty_total)
        if qty_adj <= 0 or not cumple_min_notional(info, price, qty_adj):
            logs.append(f"{asset}: no cumple min_notional/lote")
            continue
        try:
            if DRY_RUN:
                logs.append(f"[DRY_RUN] Vendería {qty_adj} {asset} en {symbol}")
                ok += 1
            else:
                client.order_market_sell(symbol=symbol, quantity=str(qty_adj))
                logs.append(f"Vendido {qty_adj} {asset} en {symbol}")
                ok += 1
        except Exception as e:
            logs.append(f"Error {asset}: {e}")
            fail += 1
    return ok, fail, "\n".join(logs)

# =============================
# Loop principal
# =============================
if __name__ == "__main__":
    while True:
        try:
            mensaje, total = obtener_saldo_en_eur()

            if total >= UMBRAL_EUR_PUMPEO:
                enviar_telegram(f"🚨 UMBRAL DE PUMPEO SUPERADO ({total:.2f} € >= {UMBRAL_EUR_PUMPEO} €)\nIniciando liquidación...")
                
                ok, fail, detalle = vender_todos()
                enviar_telegram(f"Liquidación completada\nÉxitos: {ok} | Errores: {fail}\n\n{detalle}")
                
                # Saldo post-venta
                mensaje_post, total_post = obtener_saldo_en_eur()
                enviar_telegram(f"💰 Saldo después de la liquidación: {total_post:.2f} €\n\n{mensaje_post}")

            elif total >= UMBRAL_EUR_ALERTA:
                enviar_telegram(f"⚠️ ALERTA: saldo total {total:.2f} € supera el umbral {UMBRAL_EUR_ALERTA} €\n\n{mensaje}")

            else:
                print(f"Saldo total {total:.2f} € por debajo del umbral de alerta ({UMBRAL_EUR_ALERTA} €)\n")

        except Exception as e:
            enviar_telegram(f"Error en el bot: {e}")
            print(f"Error: {e}")

        time.sleep(INTERVALO_SEGUNDOS)
