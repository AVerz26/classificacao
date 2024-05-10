import pandas as pd
import streamlit as st
import os

#Importação dos dados
csv_file = "data.csv"
excel_file = "BD_PROD.xlsx"

#Dataframes
df = pd.read_csv(csv_file)
df2 = pd.read_excel(excel_file)
# --------------------------- CONTAGEM ---------------------------- #
df2["Dt. Produção Imp."] = pd.to_datetime(df2["Dt. Produção Imp."])
df2["Data"] = df2["Dt. Produção Imp."].dt.strftime('%Y-%d-%m')

hoje = pd.Timestamp.now().date() - pd.Timedelta(days=2)
hoje = hoje.strftime('%Y-%m-%d')
df2 = df2[df2["Data"] == hoje]
#st.write(df2)
df2["Item"] = df2["Item"].astype(str)
contagem_itens = df2["Item"].value_counts().reset_index()
contagem_itens.columns = ["Item", "Quantidade"]


# ----------------------------- GUIA -------------------------------#

df["Date"] = pd.to_datetime(df["Date"])
# Filtra o DataFrame para o dia de hoje
today = pd.Timestamp.today().date() - pd.Timedelta(days=1)  # Obtém a data de hoje
filtered_df = df[df["Date"].dt.date == today]
filtered_df["A produzir"] = filtered_df["Quantidade"] - filtered_df["Estoque Inicio"]
filtered_df = filtered_df.drop(["Quantidade", "Estoque Inicio"], axis = 1)


filtered_df[['Número do Item', 'Descrição']] = filtered_df['Item'].str.split(' - ', expand=True)

# Converter o número do item para o tipo de dados string (str)
filtered_df['Número do Item'] = filtered_df['Número do Item'].astype(str)

# Fazer um merge entre df12 e contagem_itens usando o número do item como chave de junção
filtered_df = pd.merge(filtered_df, contagem_itens, left_on='Número do Item', right_on='Item', how='right')

# Preencher a coluna "Produzido" com a contagem de itens correspondente
filtered_df['Produzido'] = contagem_itens['Quantidade'].fillna(0).astype(int)

filtered_df['Percentual'] = filtered_df['Produzido'] / filtered_df['A produzir']
#filtered_df['Percentual'] = filtered_df.apply(lambda row: min(row['Percentual'], 1) * 100, axis=1)
filtered_df['Percentual'] = filtered_df.apply(lambda row: f"{min(row['Percentual'], 1) * 100:.1f}%", axis=1)


filtered_df.drop(['Item_y', 'Quantidade', 'Número do Item', 'Descrição', 'Situação'], axis=1, inplace=True)
#filtered_df.dropna(inplace=True)

st.dataframe(filtered_df)
