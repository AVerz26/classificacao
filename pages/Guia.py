import streamlit as st
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Função para salvar o DataFrame de volta para o arquivo CSV
def save_dataframe_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)

# Função para carregar o DataFrame do arquivo CSV
def load_csv_as_dataframe(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=["Date", "Name", "Age", "Email"])
    return df

# Função para limpar o arquivo CSV
def clear_csv(csv_file):
    if os.path.exists(csv_file):
        os.remove(csv_file)
        st.success("Data cleared successfully!")
    else:
        st.warning("No data to clear.")

st.sidebar.header("Links Úteis")
st.sidebar.markdown("[:egg: Rastreabilidade de Ovos](https://esteiraskajoo.streamlit.app/)")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.title("Adicionar itens para o guia:")
    
    # Carregar o arquivo CSV
    csv_file = "data.csv"
    df = load_csv_as_dataframe(csv_file)
    
    # Exibir o DataFrame como uma tabela editável
    st.header("Listagem do Guia de Produção:")
    edited_df = st.dataframe(df, editable=True)
    
    # Botão para salvar as alterações
    if st.button("Salvar Alterações"):
        save_dataframe_to_csv(edited_df, csv_file)
        st.success("Alterações salvas com sucesso!")
    
    # Botão para limpar os dados
    if st.button("Limpar Dados"):
        clear_csv(csv_file)
        st.info("Dados excluídos com sucesso!")
elif authentication_status == False:
    st.error('Nome de usuário/senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')
