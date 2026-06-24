import streamlit as st
import math

#TÍTULO DA PÁGINA

st.set_page_config(
    page_title="Combustão - Estequiometria e Equilíbrio Químico",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center;'>Combustão - Estequiometria e Equilíbrio Químico</h1>",
    unsafe_allow_html=True
)

# BOTÕES DE NAVEGAÇÃO

botao_esteq = st.button("📁 Balanço Estequiométrico", use_container_width=True)
botao_equil = st.button("📁 Equilíbrio Químico", use_container_width=True)

st.divider()

# BOTÃO 1: BALANÇO ESTEQUIOMÉTRICO

if botao_esteq:
    st.header("📁 Balanço Estequiométrico")
   
    col1, col2 = st.columns(2)
    
    with col1:
        x = st.number_input("Número de Carbonos:", min_value=1, value=1, step=1)
    with col2:
        y = st.number_input("Número de Hidrogênios:", min_value=1, value=4, step=1)
    
    st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)
    
    if st.button("Calcular Estequiometria"):
        
        O2 = x + y/4
        ar_teorico = O2 / 0.21
        CO2 = x
        H2O = y/2
        
        st.subheader("Resultados")
        
        st.write(f"**Combustível:** C{x}H{y}")
        st.write(f"**O₂ teórico:** {O2:.2f} mol")
        st.write(f"**Ar teórico:** {ar_teorico:.2f} mol")
        st.write(f"**CO₂ produzido:** {CO2:.2f} mol")
        st.write(f"**H₂O produzida:** {H2O:.2f} mol")

# ============================================
# SEÇÃO 2: EQUILÍBRIO QUÍMICO
# ============================================
if botao_equil:
    st.header("⚖️ Equilíbrio Químico")
    
    # Seu código original
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
    
    if st.button("Calcular Equilíbrio"):
        
        # Cálculos
        O2 = x + y/4
        ar_teorico = O2 / 0.21
        CO2 = x
        H2O = y/2
        
        st.subheader("Resultados")
        
        st.write(f"**Combustível:** {combustivel}")
        st.write(f"**O₂ teórico:** {O2:.2f} mol")
        st.write(f"**Ar teórico:** {ar_teorico:.2f} mol")
        st.write(f"**CO₂ produzido:** {CO2:.2f} mol")
        st.write(f"**H₂O produzida:** {H2O:.2f} mol")
