import streamlit as st

st.title("Estequiometria e Equilíbrio Químico - Combustão")

combustivel = st.selectbox(
    "Selecione o combustível:",
    ["Metano (CH₄)", "Propano (C₃H₈)", "Octano (C₈H₁₈)"]
)

if combustivel == "Metano (CH₄)":
    x = 1
    y = 4

elif combustivel == "Propano (C₃H₈)":
    x = 3
    y = 8

elif combustivel == "Octano (C₈H₁₈)":
    x = 8
    y = 18

if st.button("Calcular"):

    # O2 teórico
    O2 = x + y/4

    # Ar teórico
    ar_teorico = O2 / 0.21

    # Produtos
    CO2 = x
    H2O = y/2

    st.subheader("Resultados")

    st.write(f"Combustível: {combustivel}")
    st.write(f"O₂ teórico: {O2:.2f} mol")
    st.write(f"Ar teórico: {ar_teorico:.2f} mol")
    st.write(f"CO₂ produzido: {CO2:.2f} mol")
    st.write(f"H₂O produzida: {H2O:.2f} mol")
