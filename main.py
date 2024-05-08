import streamlit as st
import csv

def save_to_csv(name, age, email):
    # Define CSV file path
    csv_file = "data.csv"

    # Write values to CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, email])


st.title("Form to CSV")

    # Create form elements
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:")
email = st.text_input("Enter your email:")

if st.button("Submit"):
        # Save values to CSV
    save_to_csv(name, age, email)
    st.success("Data saved successfully!")

