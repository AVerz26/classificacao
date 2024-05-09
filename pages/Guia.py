import streamlit as st
import csv
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def save_to_csv(df, csv_file):
    # Write DataFrame to CSV file
    df.to_csv(csv_file, index=False)

def load_csv_as_dataframe(csv_file):
    # Read CSV file into a DataFrame
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=["Date", "Name", "Age", "Email"])  # Create empty DataFrame with specified column names
    return df

def clear_csv(csv_file):
    # Check if CSV file exists, then delete it
    if os.path.exists(csv_file):
        os.remove(csv_file)
        st.success("Data cleared successfully!")
    else:
        st.warning("No data to clear.")

def load_items_with_description_from_excel(file_path, column_name_item, column_name_description):
    # Carrega o arquivo Excel
    df = pd.read_excel(file_path)
    
    # Convertendo os dados das colunas para string e depois concatenando
    items_with_description = df[column_name_item].astype(str) + " - " + df[column_name_description].astype(str)
    
    return items_with_description.tolist()

# Define o caminho do arquivo Excel
excel_file_path = "Items.xlsx"

# Carrega os itens e descrições do Excel
items_with_description = load_items_with_description_from_excel(excel_file_path, "Item", "Descrição")

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
    
    # Carrega o arquivo CSV
    csv_file = "data.csv"
    df = load_csv_as_dataframe(csv_file)
    
    # Create form elements
    date = st.date_input("Data:")
    name = st.selectbox("Escolher item: ", items_with_description)
    age = st.number_input("Quantidade:")
    email = st.text_input("Situação:")
    
    if st.button("Enviar"):
        # Adiciona uma nova linha ao DataFrame com os valores inseridos
        new_row = {"Date": date, "Name": name, "Age": age, "Email": email}
        df = df.append(new_row, ignore_index=True)
        
        # Salva o DataFrame modificado de volta para o arquivo CSV
        save_to_csv(df, csv_file)
        
        st.success("Dados salvos!")
    
    # Exibe o DataFrame como uma tabela editável
    st.header("Listagem do Guia de Produção:")
    edited_df = st.dataframe(df, editable=True)
    
    # Button to clear CSV data
    if st.button("Limpar dados"):
        clear_csv(csv_file)
        st.info("Dados excluídos com sucesso.")
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
