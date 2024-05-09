import streamlit as st

# Função para a página inicial
def page_home():
    st.title("Página Inicial")
    st.write("Bem-vindo à página inicial!")

# Função para a página de sobre
def page_about():
    st.title("Sobre")
    st.write("Esta é a página de informações sobre o aplicativo.")

# Função para a página de contato
def page_contact():
    st.title("Contato")
    st.write("Esta é a página de contato1.")

# Função principal para rotear as páginas

st.sidebar.title("Navegação")
selection = st.sidebar.radio("Ir para:", ["Página Inicial", "Sobre", "Contato"])

    # Roteamento das páginas
if selection == "Página Inicial":
    page_home()
elif selection == "Sobre":
    page_about()
elif selection == "Contato":
    page_contact()

