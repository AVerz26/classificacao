import streamlit as st
import csv
import pandas as pd
import os

def save_to_csv(name, age, email):
    # Define CSV file path
    csv_file = "data.csv"

    # Write values to CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, email])

def load_csv_as_dataframe():
    # Define CSV file path
    csv_file = "data.csv"

    # Read CSV file into a DataFrame
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=["Name", "Age", "Email"])  # Create empty DataFrame with specified column names
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

# Define o caminho do arquivo Excel
excel_file_path = "Items.xlsx"

# Carrega os itens e descrições do Excel
items_with_description = load_items_with_description_from_excel(excel_file_path, "Item", "Descrição")

st.title("Form to CSV")

# Create form elements
name = st.selectbox("Escolher item: ", items_with_description)
age = st.number_input("Quantidade:")
email = st.text_input("Situação:")

if st.button("Submit"):
    # Save values to CSV
    save_to_csv(name, age, email)
    st.success("Dados salvos!")

# Load CSV data and display as DataFrame
st.header("Data from CSV")
df = load_csv_as_dataframe()
st.dataframe(df)

# Button to clear CSV data
if st.button("Limpar dados"):
    clear_csv()
    save_to_csv("Item", "Quantidade", "Situação")
