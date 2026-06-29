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

# OPÇÃO DE PODER CALORÍFICO - NO TOPO
st.markdown("### ⚡ Configuração do Calor de Combustão")
col_calor_config1, col_calor_config2 = st.columns(2)

with col_calor_config1:
    tipo_calor = st.radio(
        "Tipo de poder calorífico:",
        options=["Poder Calorífico Superior (PCS)", "Poder Calorífico Inferior (PCI)"],
        index=0,
        horizontal=True
    )

with col_calor_config2:
    st.caption("📌 **PCS**: Água nos produtos no estado líquido")
    st.caption("📌 **PCI**: Água nos produtos no estado vapor")
    st.caption("📌 ΔHf° (kJ/mol): CO₂ = -393.5 | H₂O(l) = -285.8 | H₂O(g) = -241.8")

st.divider()

# BOTÕES DE NAVEGAÇÃO
if st.button("Balanço Estequiométrico", use_container_width=True):
    st.session_state.mostrar_esteq = True
    st.session_state.mostrar_equil = False
st.divider()

# BALANÇO ESTEQUIOMÉTRICO
if st.session_state.mostrar_esteq:
    
    col1, col2 = st.columns(2)
    
    with col1:
        x = st.number_input("Número de Carbonos:", min_value=1, value=1, step=1)
    with col2:
        y = st.number_input("Número de Hidrogênios:", min_value=1, value=4, step=1) 
        
    st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Condições de Combustão")
    
    col_ar1, col_ar2 = st.columns(2)
    
    with col_ar1:
        tipo_ar = st.radio(
            "Tipo de condição:",
            options=["Excesso de ar", "Deficiência de ar", "Estequiométrico"],
            index=2,
            horizontal=True
        )
    
    # Campos para entrada do valor de excesso/deficiência
    with col_ar2:
        if tipo_ar == "Excesso de ar":
            excesso_valor = st.number_input(
                "Digite o % de excesso de ar:",
                min_value=1.0,
                max_value=200.0,
                value=20.0,
                step=5.0,
                format="%.1f"
            )
            fator_excesso = 1 + excesso_valor / 100
        
        elif tipo_ar == "Deficiência de ar":
            deficiencia_valor = st.number_input(
                "Digite o % de deficiência de ar:",
                min_value=1.0,
                max_value=80.0,
                value=20.0,
                step=5.0,
                format="%.1f"
            )
            fator_excesso = 1 - deficiencia_valor / 100
        
        else:  # Estequiométrico
            fator_excesso = 1.0
            st.info("✅ Condição estequiométrica (sem excesso ou deficiência de ar)")
        
    if st.button("Calcular Estequiometria", use_container_width=True):
        
        # CÁLCULOS ESTEQUIOMÉTRICOS (ar teórico)
        a_teorico = x + y/4  # O₂ necessário estequiométrico
        
        # Aplicando o fator de excesso/deficiência
        a_real = a_teorico * fator_excesso
        
        # b = CO₂ produzido (depende se há deficiência de ar)
        if fator_excesso < 1:
            # Em deficiência de ar, pode haver CO e/ou carbono
            # O₂ disponível para oxidar C após formar H₂O
            o2_para_c = a_real - (y/4)
            
            if o2_para_c >= x:
                # O₂ suficiente para oxidar todo C a CO₂
                b = x
                c = y/2
                co = 0
                o2_residual = max(0, o2_para_c - x)
                carbono_solid = 0
            elif o2_para_c > 0:
                # O₂ insuficiente para oxidar todo C a CO₂
                b = o2_para_c
                co = (x - b) * 2
                c = y/2
                o2_residual = 0
                carbono_solid = 0
            else:
                # Sem O₂ para oxidar C (apenas H₂O)
                b = 0
                co = x * 2
                c = y/2
                o2_residual = 0
                carbono_solid = 0
            
            # Ajuste para quando não há O₂ suficiente nem para CO
            if co > 0 and a_real < y/4 + co/2:
                o2_disponivel_co = a_real - y/4
                if o2_disponivel_co > 0:
                    co = o2_disponivel_co * 2
                    b = 0
                    carbono_solid = x - co/2
                else:
                    co = 0
                    carbono_solid = x
            else:
                if carbono_solid == 0 and co > 0 and b == 0:
                    # Verifica se todo C foi convertido
                    carbono_solid = max(0, x - co/2)
                
        else:
            # Estequiométrico ou excesso de ar
            b = x
            c = y/2
            co = 0
            o2_residual = max(0, a_real - a_teorico)
            carbono_solid = 0
        
        # N₂ acompanhante
        d = 3.76 * a_real
        
        # Ar real
        ar_real = a_real * 4.76
        
        # ===== CÁLCULO DO CALOR DE COMBUSTÃO =====
        
        # Entalpias de formação (kJ/mol) a 25°C
        delta_hf = {
            'CO2': -393.5,      # CO₂(g)
            'H2O_l': -285.8,    # H₂O(l)
            'H2O_g': -241.8,    # H₂O(g)
            'CO': -110.5,       # CO(g)
            'C': 0.0,           # C(s) - grafite
            'O2': 0.0,          # O₂(g)
            'N2': 0.0           # N₂(g)
        }
        
        # Entalpia de formação do combustível (CxHy)
        # Valores para combustíveis comuns
        if x == 1 and y == 4:  # Metano
            delta_hf_combustivel = -74.8
        elif x == 2 and y == 6:  # Etano
            delta_hf_combustivel = -84.7
        elif x == 3 and y == 8:  # Propano
            delta_hf_combustivel = -103.8
        elif x == 4 and y == 10:  # Butano
            delta_hf_combustivel = -126.1
        elif x == 5 and y == 12:  # Pentano
            delta_hf_combustivel = -146.8
        elif x == 6 and y == 14:  # Hexano
            delta_hf_combustivel = -167.2
        elif x == 7 and y == 16:  # Heptano
            delta_hf_combustivel = -187.8
        elif x == 8 and y == 18:  # Octano
            delta_hf_combustivel = -208.4
        elif x == 10 and y == 22:  # Decano
            delta_hf_combustivel = -249.6
        else:
            # Estimativa para outros hidrocarbonetos
            delta_hf_combustivel = -(20*x + 10*y)
        
        # Cálculo do calor de combustão (Lei de Hess)
        # ΔH_comb = Σ(n*ΔHf°_produtos) - Σ(n*ΔHf°_reagentes)
        
        # Produtos
        delta_h_produtos = 0
        
        # CO₂
        if b > 0:
            delta_h_produtos += b * delta_hf['CO2']
        
        # CO
        if co > 0:
            delta_h_produtos += co * delta_hf['CO']
        
        # Carbono sólido
        if carbono_solid > 0:
            delta_h_produtos += carbono_solid * delta_hf['C']
        
        # H₂O (depende se é PCS ou PCI)
        if c > 0:
            if tipo_calor == "Poder Calorífico Superior (PCS)":
                # Água líquida
                delta_h_produtos += c * delta_hf['H2O_l']
            else:
                # Água vapor
                delta_h_produtos += c * delta_hf['H2O_g']
        
        # Reagentes
        delta_h_reagentes = delta_hf_combustivel  # Apenas o combustível (O₂ e N₂ são 0)
        
        # Calor de combustão (kJ/mol de combustível)
        delta_h_combustao = delta_h_produtos - delta_h_reagentes
        
        # Calor liberado por mol de combustível (negativo = exotérmico)
        calor_liberado = -delta_h_combustao  # kJ/mol
        
        # Conversão para kJ/kg (considerando massa molar do combustível)
        massa_molar = x*12 + y*1  # g/mol
        calor_liberado_kg = calor_liberado * 1000 / massa_molar  # kJ/kg
        
        # ===== EXIBIÇÃO DOS RESULTADOS =====
        st.divider()
        st.markdown(
            "<h2 style='text-align: center;'>Resultados</h2>",
            unsafe_allow_html=True
        )
        st.divider()
        
        # Mostra condição atual
        if tipo_ar == "Excesso de ar":
            st.markdown(f"**Condição:** {excesso_valor:.1f}% de excesso de ar")
        elif tipo_ar == "Deficiência de ar":
            st.markdown(f"**Condição:** {deficiencia_valor:.1f}% de deficiência de ar")
        else:
            st.markdown("**Condição:** Estequiométrica")
        
        # Mostra o tipo de poder calorífico selecionado
        st.markdown(f"**Poder calorífico:** {tipo_calor}")
            
        st.divider()
        
        st.markdown("### ➡️ Reação Global Balanceada")
        
        # Construindo a equação da reação
        reacao = f"C<sub>{x}</sub>H<sub>{y}</sub> + {a_real:.2f}(O₂ + 3,76 N₂) → "
        
        produtos = []
        if b > 0:
            produtos.append(f"{b:.2f} CO₂")
        if co > 0:
            produtos.append(f"{co:.2f} CO")
        if carbono_solid > 0:
            produtos.append(f"{carbono_solid:.2f} C")
        if c > 0:
            produtos.append(f"{c:.2f} H₂O")
        if d > 0:
            produtos.append(f"{d:.2f} N₂")
        if o2_residual > 0:
            produtos.append(f"{o2_residual:.2f} O₂")
            
        reacao += " + ".join(produtos)
        
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
        
        # ===== CALOR DE COMBUSTÃO =====
        st.markdown("### ➡️ Calor de Combustão")
        
        col_calor1, col_calor2, col_calor3 = st.columns(3)
        
        with col_calor1:
            st.metric(
                label=f"Calor liberado",
                value=f"{calor_liberado:.1f} kJ/mol"
            )
        
        with col_calor2:
            st.metric(
                label=f"Calor liberado",
                value=f"{calor_liberado_kg:.1f} kJ/kg"
            )
        
        with col_calor3:
            st.metric(
                label=f"Combustível",
                value=f"C{'{'}{x}{'}'}H{'{'}{y}{'}'}"
            )
        
        # Informações adicionais sobre o calor
        with st.expander("📊 Detalhes do cálculo do calor"):
            st.write(f"**Entalpia de formação do combustível:** {delta_hf_combustivel:.1f} kJ/mol")
            st.write(f"**Entalpia dos produtos:** {delta_h_produtos:.1f} kJ/mol")
            st.write(f"**ΔH da combustão:** {delta_h_combustao:.1f} kJ/mol")
            st.write(f"**Massa molar do combustível:** {massa_molar:.1f} g/mol")
            
            if tipo_calor == "Poder Calorífico Superior (PCS)":
                st.success("✅ Usando H₂O(l) nos produtos (PCS)")
            else:
                st.info("ℹ️ Usando H₂O(g) nos produtos (PCI)")
        
        st.divider()
          
        # INFORMAÇÕES SOBRE AR
        st.markdown("### ➡️ Informações sobre o Ar")
        
        col_ar1, col_ar2, col_ar3, col_ar4 = st.columns(4)
        with col_ar1:
            st.metric(
                label="Ar real (mol)",
                value=f"{ar_real:.2f} mol"
            )
        with col_ar2:
            st.metric(
                label="O₂ real (mol)",
                value=f"{a_real:.2f} mol"
            )
        with col_ar3:
            st.metric(
                label="N₂ acompanhante (mol)",
                value=f"{d:.2f} mol"
            )
        with col_ar4:
            if tipo_ar == "Excesso de ar":
                st.metric(
                    label="O₂ em excesso (mol)",
                    value=f"{o2_residual:.2f} mol"
                )
            elif tipo_ar == "Deficiência de ar":
                st.metric(
                    label="Falta de O₂ (mol)",
                    value=f"{(a_teorico - a_real):.2f} mol"
                )
            else:
                st.metric(
                    label="O₂ residual",
                    value="0.00 mol"
                )
        st.divider()
        
        # INFORMAÇÕES SOBRE OS PRODUTOS
        if fator_excesso < 1:
            st.markdown("### ➡️ Produtos da Combustão Incompleta")
            col_prod1, col_prod2 = st.columns(2)
            with col_prod1:
                if co > 0:
                    st.warning(f"⚠️ **CO formado:** {co:.2f} mol")
                if carbono_solid > 0:
                    st.warning(f"⚠️ **Carbono sólido formado:** {carbono_solid:.2f} mol")
            with col_prod2:
                st.info(f"**CO₂ formado:** {b:.2f} mol")
                st.info(f"**H₂O formada:** {c:.2f} mol")
        
        st.divider()
        st.caption("💡 Nota: Em condições de deficiência de ar, a combustão é incompleta e pode formar CO e/ou carbono sólido. O calor liberado será menor.")
