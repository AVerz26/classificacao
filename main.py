import streamlit as st
import pandas as pd
import os

def save_to_csv(df):
    # Define CSV file path
    csv_file = "data.csv"

    # Save DataFrame to CSV file
    df.to_csv(csv_file, index=False)

def load_csv_as_dataframe():
    # Define CSV file path
    csv_file = "data.csv"

    # Read CSV file into a DataFrame
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=["Item", "Quantidade", "Prioridade"])  # Create empty DataFrame with specified column names
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

st.title("CSV Editor")

# Load CSV data into a DataFrame
df = load_csv_as_dataframe()

# Display DataFrame as editable table
st.header("Edit CSV Data")
edited_df = st.dataframe(df, editable=True)

# Save changes to CSV file when user clicks a button
if st.button("Save Changes"):
    save_to_csv(edited_df)
    st.success("Changes saved successfully!")

# Button to clear CSV data
if st.button("Clear Data"):
    clear_csv()
