import pandas as pd
import streamlit as st
import os

#Importação dos dados
csv_file = "data.csv"
excel_file = "BD_PROD.xlsx"

#Dataframes
df = pd.read_csv(csv_file)
df2 = pd.read_excel(excel_file)

df["Date"] = pd.to_datetime(df["Date"])
# Filtra o DataFrame para o dia de hoje
today = pd.Timestamp.today().date()  # Obtém a data de hoje
filtered_df = df[df["Date"].dt.date == today]
filtered_df["A produzir"] = filtered_df["Quantidade"] - filtered_df["Estoque Inicio"]
filtered_df = filtered_df.drop(["Quantidade", "Estoque Inicio"], axis = 1)
# Exibe o DataFrame filtrado
st.write(filtered_df)

st.write(df2.head())

df2["Dt. Produção Imp."] = pd.to_datetime(df2["Dt. Produção Imp."])
df2["Data"] = df2["Dt. Produção Imp."].dt.strftime('%Y-%d-%m')

# Filtrar apenas as linhas onde a data de produção é igual ao dia de hoje
hoje = pd.Timestamp.now().date() - pd.Timedelta(days=1)
hoje = hoje.strftime('%Y-%m-%d')
st.write(df2)
st.write(hoje)
df2 = df2[df2["Data"] == hoje]
st.write(df2)
