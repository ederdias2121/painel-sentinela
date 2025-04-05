import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(layout="wide")
st.title("📊 Painel Sentinela Cripto (Debug Mockado)")
st.markdown("Simulação com dados de fallback caso API da Binance falhe")

symbols = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT",
    "JASMYUSDT", "AGIXUSDT", "FETUSDT", "GUNZUSDT", "REZUSDT",
    "FUNUSDT", "LAYERUSDT", "ACTUSDT", "WINGUSDT", "1000SATSUSDT", "EOSUSDT"
]

fallback_prices = {
    "BTCUSDT": 70500.0,
    "ETHUSDT": 3550.0,
    "SOLUSDT": 123.5,
    "XRPUSDT": 0.612,
    "DOGEUSDT": 0.165,
    "JASMYUSDT": 0.021,
    "AGIXUSDT": 1.10,
    "FETUSDT": 1.07,
    "GUNZUSDT": 0.061,
    "REZUSDT": 0.017,
    "FUNUSDT": 0.0082,
    "LAYERUSDT": 0.135,
    "ACTUSDT": 0.0019,
    "WINGUSDT": 9.5,
    "1000SATSUSDT": 0.00065,
    "EOSUSDT": 0.91
}

@st.cache_data(ttl=10)
def fetch_prices():
    data = []
    errors = []
    for symbol in symbols:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                data.append({
                    "Moeda": symbol,
                    "Preço": float(json_data['price']),
                    "Fonte": "🔵 Binance"
                })
            else:
                data.append({
                    "Moeda": symbol,
                    "Preço": fallback_prices.get(symbol, 0),
                    "Fonte": f"🟡 Mock (API {response.status_code})"
                })
        except Exception as e:
            errors.append((symbol, str(e)))
            data.append({
                "Moeda": symbol,
                "Preço": fallback_prices.get(symbol, 0),
                "Fonte": "🔴 Mock (Exception)"
            })
    return pd.DataFrame(data), errors

with st.spinner("🔄 Atualizando dados..."):
    df, error_log = fetch_prices()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.error("❌ Nenhum dado retornado. Verifique sua conexão ou a API da Binance.")

if error_log:
    st.markdown("### ⚠️ Log de Erros:")
    for err in error_log:
        st.text(f"{err}")
