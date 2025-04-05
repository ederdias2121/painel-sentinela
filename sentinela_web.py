
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

st.set_page_config(page_title="Painel Sentinela Cripto", layout="wide")

st.title("📊 Painel Sentinela Cripto em Tempo Real")
st.caption("Atualizado a cada 10 segundos com base na API da Binance")

# Função para buscar preços em tempo real da Binance
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return float(response.json()['price'])
    except:
        return None

# Lista de moedas (pode ser expandida depois)
symbols = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT",
    "FETUSDT", "AGIXUSDT", "FUNUSDT", "REZUSDT", "GUNUSDT",
    "JASMYUSDT", "LAYERUSDT", "ACTUSDT", "WINGUSDT", "GUNZUSDT"
]

# Função para montar o painel
def gerar_painel():
    dados = []
    for symbol in symbols:
        preco = get_price(symbol)
        if preco:
            rsi = round(30 + (preco % 40), 2)  # Simulação de RSI apenas para visual
            tendencia = (
                "🔴 Sobrevendido" if rsi < 30 else
                "🟡 Lateral" if rsi <= 50 else
                "🟢 Alta"
            )
            suporte = round(preco * 0.93, 6)
            resistencia = round(preco * 1.05, 6)
            tp = round(preco * 1.08, 6)
            sl = round(preco * 0.95, 6)
            dados.append({
                "Moeda": symbol,
                "Preço Atual (USDT)": preco,
                "RSI (Simulado)": rsi,
                "Tendência": tendencia,
                "Suporte": suporte,
                "Resistência": resistencia,
                "Take Profit": tp,
                "Stop Loss": sl,
                "Atualizado em": datetime.now().strftime('%H:%M:%S')
            })
    return pd.DataFrame(dados)

# Área principal do painel
placeholder = st.empty()

while True:
    df = gerar_painel()
    with placeholder.container():
        st.dataframe(df, use_container_width=True)
    time.sleep(10)
