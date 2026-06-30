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

# BOTÕES DE NAVEGAÇÃO
col_botao1, col_botao2 = st.columns(2)

with col_botao1:
    if st.button("👩‍🔬 Balanço Estequiométrico", use_container_width=True):
        st.session_state.mostrar_esteq = True
        st.session_state.mostrar_calor = False

with col_botao2:
    if st.button("🔥 Poder Calorífico", use_container_width=True):
        st.session_state.mostrar_calor = True
        st.session_state.mostrar_esteq = False

st.divider()

# FUNÇÃO PARA CALCULAR Cp (capacidade calorífica)

def calcular_cp(gas, T):
    """
    Calcula a capacidade calorífica molar (Cp) em J/mol·K
    para diferentes gases em função da temperatura (K)
    """
    # Coeficientes para Cp = a + b*T + c*T² + d*T³ (T em K)
    # Valores em J/mol·K
    coeficientes = {
        'CO2': {'a': 22.26, 'b': 5.98e-3, 'c': -3.50e-6, 'd': 7.47e-9},
        'H2O': {'a': 32.24, 'b': 1.92e-3, 'c': 1.06e-5, 'd': -3.60e-9},
        'N2': {'a': 28.90, 'b': -1.57e-3, 'c': 0.81e-5, 'd': -2.87e-9},
        'O2': {'a': 25.48, 'b': 1.52e-3, 'c': -0.72e-5, 'd': 1.31e-9},
        'CO': {'a': 28.95, 'b': -0.41e-3, 'c': 0.51e-5, 'd': -2.28e-9}
    }
    
    if gas in coeficientes:
        a = coeficientes[gas]['a']
        b = coeficientes[gas]['b']
        c = coeficientes[gas]['c']
        d = coeficientes[gas]['d']
        return a + b*T + c*T**2 + d*T**3
    else:
        return 30.0  # Valor aproximado para outros gases

def calcular_cp_medio(gas, T1, T2):
    
    n_points = 100
    dt = (T2 - T1) / n_points
    soma_cp = 0
    
    for i in range(n_points):
        T = T1 + i * dt + dt/2
        soma_cp += calcular_cp(gas, T)
    
    return soma_cp / n_points

def calcular_temperatura_adiabatica(produtos, delta_h_combustao, T_inicial=298.15):
       
    # Converter delta_h para J/mol
    delta_h = delta_h_combustao * 1000  
    
    # Método iterativo para encontrar T_ad
    T_guess = 1500  # Chute inicial (K)
    tolerancia = 1.0  # Tolerância em K
    max_iter = 50
    
    for iteracao in range(max_iter):
        # Calcular calor sensível para aquecer produtos de T_inicial até T_guess
        calor_sensivel = 0
        
        for gas, n_mols in produtos.items():
            if n_mols > 0 and gas in ['CO2', 'H2O', 'N2', 'O2', 'CO']:
                cp_medio = calcular_cp_medio(gas, T_inicial, T_guess)
                calor_sensivel += n_mols * cp_medio * (T_guess - T_inicial)
            elif n_mols > 0:
                # Para gases não listados, usar Cp aproximado
                cp_medio = 30.0  # J/mol·K
                calor_sensivel += n_mols * cp_medio * (T_guess - T_inicial)
        
        # Calcular T pela equação: delta_h = calor_sensivel
        if calor_sensivel > 0:
            T_novo = T_inicial + delta_h / (calor_sensivel / (T_guess - T_inicial))
        else:
            T_novo = T_guess * 1.5
        
        # Verificar convergência
        if abs(T_novo - T_guess) < tolerancia:
            T_ad = T_novo
            break
        
        T_guess = T_novo
    
    else:
        # Se não convergiu, usar o último valor
        T_ad = T_guess
    
    return T_ad, T_ad - 273.15

# OPÇÃO 1: BALANÇO ESTEQUIOMÉTRICO

