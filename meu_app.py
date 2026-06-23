import streamlit as st

st.title("Meu Primeiro App com Streamlit")
st.write("Olá, mundo! Este é meu primeiro aplicativo.")

nome = st.text_input("Digite seu nome:")
if nome:
    st.write(f"Olá, {nome}! Bem-vindo ao Streamlit.")
