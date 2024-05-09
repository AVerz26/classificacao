import pandas as pd
import streamlit as st
import os

csv_file = "data.csv"

df = pd.read_csv(csv_file)

st.write(df)