if st.session_state.mostrar_esteq:
    st.header("👩‍🔬 Balanço Estequiométrico")
    
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
            options=["Excesso de ar", "Deficiência de ar", "Ar teórico"],
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
                step=1.0,
                format="%.1f"
            )
            fator_excesso = 1 + excesso_valor / 100
        
        elif tipo_ar == "Deficiência de ar":
            deficiencia_valor = st.number_input(
                "Digite o % de deficiência de ar:",
                min_value=1.0,
                max_value=80.0,
                value=20.0,
                step=1.0,
                format="%.1f"
            )
            fator_excesso = 1 - deficiencia_valor / 100
        
        else:  # Ar Teórico
            fator_excesso = 1.0
            st.info("✅ Condição de ar teórico (sem excesso ou deficiência de ar)")
    
    calcular_temp = st.checkbox("🌡️ Calcular Temperatura Adiabática de Chama (sem dissociação)")
    
    if st.button("Calcular Estequiometria", use_container_width=True):
        
        # CÁLCULOS ESTEQUIOMÉTRICOS (ar teórico)
        a_teorico = x + y/4  # O₂ necessário estequiométrico
        
        # Aplicando o fator de excesso/deficiência
        a_real = a_teorico * fator_excesso
        
        # CÁLCULO DA RAZÃO DE EQUIVALÊNCIA (Φ)
        if a_real > 0:
            razao_equivalencia = a_teorico / a_real
        else:
            razao_equivalencia = float('inf')
        
        if razao_equivalencia == 1.0:
            classificacao_mistura = "✅ **Mistura Estequiométrica** (Φ = 1,0)"
            cor_mistura = "#28a745"
        elif razao_equivalencia < 1.0:
            classificacao_mistura = f"🟢 **Mistura Pobre** (Φ = {razao_equivalencia:.3f} < 1,0) - Excesso de ar"
            cor_mistura = "#17a2b8"
        else:
            classificacao_mistura = f"🔴 **Mistura Rica** (Φ = {razao_equivalencia:.3f} > 1,0) - Deficiência de ar"
            cor_mistura = "#dc3545"
        
        # b = CO₂ produzido (depende se há deficiência de ar)
        if fator_excesso < 1:
            o2_para_c = a_real - (y/4)
            
            if o2_para_c >= x:
                b = x
                c = y/2
                co = 0
                o2_residual = max(0, o2_para_c - x)
              
            elif o2_para_c > 0:
                b = o2_para_c
                co = (x - b) * 2
                c = y/2
                o2_residual = 0
              
            else:
                b = 0
                co = x * 2
                c = y/2
                o2_residual = 0
                         
            # Ajuste para quando não há O₂ suficiente nem para CO
            if co > 0 and a_real < y/4 + co/2:
                o2_disponivel_co = a_real - y/4
                if o2_disponivel_co > 0:
                    co = o2_disponivel_co * 2
                    b = 0
                  
                else:
                    co = 0
                                   
        else:
            # Estequiométrico ou excesso de ar
            b = x
            c = y/2
            co = 0
            o2_residual = max(0, a_real - a_teorico)
          
        
        # N₂ produtos
        d = 3.76 * a_real
        
        # Ar real
        ar_real = a_real * 4.76
        
       # CÁLCULO DA TEMPERATURA ADIABÁTICA DE CHAMA
                
        if calcular_temp:
            # Produtos da combustão (apenas para temperatura adiabática)
            # Para ar teórico ou excesso: CO₂, H₂O, N₂, O₂
            # Para deficiência: CO₂, CO, H₂O, N₂
            produtos = {}
            
            if b > 0:
                produtos['CO2'] = b
            if co > 0:
                produtos['CO'] = co
            if c > 0:
                produtos['H2O'] = c
            if d > 0:
                produtos['N2'] = d
            if o2_residual > 0:
                produtos['O2'] = o2_residual
            
            # Entalpia de combustão (calor liberado em kJ/mol)
            # Usar valor aproximado baseado na fórmula do combustível
            # ΔH_comb ≈ - (a_teorico * 393.5 + c * 241.8 - delta_hf_combustivel)
            # Estimativa simplificada para hidrocarbonetos
            
            # Entalpia de formação aproximada do combustível (kJ/mol)
            delta_hf_combustivel = -(20*x + 10*y)  # Estimativa para alcanos
            
            # Entalpia dos produtos (CO₂ e H₂O)
            delta_hf_CO2 = -393.5  # kJ/mol
            delta_hf_H2O = -241.8  # kJ/mol (vapor)
            delta_hf_CO = -110.5   # kJ/mol
            
            delta_h_produtos = 0
            if b > 0:
                delta_h_produtos += b * delta_hf_CO2
            if co > 0:
                delta_h_produtos += co * delta_hf_CO
            if c > 0:
                delta_h_produtos += c * delta_hf_H2O
            
            delta_h_combustao = delta_h_produtos - delta_hf_combustivel
            calor_liberado = -delta_h_combustao  # kJ/mol
            
            # Calcular temperatura adiabática
            T_ad, T_ad_C = calcular_temperatura_adiabatica(produtos, calor_liberado)
            
            # Calcular também para comparação com Cp constante
            # Método simplificado (Cp constante)
            cp_produtos_total = 0
            cp_constantes = {'CO2': 44.0, 'H2O': 33.6, 'N2': 29.1, 'O2': 29.4, 'CO': 29.1}
            
            for gas, n_mols in produtos.items():
                if gas in cp_constantes:
                    cp_produtos_total += n_mols * cp_constantes[gas] / 1000  # J -> kJ
            
            if cp_produtos_total > 0:
                T_ad_simplificado = 298.15 + calor_liberado / cp_produtos_total
                T_ad_simplificado_C = T_ad_simplificado - 273.15
            else:
                T_ad_simplificado = 298.15
                T_ad_simplificado_C = 25.0
        
        # RESULTADOS
        st.divider()
        st.markdown(
            "<h2 style='text-align: center;'>Resultados do Balanço Estequiométrico</h2>",
            unsafe_allow_html=True
        )
        st.divider()
        
        st.markdown("### ➡️ Reação Global Balanceada")
        
        # Construindo a equação da reação
        reacao = f"C<sub>{x}</sub>H<sub>{y}</sub> + {a_real:.2f}(O₂ + 3,76 N₂) → "
        
        produtos_lista = []
        if b > 0:
            produtos_lista.append(f"{b:.2f} CO₂")
        if co > 0:
            produtos_lista.append(f"{co:.2f} CO")
        if c > 0:
            produtos_lista.append(f"{c:.2f} H₂O")
        if d > 0:
            produtos_lista.append(f"{d:.2f} N₂")
        if o2_residual > 0:
            produtos_lista.append(f"{o2_residual:.2f} O₂")
            
        reacao += " + ".join(produtos_lista)
        
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

        # RAZÃO DE EQUIVALÊNCIA
        
        st.markdown("### ➡️ Razão de Equivalência (Φ)")
        
        col_phi1, col_phi2, col_phi3 = st.columns([1, 2, 1])
        with col_phi2:
            st.markdown(
                f"""
                <div style='
                    background-color: {cor_mistura}20;
                    padding: 15px;
                    border-radius: 10px;
                    border: 2px solid {cor_mistura};
                    text-align: center;
                '>
                    <h3 style='color: {cor_mistura}; margin: 0;'>
                        Φ = {razao_equivalencia:.4f}
                    </h3>
                    <p style='margin: 5px 0 0 0; font-size: 16px;'>
                        {classificacao_mistura}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.divider()
        
        # TEMPERATURA ADIABÁTICA DE CHAMA
        
        if calcular_temp:
            st.markdown("### ➡️ Temperatura Adiabática de Chama (sem dissociação)")
            
            col_temp1, col_temp2 = st.columns(2)
            
            with col_temp1:
                st.metric(
                    label="Temperatura Adiabática (Cp variável)",
                    value=f"{T_ad:.1f} K",
                    delta=f"{T_ad_C:.1f} °C"
                )
            
            with col_temp2:
                st.metric(
                    label="Temperatura Adiabática (Cp constante - estimativa)",
                    value=f"{T_ad_simplificado:.1f} K",
                    delta=f"{T_ad_simplificado_C:.1f} °C"
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
                label="N₂ do ar (mol)",
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
        
        # RESUMO DOS PARÂMETROS DE COMBUSTÃO
        st.markdown("### 📊 Resumo dos Parâmetros de Combustão")
        
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        with col_res1:
            st.metric(
                label="O₂ teórico (mol)",
                value=f"{a_teorico:.2f} mol"
            )
        with col_res2:
            st.metric(
                label="O₂ real (mol)",
                value=f"{a_real:.2f} mol"
            )
        with col_res3:
            st.metric(
                label="Razão de Equivalência (Φ)",
                value=f"{razao_equivalencia:.4f}"
            )
        with col_res4:
            if razao_equivalencia == 1.0:
                st.metric(
                    label="Classificação",
                    value="Estequiométrica",
                    delta="✅ Ideal"
                )
            elif razao_equivalencia < 1.0:
                st.metric(
                    label="Classificação",
                    value="Pobre",
                    delta="🔵 Excesso de ar"
                )
            else:
                st.metric(
                    label="Classificação",
                    value="Rica",
                    delta="🔴 Deficiência de ar"
                )

# =============================================
# OPÇÃO 2: PODER CALORÍFICO
# =============================================

if st.session_state.mostrar_calor:
    st.header("🔥 Cálculo do Poder Calorífico")
    
    st.markdown("""Digite a fórmula do combustível e escolha o tipo de poder calorífico desejado.""")
    
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
            'CO2': -393.52,
            'H2O_l': -285.83,
            'H2O_g': -241.82,
            'O2': 0.0,
            'N2': 0.0
        }
        
        # Entalpia de formação do combustível
        if x == 1 and y == 4:
            delta_hf_combustivel = -74.85
            nome_combustivel = "Metano"
        elif x == 2 and y == 2:
            delta_hf_combustivel = 226.73
            nome_combustivel = "Acetileno" 
        elif x == 2 and y == 4:
            delta_hf_combustivel = 52.28
            nome_combustivel = "Etileno"  
        elif x == 2 and y == 6:
            delta_hf_combustivel = -84.68
            nome_combustivel = "Etano"
        elif x == 3 and y == 6:
            delta_hf_combustivel = 20.41
            nome_combustivel = "Propileno"
        elif x == 3 and y == 8:
            delta_hf_combustivel = -103.85
            nome_combustivel = "Propano"
        elif x == 4 and y == 10:
            delta_hf_combustivel = -126.15
            nome_combustivel = "Butano"
        elif x == 5 and y == 12:
            delta_hf_combustivel = -146.44
            nome_combustivel = "Pentano"
        elif x == 8 and y == 18:
            delta_hf_combustivel = -208.45
            nome_combustivel = "Octano Gasoso"
        elif x == 8 and y == 18:
            delta_hf_combustivel = 82.93
            nome_combustivel = "Benzeno"
        elif x == 7 and y == 16:
            delta_hf_combustivel = -187.8
            nome_combustivel = "Heptano"
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
# MENSAGEM INICIAL (quando nenhuma opção está selecionada)
# =============================================
if not st.session_state.mostrar_esteq and not st.session_state.mostrar_calor:
    st.info("👆 Selecione uma das opções acima para começar:")
    st.markdown("""
    - **Balanço Estequiométrico**: Calcule a quantidade de ar necessária, produtos formados e condições de combustão.
    - **Poder Calorífico**: Calcule o calor liberado na combustão completa do combustível.
    """)
