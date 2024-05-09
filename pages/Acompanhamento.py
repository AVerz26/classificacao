import pandas as pd
import streamlit as st
import os

csv_file = "data.csv"

df = pd.read_csv(csv_file)

df["Date"] = pd.to_datetime(df["Date"])

# Filtra o DataFrame para o dia de hoje
today = pd.Timestamp.today().date()  # Obtém a data de hoje
filtered_df = df[df["Date"].dt.date == today]

filtered_df["A produzir"] = filtered_df["Quantidade"] - filtered_df["Estoque Inicio"]
filtered_df.drop(["Quantidade", "Inicio"], axis = 0)


# Exibe o DataFrame filtrado
st.write(filtered_df)
