import pandas as pd
import streamlit as st
import os

#Importação dos dados
csv_file = "data.csv"
excel_file = "BD_PROD.xlsx"
itens = "Items.xlsx"

#Dataframes
df = pd.read_csv(csv_file)
df2 = pd.read_excel(excel_file)
items = pd.read_excel(itens)
# --------------------------- CONTAGEM ---------------------------- #
df2["Dt. Produção Imp."] = pd.to_datetime(df2["Dt. Produção Imp."])
df2["Data"] = df2["Dt. Produção Imp."].dt.strftime('%Y-%d-%m')

hoje = pd.Timestamp.now().date()
hoje = hoje.strftime('%Y-%m-%d')
df2 = df2[df2["Data"] == hoje]
#st.write(df2)
df2["Item"] = df2["Item"].astype(str)
contagem_itens = df2["Item"].value_counts().reset_index()
contagem_itens.columns = ["Item", "Quantidade"]


# ----------------------------- GUIA -------------------------------#

df["Date"] = pd.to_datetime(df["Date"])
# Filtra o DataFrame para o dia de hoje
today = pd.Timestamp.today().date()  # Obtém a data de hoje
filtered_df = df[df["Date"].dt.date == today]
filtered_df["A produzir"] = filtered_df["Quantidade"] - filtered_df["Estoque Inicio"]
filtered_df = filtered_df.drop(["Quantidade", "Estoque Inicio"], axis = 1)


filtered_df[['Número do Item', 'Descrição']] = filtered_df['Item'].str.split(' - ', expand=True)

# Converter o número do item para o tipo de dados string (str)
filtered_df['Número do Item'] = filtered_df['Número do Item'].astype(str)

x = pd.merge(filtered_df, items, left_on='Número do Item', right_on='Item', how='left')

# Fazer um merge entre df12 e contagem_itens usando o número do item como chave de junção
filtered_df = pd.merge(filtered_df, contagem_itens, left_on='Número do Item', right_on='Item', how='right')

# Preencher a coluna "Produzido" com a contagem de itens correspondente
filtered_df['Produzido'] = contagem_itens['Quantidade'].fillna(0).astype(int)
filtered_df['Produzido'].fillna(0, inplace=True)
filtered_df['A produzir'].fillna(0, inplace=True)
filtered_df['Percentual'] = filtered_df['Produzido'] / filtered_df['A produzir']
filtered_df['Percentual'] = filtered_df.apply(lambda row: min(row['Percentual'], 1) * 100, axis=1)
#filtered_df['Percentual'] = filtered_df.apply(lambda row: f"{min(row['Percentual'], 1) * 100:.1f}%", axis=1)
filtered_df = filtered_df.sort_values(by='Percentual', ascending=False)

filtered_df['Faltantes'] = filtered_df['Produzido'] - filtered_df['A produzir']
filtered_df.loc[filtered_df['Faltantes'] > 0, 'Faltantes'] = 0

filtered_df.drop(['Item_x', 'Date', 'Quantidade', 'Número do Item','Situação'], axis=1, inplace=True)
#filtered_df.dropna(inplace=True)

colunas = filtered_df.columns.tolist()
nova_ordem_colunas = [colunas[2]] + colunas[:2] + colunas[3:]
filtered_df = filtered_df[nova_ordem_colunas]
filtered_df.drop(['Descrição'], axis=1, inplace=True)

# ----------------------------------- SITE ----------------------------------- #

#st.markdown("<div style='text-align: center;'>Produção ACA: {} caixas </div>"format(int(sum(max(dados_filtrados[column]) for column in dados_filtrados.columns[1:9])/360)), unsafe_allow_html=True)
ultimo_valor_data = df2['Dt. Produção'].iloc[-1]

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='text-align: center;'>Produção ACA:  caixas </div>", unsafe_allow_html=True)

# Centralize o conteúdo de col2
with col2:
    st.markdown("<div style='text-align: left'><small><em>(Última atualização: {} )</em></small></div>".format(ultimo_valor_data), unsafe_allow_html=True)



st.data_editor(
    filtered_df,
    width = 1300,
    column_config={
        "Percentual": st.column_config.ProgressColumn(
            "Percentual",
            help="Cumprido",
            format="%.1f",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
)

st.write(x)
