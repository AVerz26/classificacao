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
st.dataframe(df)

# Button to clear CSV data
if st.button("Clear Data"):
    clear_csv()
