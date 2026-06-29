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
if "mostrar_calor" not in st.session_state:
    st.session_state.mostrar_calor = False
if "mostrar_temp" not in st.session_state:
    st.session_state.mostrar_temp = False

# BOTÕES DE NAVEGAÇÃO - ESCOLHA ENTRE AS OPÇÕES
col_botao1, col_botao2, col_botao3 = st.columns(3)

with col_botao1:
    if st.button("🔬 Balanço Estequiométrico", use_container_width=True):
        st.session_state.mostrar_esteq = True
        st.session_state.mostrar_calor = False
        st.session_state.mostrar_temp = False

with col_botao2:
    if st.button("🔥 Poder Calorífico", use_container_width=True):
        st.session_state.mostrar_calor = True
        st.session_state.mostrar_esteq = False
        st.session_state.mostrar_temp = False

with col_botao3:
    if st.button("🌡️ Temp. Chama Adiabática", use_container_width=True):
        st.session_state.mostrar_temp = True
        st.session_state.mostrar_esteq = False
        st.session_state.mostrar_calor = False

st.divider()

# =============================================
# OPÇÃO 1: BALANÇO ESTEQUIOMÉTRICO
# =============================================
if st.session_state.mostrar_esteq:
    st.header("🔬 Balanço Estequiométrico")
    
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
    
    # Opção para incluir ou não o cálculo do calor
    incluir_calor = st.checkbox("Calcular também o calor de combustão", value=False)
    
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
        
        # RESULTADOS
        st.divider()
        st.markdown(
            "<h2 style='text-align: center;'>Resultados do Balanço Estequiométrico</h2>",
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
        
        # ===== CÁLCULO DO CALOR (SE SELECIONADO) =====
        if incluir_calor:
            st.divider()
            st.markdown("### ➡️ Calor de Combustão")
            
            # Opção de PCS/PCI
            tipo_calor = st.radio(
                "Tipo de poder calorífico:",
                options=["PCS (água líquida)", "PCI (água vapor)"],
                index=0,
                horizontal=True
            )
            
            # Entalpias de formação (kJ/mol) a 25°C
            delta_hf = {
                'CO2': -393.5,
                'H2O_l': -285.8,
                'H2O_g': -241.8,
                'CO': -110.5,
                'C': 0.0,
                'O2': 0.0,
                'N2': 0.0
            }
            
            # Entalpia de formação do combustível
            if x == 1 and y == 4:
                delta_hf_combustivel = -74.8
            elif x == 2 and y == 6:
                delta_hf_combustivel = -84.7
            elif x == 3 and y == 8:
                delta_hf_combustivel = -103.8
            elif x == 4 and y == 10:
                delta_hf_combustivel = -126.1
            elif x == 5 and y == 12:
                delta_hf_combustivel = -146.8
            elif x == 6 and y == 14:
                delta_hf_combustivel = -167.2
            elif x == 7 and y == 16:
                delta_hf_combustivel = -187.8
            elif x == 8 and y == 18:
                delta_hf_combustivel = -208.4
            elif x == 10 and y == 22:
                delta_hf_combustivel = -249.6
            else:
                delta_hf_combustivel = -(20*x + 10*y)
            
            # Cálculo do calor
            delta_h_produtos = 0
            
            if b > 0:
                delta_h_produtos += b * delta_hf['CO2']
            if co > 0:
                delta_h_produtos += co * delta_hf['CO']
            if carbono_solid > 0:
                delta_h_produtos += carbono_solid * delta_hf['C']
            if c > 0:
                if tipo_calor == "PCS (água líquida)":
                    delta_h_produtos += c * delta_hf['H2O_l']
                else:
                    delta_h_produtos += c * delta_hf['H2O_g']
            
            delta_h_reagentes = delta_hf_combustivel
            delta_h_combustao = delta_h_produtos - delta_h_reagentes
            calor_liberado = -delta_h_combustao
            
            massa_molar = x*12 + y*1
            calor_liberado_kg = calor_liberado * 1000 / massa_molar
            
            col_calor1, col_calor2 = st.columns(2)
            with col_calor1:
                st.metric("Calor liberado", f"{calor_liberado:.1f} kJ/mol")
            with col_calor2:
                st.metric("Calor liberado", f"{calor_liberado_kg:.1f} kJ/kg")
            
            with st.expander("📊 Detalhes do cálculo"):
                st.write(f"**ΔHf° do combustível:** {delta_hf_combustivel:.1f} kJ/mol")
                st.write(f"**ΔH dos produtos:** {delta_h_produtos:.1f} kJ/mol")
                st.write(f"**ΔH da combustão:** {delta_h_combustao:.1f} kJ/mol")
                st.write(f"**Massa molar:** {massa_molar:.1f} g/mol")
        
        st.divider()
        st.caption("💡 Nota: Em condições de deficiência de ar, a combustão é incompleta e pode formar CO e/ou carbono sólido.")

# =============================================
# OPÇÃO 2: PODER CALORÍFICO
# =============================================
if st.session_state.mostrar_calor:
    st.header("🔥 Cálculo do Poder Calorífico")
    
    st.markdown("""
    ### Instruções
    Digite a fórmula do combustível e escolha o tipo de poder calorífico desejado.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        x = st.number_input("Número de Carbonos:", min_value=1, value=1, step=1, key="calor_x")
    with col2:
        y = st.number_input("Número de Hidrogênios:", min_value=1, value=4, step=1, key="calor_y")
    
    st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)
    
    st.divider()
    
    col_calor1, col_calor2 = st.columns(2)
    
    with col_calor1:
        tipo_calor = st.radio(
            "Tipo de poder calorífico:",
            options=["Poder Calorífico Superior (PCS)", "Poder Calorífico Inferior (PCI)"],
            index=0,
            horizontal=True
        )
    
    with col_calor2:
        st.caption("📌 **PCS**: Água líquida nos produtos")
        st.caption("📌 **PCI**: Água vapor nos produtos")
    
    if st.button("Calcular Poder Calorífico", use_container_width=True):
        
        # Entalpias de formação (kJ/mol) a 25°C
        delta_hf = {
            'CO2': -393.5,
            'H2O_l': -285.8,
            'H2O_g': -241.8,
            'O2': 0.0,
            'N2': 0.0
        }
        
        # Entalpia de formação do combustível
        if x == 1 and y == 4:
            delta_hf_combustivel = -74.8
            nome_combustivel = "Metano"
        elif x == 2 and y == 6:
            delta_hf_combustivel = -84.7
            nome_combustivel = "Etano"
        elif x == 3 and y == 8:
            delta_hf_combustivel = -103.8
            nome_combustivel = "Propano"
        elif x == 4 and y == 10:
            delta_hf_combustivel = -126.1
            nome_combustivel = "Butano"
        elif x == 5 and y == 12:
            delta_hf_combustivel = -146.8
            nome_combustivel = "Pentano"
        elif x == 6 and y == 14:
            delta_hf_combustivel = -167.2
            nome_combustivel = "Hexano"
        elif x == 7 and y == 16:
            delta_hf_combustivel = -187.8
            nome_combustivel = "Heptano"
        elif x == 8 and y == 18:
            delta_hf_combustivel = -208.4
            nome_combustivel = "Octano"
        elif x == 10 and y == 22:
            delta_hf_combustivel = -249.6
            nome_combustivel = "Decano"
        else:
            delta_hf_combustivel = -(20*x + 10*y)
            nome_combustivel = f"C{'{'}{x}{'}'}H{'{'}{y}{'}'}"
        
        # Estequiometria para combustão completa
        a = x + y/4  # O₂ necessário
        b = x  # CO₂ produzido
        c = y/2  # H₂O produzida
        
        # Cálculo do calor de combustão (Lei de Hess)
        delta_h_produtos = b * delta_hf['CO2']
        
        # Define o valor da entalpia da água baseado no tipo selecionado
        if tipo_calor == "Poder Calorífico Superior (PCS)":
            delta_h_produtos += c * delta_hf['H2O_l']
            estado_agua = "líquida"
            delta_hf_agua = delta_hf['H2O_l']
        else:
            delta_h_produtos += c * delta_hf['H2O_g']
            estado_agua = "vapor"
            delta_hf_agua = delta_hf['H2O_g']
        
        delta_h_reagentes = delta_hf_combustivel
        delta_h_combustao = delta_h_produtos - delta_h_reagentes
        calor_liberado = -delta_h_combustao  # kJ/mol
        
        # Conversão para kJ/kg
        massa_molar = x*12 + y*1  # g/mol
        calor_liberado_kg = calor_liberado * 1000 / massa_molar  # kJ/kg
        
        # Conversão para MJ/kg (mais comum para combustíveis)
        calor_liberado_MJkg = calor_liberado_kg / 1000
        
        # RESULTADOS
        st.divider()
        st.markdown(
            "<h2 style='text-align: center;'>Resultados do Poder Calorífico</h2>",
            unsafe_allow_html=True
        )
        st.divider()
        
        # Informações do combustível
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Combustível", f"C{'{'}{x}{'}'}H{'{'}{y}{'}'}")
        with col_info2:
            st.metric("Nome", nome_combustivel)
        with col_info3:
            st.metric("Massa molar", f"{massa_molar:.1f} g/mol")
        
        st.divider()
        
        # Reação de combustão
        st.markdown("### ➡️ Reação de Combustão Completa")
        reacao = f"C<sub>{x}</sub>H<sub>{y}</sub> + {a:.2f} O₂ → {b:.2f} CO₂ + {c:.2f} H₂O({estado_agua})"
        
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
        
        # Resultados do poder calorífico
        st.markdown("### ➡️ Poder Calorífico")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(
                label=f"{tipo_calor}",
                value=f"{calor_liberado:.1f} kJ/mol"
            )
        with col_res2:
            st.metric(
                label=f"{tipo_calor}",
                value=f"{calor_liberado_kg:.1f} kJ/kg"
            )
        with col_res3:
            st.metric(
                label=f"{tipo_calor}",
                value=f"{calor_liberado_MJkg:.2f} MJ/kg"
            )
        
        st.divider()
        
        # Detalhes do cálculo
        with st.expander("📊 Detalhes do Cálculo Termodinâmico"):
            st.write("**Dados utilizados (ΔHf° a 25°C):**")
            st.write(f"- Combustível (C{'{'}{x}{'}'}H{'{'}{y}{'}'}): {delta_hf_combustivel:.1f} kJ/mol")
            st.write(f"- CO₂(g): {delta_hf['CO2']:.1f} kJ/mol")
            if tipo_calor == "Poder Calorífico Superior (PCS)":
                st.write(f"- H₂O(l): {delta_hf['H2O_l']:.1f} kJ/mol")
            else:
                st.write(f"- H₂O(g): {delta_hf['H2O_g']:.1f} kJ/mol")
            st.write(f"- O₂(g): 0.0 kJ/mol")
            
            st.write("\n**Cálculo pela Lei de Hess:**")
            st.write(f"ΔH_comb = Σ(n×ΔHf°_produtos) - Σ(n×ΔHf°_reagentes)")
            st.write(f"ΔH_comb = ({b:.2f}×{delta_hf['CO2']:.1f} + {c:.2f}×{delta_hf_agua:.1f}) - ({delta_hf_combustivel:.1f})")
            st.write(f"ΔH_comb = {delta_h_produtos:.1f} - ({delta_hf_combustivel:.1f}) = {delta_h_combustao:.1f} kJ/mol")
            st.write(f"**Calor liberado = {calor_liberado:.1f} kJ/mol**")
        
        st.divider()
        st.caption("💡 O poder calorífico é o calor liberado na combustão completa de 1 mol ou 1 kg de combustível.")

# =============================================
# OPÇÃO 3: TEMPERATURA DE CHAMA ADIABÁTICA
# =============================================
if st.session_state.mostrar_temp:
    st.header("🌡️ Temperatura de Chama Adiabática")
    
    st.markdown("""
    ### Instruções
    A temperatura de chama adiabática é a temperatura máxima alcançada quando todo o calor liberado na combustão 
    é utilizado para aquecer os produtos, sem perdas de calor para o ambiente.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        x = st.number_input("Número de Carbonos:", min_value=1, value=1, step=1, key="temp_x")
    with col2:
        y = st.number_input("Número de Hidrogênios:", min_value=1, value=4, step=1, key="temp_y")
    
    st.write(f"**Combustível:** C<sub>{x}</sub>H<sub>{y}</sub>", unsafe_allow_html=True)
    
    st.divider()
    
    col_temp1, col_temp2 = st.columns(2)
    
    with col_temp1:
        # Condições iniciais
        T_inicial = st.number_input(
            "Temperatura inicial dos reagentes (°C):",
            min_value=0,
            max_value=500,
            value=25,
            step=5
        )
        
        tipo_ar_temp = st.radio(
            "Condição de ar:",
            options=["Estequiométrico", "Excesso de ar"],
            index=0,
            horizontal=True
        )
    
    with col_temp2:
        if tipo_ar_temp == "Excesso de ar":
            excesso_temp = st.number_input(
                "% de excesso de ar:",
                min_value=1.0,
                max_value=200.0,
                value=20.0,
                step=5.0,
                format="%.1f"
            )
            fator_excesso_temp = 1 + excesso_temp / 100
        else:
            fator_excesso_temp = 1.0
            st.info("✅ Condição estequiométrica")
        
        # Opção para considerar ou não dissociação
        considerar_dissociacao = st.checkbox(
            "Considerar dissociação (aproximação)",
            value=False,
            help="Em temperaturas muito altas (>2000°C), a dissociação dos produtos pode ocorrer"
        )
    
    if st.button("Calcular Temperatura de Chama", use_container_width=True):
        
        # CÁLCULOS ESTEQUIOMÉTRICOS
        a_teorico = x + y/4
        a_real = a_teorico * fator_excesso_temp
        
        # Para temperatura adiabática, consideramos combustão completa
        # (assumindo que há oxigênio suficiente)
        if a_real >= a_teorico:
            b = x  # CO₂
            c = y/2  # H₂O
            co = 0
            o2_residual = a_real - a_teorico
            carbono_solid = 0
        else:
            # Se houver deficiência, não calculamos (seria combustão incompleta)
            st.error("⚠️ A temperatura de chama adiabática é calculada para combustão completa. Use excesso de ar ou condição estequiométrica.")
            st.stop()
        
        # N₂
        d = 3.76 * a_real
        
        # Entalpias de formação (kJ/mol) a 25°C
        delta_hf = {
            'CO2': -393.5,
            'H2O_g': -241.8,
            'O2': 0.0,
            'N2': 0.0
        }
        
        # Entalpia de formação do combustível
        if x == 1 and y == 4:
            delta_hf_combustivel = -74.8
            nome_combustivel = "Metano"
        elif x == 2 and y == 6:
            delta_hf_combustivel = -84.7
            nome_combustivel = "Etano"
        elif x == 3 and y == 8:
            delta_hf_combustivel = -103.8
            nome_combustivel = "Propano"
        elif x == 4 and y == 10:
            delta_hf_combustivel = -126.1
            nome_combustivel = "Butano"
        elif x == 5 and y == 12:
            delta_hf_combustivel = -146.8
            nome_combustivel = "Pentano"
        elif x == 6 and y == 14:
            delta_hf_combustivel = -167.2
            nome_combustivel = "Hexano"
        elif x == 7 and y == 16:
            delta_hf_combustivel = -187.8
            nome_combustivel = "Heptano"
        elif x == 8 and y == 18:
            delta_hf_combustivel = -208.4
            nome_combustivel = "Octano"
        elif x == 10 and y == 22:
            delta_hf_combustivel = -249.6
            nome_combustivel = "Decano"
        else:
            delta_hf_combustivel = -(20*x + 10*y)
            nome_combustivel = f"C{'{'}{x}{'}'}H{'{'}{y}{'}'}"
        
        # Calor de combustão a 25°C (PCI - água vapor)
        delta_h_produtos_25 = b * delta_hf['CO2'] + c * delta_hf['H2O_g']
        delta_h_combustao = delta_h_produtos_25 - delta_hf_combustivel
        calor_liberado = -delta_h_combustao  # kJ/mol
        
        # Capacidades caloríficas médias (kJ/mol·K) em função da temperatura
        # Aproximações para altas temperaturas
        def cp_CO2(T):
            # T em Kelvin
            return 0.044 + 0.000008 * (T - 298)  # kJ/mol·K
        
        def cp_H2O(T):
            return 0.033 + 0.000007 * (T - 298)
        
        def cp_N2(T):
            return 0.029 + 0.000003 * (T - 298)
        
        def cp_O2(T):
            return 0.029 + 0.000004 * (T - 298)
        
        # Cálculo da temperatura adiabática
        # Método iterativo: ΔH_comb = Σ(n_i * ∫Cp_i dT) de T0 até T_adia
        
        T0 = T_inicial + 273.15  # Converter para Kelvin
        
        # Função para calcular o calor necessário para aquecer os produtos até T
        def calor_aquecimento(T):
            calor = 0
            calor += b * (cp_CO2(T) * (T - T0))
            calor += c * (cp_H2O(T) * (T - T0))
            calor += d * (cp_N2(T) * (T - T0))
            if o2_residual > 0:
                calor += o2_residual * (cp_O2(T) * (T - T0))
            return calor
        
        # Método de iteração para encontrar T_adia
        # Estimativa inicial
        T_adia = T0 + 1000  # 1000 K acima da temperatura inicial
        
        # Iteração (método de Newton simplificado)
        for _ in range(50):
            calor_necessario = calor_aquecimento(T_adia)
            erro = calor_necessario - calor_liberado
            
            if abs(erro) < 0.1:  # Precisão de 0.1 kJ
                break
            
            # Derivada numérica
            dT = 10  # K
            calor_necessario2 = calor_aquecimento(T_adia + dT)
            derivada = (calor_necessario2 - calor_necessario) / dT
            
            if derivada != 0:
                T_adia = T_adia - erro / derivada
            else:
                break
        
        # Ajuste para dissociação (se selecionado)
        if considerar_dissociacao and T_adia > 2200:
            # Correção aproximada para dissociação
            # A dissociação reduz a temperatura em cerca de 5-10%
            fator_dissociacao = 1 - 0.05 * (T_adia - 2200) / 1000
            T_adia_diss = T_adia * max(fator_dissociacao, 0.85)
            T_adia_final = T_adia_diss
            dissociacao_aplicada = True
        else:
            T_adia_final = T_adia
            dissociacao_aplicada = False
        
        # RESULTADOS
        st.divider()
        st.markdown(
            "<h2 style='text-align: center;'>Temperatura de Chama Adiabática</h2>",
            unsafe_allow_html=True
        )
        st.divider()
        
        # Informações do combustível
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Combustível", f"C{'{'}{x}{'}'}H{'{'}{y}{'}'}")
        with col_info2:
            st.metric("Nome", nome_combustivel)
        with col_info3:
            if tipo_ar_temp == "Estequiométrico":
                st.metric("Condição", "Estequiométrica")
            else:
                st.metric("Condição", f"{excesso_temp:.1f}% excesso de ar")
        
        st.divider()
        
        # Reação de combustão
        st.markdown("### ➡️ Reação de Combustão")
        reacao = f"C<sub>{x}</sub>H<sub>{y}</sub> + {a_real:.2f}(O₂ + 3,76 N₂) → "
        produtos = []
        if b > 0:
            produtos.append(f"{b:.2f} CO₂")
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
               
