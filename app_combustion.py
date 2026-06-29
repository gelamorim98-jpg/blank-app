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
        
    if st.button("Calcular Estequiometria"):
        
        # CÁLCULOS ESTEQUIOMÉTRICOS (ar teórico)
        a_teorico = x + y/4  # O₂ necessário estequiométrico
        
        # Aplicando o fator de excesso/deficiência
        a_real = a_teorico * fator_excesso
        
        # b = CO₂ produzido (depende se há deficiência de ar)
        if fator_excesso < 1:
            # Em deficiência de ar, pode haver CO e/ou carbono
            # Vamos considerar a combustão incompleta com CO
            # Para simplificar: a quantidade de CO₂ é limitada pelo O₂ disponível
            # CO₂ máximo possível = O₂ disponível / 1 (para cada CO₂ precisa de 1 O₂)
            # Mas precisamos também de O₂ para H₂O
            # Simplificando: primeiro forma H₂O, depois CO₂, depois CO se ainda tiver C
            
            # O₂ disponível para oxidar C após formar H₂O
            o2_para_c = a_real - (y/4)
            
            if o2_para_c >= x:
                # O₂ suficiente para oxidar todo C a CO₂
                b = x
                # O₂ restante (se houver) - não usado
                c = y/2
                # Neste caso, não há CO
                co = 0
                # Mas pode ter O₂ residual se houver excesso
                o2_residual = max(0, o2_para_c - x)
            elif o2_para_c > 0:
                # O₂ insuficiente para oxidar todo C a CO₂
                # Primeiro, todo CO₂ que pode ser formado
                b = o2_para_c  # cada mol de CO₂ precisa de 1 mol de O₂
                # O restante do C forma CO (cada mol de CO precisa de 0.5 mol de O₂)
                co = (x - b) * 2
                # Mas precisamos verificar se há O₂ suficiente para isso
                # Na verdade, com deficiência, o cálculo é mais complexo
                # Vamos usar uma simplificação: tudo que sobra após CO₂ vira CO
                c = y/2
                o2_residual = 0
            else:
                # Sem O₂ para oxidar C (apenas H₂O)
                b = 0
                co = x * 2  # Todo carbono vira CO (ou carbono sólido, mas vamos considerar CO)
                c = y/2
                o2_residual = 0
                
            # Ajuste para quando não há O₂ suficiente nem para CO
            if co > 0 and a_real < y/4 + co/2:
                # Não há O₂ suficiente para todo CO, parte do carbono fica sólido
                # Vamos simplificar: forma o máximo de CO possível
                o2_disponivel_co = a_real - y/4
                if o2_disponivel_co > 0:
                    co = o2_disponivel_co * 2
                    b = 0
                    carbono_solid = x - co/2
                else:
                    co = 0
                    carbono_solid = x
            else:
                carbono_solid = 0
                
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
        
        st.divider()
        st.caption("💡 Nota: Em condições de deficiência de ar, a combustão é incompleta e pode formar CO e/ou carbono sólido.")
