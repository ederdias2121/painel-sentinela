
import requests
import pandas as pd
import time
from datetime import datetime

# Lista de pares monitorados
moedas = [
    "FUNUSDT", "REZUSDT", "GUNUSDT", "SOLUSDT", "JASMYUSDT",
    "AGIXUSDT", "DOGEUSDT", "FETUSDT", "BTCUSDT", "ETHUSDT", "XRPUSDT"
]

# Função para obter o preço atual da moeda
def obter_preco(moeda):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={moeda}"
    try:
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        return float(dados["price"])
    except:
        return None

# Obter dados e gerar DataFrame
dados = []
for moeda in moedas:
    preco = obter_preco(moeda)
    if preco:
        dados.append({
            "Moeda": moeda,
            "Preço Atual (USDT)": preco,
            "Data/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

df = pd.DataFrame(dados)

# Exportar para Excel e CSV
excel_path = "/Users/ederdias/Documents/cripto/Painel_Sentinela_Python.xlsx"
csv_path = "/mnt/data/Painel_Sentinela_Python.csv"

df.to_excel(excel_path, index=False)
df.to_csv(csv_path, index=False)

print("Painel exportado com sucesso!")
