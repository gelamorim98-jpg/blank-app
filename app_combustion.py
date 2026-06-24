import streamlit as st
import math

# TÍTULO DA PÁGINA
st.set_page_config(
    page_title="Combustão - Estequiometria e Equilíbrio Químico",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center;'>Combustão - Estequiometria e Equilíbrio Químico</h1>",
    unsafe_allow_html=True
)

# ARMAZENAMENTO DE VARIÁVEIS

if "mostrar_esteq" not in st.session_state:
    st.session_state.mostrar_esteq = False
if "mostrar_equil" not in st.session_state:
    st.session_state.mostrar_equil = False

# BOTÕES DE NAVEGAÇÃO

if st.button("Balanço Estequiométrico", use_container_width=True):
    st.session_state.mostrar_esteq = True
    st.session_state.mostrar_equil = False

if st.button("Equilíbrio Químico", use_container_width=True):
    st.session_state.mostrar_equil = True
    st.session_state.mostrar_esteq = False

st.divider()

# BALANÇO ESTEQUIOMÉTRICO

if st.session_state.mostrar_esteq:
    st.header("Balanço Estequiométrico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x = st.number_input("Número de Carbonos:", min_value=1, value=1, step=1)
    with col2:
        y = st.number_input("Número de Hidrogênios:", min_value=1, value=4, step=1)
    
    st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)
    
    if st.button("Calcular Estequiometria"):
        
        # Cálculos
        O2 = x + y/4
        ar_teorico = O2 / 0.21
        CO2 = x
        H2O = y/2
        
        # Nitrogênio (N₂) - 79% do ar
        N2 = ar_teorico * 0.79
        
        st.subheader("Resultados")
        
        st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)
        st.write(f"**O₂ teórico:** {O2:.2f} mol")
        st.write(f"**Ar teórico:** {ar_teorico:.2f} mol")
        st.write(f"**CO₂ produzido:** {CO2:.2f} mol")
        st.write(f"**H₂O produzida:** {H2O:.2f} mol")
        st.write(f"**N₂:** {N2:.2f} mol")

# EQUILÍBRIO QUÍMICO

if st.session_state.mostrar_equil:
    st.header("Equilíbrio Químico")
    
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
        
        # Nitrogênio (N₂) - 79% do ar
        N2 = ar_teorico * 0.79
        
        st.subheader("Resultados")
        
        st.write(f"**Combustível:** {combustivel}")
        st.write(f"**O₂ teórico:** {O2:.2f} mol")
        st.write(f"**Ar teórico:** {ar_teorico:.2f} mol")
        st.write(f"**CO₂ produzido:** {CO2:.2f} mol")
        st.write(f"**H₂O produzida:** {H2O:.2f} mol")
        st.write(f"**N₂:** {N2:.2f} mol")
