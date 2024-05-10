import pandas as pd
import streamlit as st
import os

def save_to_csv_again(df):
    # Define CSV file path
    csv_file = "date.csv"

    # Write DataFrame to CSV file
    df.to_csv(csv_file, index=False)

st.set_page_config(layout="wide")
#Importação dos dados
csv_file = "data.csv"
excel_file = "BD_PROD.xlsx"
itens = "Items.xlsx"

#Dataframes
df = pd.read_csv(csv_file)
df2 = pd.read_excel(excel_file)
items = pd.read_excel(itens)
items['Item'] = items['Item'].astype(str)
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


x = pd.merge(items, df2, left_on='Item', right_on='Item', how='left')
x = x.loc[x['Origem'].isin(["PVA-MOBA-1", "PVA-MOBA-2"])]
soma_conv = x['Conv'].sum()
#
contagem_tipos = x['Tipo'].value_counts()
contagem_embalado = contagem_tipos.get('EMBALADO', 0)
porcentagem_embalado = (contagem_embalado / len(x['Tipo'])) * 100
contagem_granel = contagem_tipos.get('GRANEL', 0)
porcentagem_granel = (contagem_granel / len(x['Tipo'])) * 100
contagem_ind = contagem_tipos.get('INDUSTRIA', 0)
porcentagem_ind = (contagem_ind / len(x['Tipo'])) * 100

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

x = x.sort_values(by='Dt. Produção', ascending=True)
ultimo_valor_data = x['Dt. Produção'].iloc[-1]

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='text-align: right;'>Produção ACA: {} caixas </div>".format(int(soma_conv)), unsafe_allow_html=True)

# Centralize o conteúdo de col2
with col2:
    st.markdown("<div style='text-align: left'><small><em>(Última atualização: {} )</em></small></div>".format(ultimo_valor_data), unsafe_allow_html=True)

porcentagem_formatada = "{:.1f}".format(porcentagem_embalado)
porcentagem_formatada2 = "{:.1f}".format(porcentagem_granel)
porcentagem_formatada3 = "{:.1f}".format(porcentagem_industria)

colu1, colu2, colu3 = st.columns(3)
with colu1:
    st.markdown("<div style='text-align: center'><em>(Embalado: {}% )</em></div>".format(porcentagem_formatada), unsafe_allow_html=True)
with colu2:
    st.markdown("<div style='text-align: center'><em>(Granel: {}% )</em></div>".format(porcentagem_granel), unsafe_allow_html=True)
with colu3:
    st.markdown("<div style='text-align: center'><em>(Industria: {}% )</em></div>".format(porcentagem_industria), unsafe_allow_html=True)

filtered_df['Status'] = ""

m = st.data_editor(
    filtered_df,
    width = 1300,
    height = 800,
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

if st.button("Salvar Alterações"):
    save_to_csv_again(m)

