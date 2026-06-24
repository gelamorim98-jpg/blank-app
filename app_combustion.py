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

# ARMAZENAMENTO DAS VARIÁVEIS
if "mostrar_esteq" not in st.session_state:
    st.session_state.mostrar_esteq = False

# BOTÕES DE NAVEGAÇÃO
if st.button("Balanço Estequiométrico", use_container_width=True):
    st.session_state.mostrar_esteq = True
    st.session_state.mostrar_equil = False
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
        
        # CÁLCULOS
        # A reação no formato: CxHy + a(O2 + 3,76N2) → bCO2 + cH2O + dN2
        # a = O₂ necessário
        a = x + y/4
        
        # b = CO₂ produzido
        b = x
        
        # c = H₂O produzida
        c = y/2
        
        # d = N₂
        d = 3.76 * a
        
        # Ar teórico
        ar_teorico = a * 4.76
        
        # RESULTADOS
        st.divider()
        st.markdown(
            "<h2 style='text-align: center;'>Resultados</h2>",
            unsafe_allow_html=True
        )
        st.divider()
        
        st.markdown("### ➡️ Reação Global Balanceada")
        reacao = f"C<sub>{x}</sub>H<sub>{y}</sub> + {a:.2f}(O₂ + 3,76 N₂) → {b:.2f} CO₂ + {c:.2f} H₂O + {d:.2f} N₂"
        
        st.markdown(
            f"""
            <div style='
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #ff4b4b;
                font-size: 18px;
                text-align: center;
                font-family: 'Courier New', monospace;
            '>
                <b>{reacao}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()
          
        # AR TEÓRICO
        
        st.markdown("### ➡️ Ar Teórico")
        col_ar1, col_ar2, col_ar3 = st.columns(3)
        with col_ar1:
            st.metric(
                label="Ar teórico (mol)",
                value=f"{ar_teorico:.2f} mol"
            )
        with col_ar2:
            st.metric(
                label="O₂ necessário (mol)",
                value=f"{a:.2f} mol"
            )
        with col_ar3:
            st.metric(
                label="N₂ acompanhante (mol)",
                value=f"{d:.2f} mol"
            )
        st.divider()
