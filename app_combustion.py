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

# ============================================
# INICIALIZAR SESSION STATE
# ============================================
if "pagina" not in st.session_state:
    st.session_state.pagina = None

# BOTÕES DE NAVEGAÇÃO
col1, col2 = st.columns(2)

with col1:
    if st.button("Balanço Estequiométrico", use_container_width=True):
        st.session_state.pagina = "esteq"

with col2:
    if st.button("Equilíbrio Químico", use_container_width=True):
        st.session_state.pagina = "equil"

st.divider()

# ============================================
# SEÇÃO 1: BALANÇO ESTEQUIOMÉTRICO
# ============================================
if st.session_state.pagina == "esteq":
    st.header("Balanço Estequiométrico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x = st.number_input("Número de Carbonos:", min_value=1, value=1, step=1, key="x_carbonos")
    with col2:
        y = st.number_input("Número de Hidrogênios:", min_value=1, value=4, step=1, key="y_hidrogenios")
    
    st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)
    
    # Botão para calcular
    if st.button("Calcular Estequiometria", key="calc_esteq"):
        
        # Cálculos
        O2 = x + y/4
        ar_teorico = O2 / 0.21
        CO2 = x
        H2O = y/2
        
        # Salva os resultados no session_state
        st.session_state.resultados_esteq = {
            "x": x,
            "y": y,
            "O2": O2,
            "ar_teorico": ar_teorico,
            "CO2": CO2,
            "H2O": H2O
        }
    
    # Exibe os resultados se existirem
    if "resultados_esteq" in st.session_state:
        res = st.session_state.resultados_esteq
        
        st.subheader("Resultados")
        
        st.write(f"**Combustível:** C<sub>{res['x']}</sub>H<sub>{res['y']}</sub>", unsafe_allow_html=True)
        st.write(f"**O₂ teórico:** {res['O2']:.2f} mol")
        st.write(f"**Ar teórico:** {res['ar_teorico']:.2f} mol")
        st.write(f"**CO₂ produzido:** {res['CO2']:.2f} mol")
        st.write(f"**H₂O produzida:** {res['H2O']:.2f} mol")

# ============================================
# SEÇÃO 2: EQUILÍBRIO QUÍMICO
# ============================================
if st.session_state.pagina == "equil":
    st.header("⚖️ Equilíbrio Químico")
    
    combustivel = st.selectbox(
        "Selecione o combustível:",
        ["Metano (CH₄)", "Propano (C₃H₈)", "Octano (C₈H₁₈)"],
        key="combustivel_equilibrio"
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
    
    if st.button("Calcular Equilíbrio", key="calc_equil"):
        
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
