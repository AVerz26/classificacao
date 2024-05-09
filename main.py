import streamlit as st

st.sidebar.write("Links adicionais")
st.sidebar.markdown("[Acompanhamento Esteiras Kajoo](https://esteiraskajoo.streamlit.app)")

st.title("Controle e Acompanhamento da Produção")

st.subheader("Páginas disponíveis para consulta:")
st.page_link("main.py", label="Página de Início", icon="🏠")
st.caption("Página de navegação")
st.page_link("pages/Guia.py", label="Guia de Produção", icon="📋")
st.caption("Cadastro de itens para o guia de produção")
st.page_link("pages/Acompanhamento.py", label="Acompanhamento da Produção", icon="📊")
st.caption("Acompanhamento de itens de produção")
st.page_link("pages/Rastreabilidade.py", label="Rastreabilidade de Cargas", icon="🔍")
st.caption("Rastreabilidade de caixas detalhado")
