import streamlit as st
import csv
import pandas as pd
import os
import streamlit_authenticator as stauth

def save_to_csv(date, name, age, email):
    # Define CSV file path
    csv_file = "data.csv"

    # Write values to CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, name, age, email])

def load_csv_as_dataframe():
    # Define CSV file path
    csv_file = "data.csv"

    # Read CSV file into a DataFrame
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=["Date", "Name", "Age", "Email"])  # Create empty DataFrame with specified column names
    return df

def clear_csv():
    # Define CSV file path
    csv_file = "data.csv"

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

import yaml
from yaml.loader import SafeLoader

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    # Define o caminho do arquivo Excel
    excel_file_path = "Items.xlsx"
    
    # Carrega os itens e descrições do Excel
    items_with_description = load_items_with_description_from_excel(excel_file_path, "Item", "Descrição")
    
    st.sidebar.header("Links Úteis")
    st.sidebar.markdown("[:egg: Rastreabilidade de Ovos](https://esteiraskajoo.streamlit.app/)")
    
    st.title("Adicionar itens para o guia:")
    
    # Create form elements
    date = st.date_input("Data:", value=None, format="DD/MM/YYYY")
    name = st.selectbox("Escolher item: ", items_with_description)
    age = st.number_input("Quantidade:")
    email = st.text_input("Situação:")
    
    if st.button("Enviar"):
        # Save values to CSV
        save_to_csv(date, name, age, email)
        st.success("Dados salvos!")
    
    # Load CSV data and display as DataFrame
    st.header("Listagem do Guia de Produção:")
    df = load_csv_as_dataframe()
    #st.dataframe(df)
    
    edited_df = st.data_editor(df)
    
    # Button to clear CSV data
    if st.button("Limpar dados"):
        clear_csv()
        save_to_csv("Date", "Item", "Quantidade", "Situação")


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')



