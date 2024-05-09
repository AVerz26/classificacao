import streamlit as st

st.title("Controle de Produção")

st.subheader("Páginas disponíveis para consulta:")
st.page_link("main.py", label="Página de Início", icon="🏠")
st.write("Página de navegação")
st.page_link("pages/Guia.py", label="Guia de Produção", icon="📋")
st.write("Cadastro de itens para o guia de produção")
