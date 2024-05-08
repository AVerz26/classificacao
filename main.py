import streamlit as st
import csv
import pandas as pd

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
    df = pd.read_csv(csv_file)
    return df

st.title("Form to CSV")

# Create form elements
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:")
email = st.text_input("Enter your email:")

if st.button("Submit"):
    # Save values to CSV
    save_to_csv(name, age, email)
    st.success("Data saved successfully!")

# Load CSV data and display as DataFrame
st.header("Data from CSV")
df = load_csv_as_dataframe()
st.write(df)
