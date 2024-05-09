import streamlit as st
import pandas as pd

# Carrega o arquivo Excel
@st.cache
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Função para procurar a etiqueta e retornar as informações
def search_label(df, label):
    # Procura a etiqueta na primeira coluna
    row = df[df['Etiqueta'] == label]
    if not row.empty:
        return row.iloc[0]  # Retorna a primeira linha encontrada
    else:
        return None

st.title("Pesquisa de Etiqueta")
    
    # Carrega o arquivo Excel
file_path = "BD_PROD.xlsx"
df = load_data(file_path)
    
    # Entrada para o usuário
label = st.text_input("Digite o código da etiqueta:")
    
if st.button("Procurar"):
    if label:
            # Procura a etiqueta e exibe as informações
        result = search_label(df, label)
        if result is not None:
            st.success("Etiqueta encontrada!")
            st.write("Informações:")
            st.write("Item: ",result[1])
            st.write("Produzido: ",result[2])
            st.write("Data/Hora produzida: ",result[8])
            st.write("Data/Hora embarcada: ",result[9])
        else:
            st.warning("Etiqueta não encontrada.")
    else:
        st.warning("Por favor, digite o código da etiqueta.")


