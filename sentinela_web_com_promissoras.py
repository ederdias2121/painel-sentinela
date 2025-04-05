
import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(layout="wide")
st.title("📊 Painel Sentinela Cripto em Tempo Real")
st.caption("Atualizado a cada 10 segundos com base na API da Binance")

# Lista das moedas
moedas = [
    "FUNUSDT", "REZUSDT", "GUNZUSDT", "SOLUSDT", "JASMYUSDT",
    "AGIXUSDT", "DOGEUSDT", "FETUSDT", "XRPUSDT", "BTCUSDT", "ETHUSDT"
]

@st.cache_data(ttl=10)
def buscar_precos(moedas):
    precos = []
    for moeda in moedas:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={moeda}"
        try:
            response = requests.get(url)
            data = response.json()
            preco = float(data["price"])
            precos.append({"Moeda": moeda, "Preço Atual": preco})
        except:
            precos.append({"Moeda": moeda, "Preço Atual": "Erro"})
    return pd.DataFrame(precos)

df = buscar_precos(moedas)

# Exibir tabela
st.dataframe(df, use_container_width=True)
