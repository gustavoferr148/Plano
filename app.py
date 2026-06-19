import streamlit as st
import pandas as pd
import datetime

# 1. Configuração da Página para um layout mais profissional
st.set_page_config(
    page_title="Portal de Precificação | JR Consultoria",
    page_icon="📊",
    layout="wide"
)

# 2. Rodapé Profissional
footer_text = f"© {datetime.date.today().year} JR Consultoria | Curitiba, Paraná, Brasil | UFPR"
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: grey;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
    }
    </style>
    <div class="footer">
        <p>{}</p>
    </div>
    """.format(footer_text),
    unsafe_allow_html=True,
)

# 3. Cabeçalho Profissional com Logotipo Fictício
header_col1, header_col2 = st.columns([1, 6])
with header_col1:
    # st.image("logo_jr_consultoria.png") # Para uma imagem real
    st.markdown(
        """
        <style>
        .logo-text {
            color: #2F80ED;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
        }
        </style>
        <div class="logo-text">
            JR
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_col2:
    st.title("📊 Portal de Precificação de Projetos")
    st.write("Um ambiente profissional para gerar propostas comerciais precisas.")

# 4. PAINEL LATERAL: CONFIGURAÇÃO DE VALORES BASE
st.sidebar.markdown(
    """
    <style>
    .sidebar-header {
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    </style>
    <div class="sidebar-header">
        🛠 Configurações de Valores Base
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.write("Defina os preços de partida para cada metodologia. Eles servem de base para o cálculo.")

base_marketing = st.sidebar.number_input("Preço Base: Plano de Marketing (R$)", value=3000)
base_processos = st.sidebar.number_input("Preço Base: Mapeamento de Processos (R$)", value=4000)
base_pesquisa = st.sidebar.number_input("Preço Base: Pesquisa de Mercado (R$)", value=3500)

st.sidebar.divider()
st.sidebar.caption("UFPR - JR Consultoria")

# 5. CORPO PRINCIPAL: ENTRADA DE VARIÁVEIS DO PROJETO EM COLUNAS
input_section_container = st.container()
with input_section_container:
    st.header("📋 Dados do Projeto")
    st.write("Forneça os detalhes do projeto para calcular a proposta.")

    # Criar colunas para organizar os inputs
    input_col1, input_col2 = st.columns([1, 1])

    with input_col1:
        st.subheader("1. Escopo e Equipe")
        metodologia = st.selectbox(
            "Metodologia do Projeto",
            ["Plano de Marketing", "Mapeamento de Processos", "Pesquisa de Mercado"]
        )
        tempo = st.slider("Tempo de Execução (em semanas)", min_value=2, max_value=16, value=6, help="Tempo total do projeto.")
        consultores = st.slider("Número de Consultores Alocados", min_value=1, max_value=6, value=3, help="Tamanho da equipe.")

    with input_col2:
        st.subheader("2. Complexidade e Interesse")
        complexidade = st.select_slider(
            "Grau de Complexidade",
            options=["Baixa", "Média", "Alta"],
            value="Média",
            help="Quão complexo é o projeto."
        )
        interesse = st.select_slider(
            "Interesse Estratégico da JR no Projeto",
            options=["Baixo", "Médio", "Alto"],
            value="Médio",
            help="Quão importante este projeto é para a consultoria."
        )

# 6. LÓGICA DE CÁLCULO DE PRECIFICAÇÃO (Copiar da lógica anterior)
if metodologia == "Plano de Marketing":
    preco_base = base_marketing
    # Relação direta: cada semana adicional adiciona uma taxa sobre o preço base
    fator_tempo = 1.0 + (tempo * 0.05)

elif metodologia == "Mapeamento de Processos":
    preco_base = base_processos
    # Relação direta: processos mais longos demandam mais reuniões e mapeamentos
    fator_tempo = 1.0 + (tempo * 0.06)

else:  # Pesquisa de Mercado
    preco_base = base_pesquisa
    # Relação INVERSA: prazos mais curtos exigem esforço concentrado/urgência, encarecendo o projeto
    # Considera-se 8 semanas como o tempo padrão ideal (fator 1.0)
    semanas_padrao = 8
    fator_tempo = semanas_padrao / tempo

# Fator Consultores (Acréscimo por consultor acima de um patamar mínimo)
# Exemplo: Cada consultor a partir do 2º adiciona 10% de custo operacional ao preço base
fator_consultores = 1.0 + (max(0, consultores - 1) * 0.10)

# Fator Complexidade
if complexidade == "Baixa":
    fator_complexidade = 0.85
elif complexidade == "Média":
    fator_complexidade = 1.0
else:  # Alta
    fator_complexidade = 1.25

# Fator Interesse Estratégico
# Em Empresas Juniores, um alto interesse pode significar aplicar um desconto para ganhar portfólio
# Um baixo interesse pode aplicar uma margem maior para valer a pena a alocação
if interesse == "Alto":
    fator_interesse = 0.90  # 10% de desconto estratégico
elif interesse == "Médio":
    fator_interesse = 1.0
else:  # Baixo
    fator_interesse = 1.15  # 15% de acréscimo

# --- CÁLCULO FINAL ---
preco_final = preco_base * fator_tempo * fator_consultores * fator_complexidade * fator_interesse

# --- EXIBIÇÃO DOS RESULTADOS ---
st.markdown("---")
result_container = st.container()
with result_container:
    st.subheader("💰 Proposta Gerada")
    st.write("Abaixo está a estimativa de preço final para o cliente.")

    # Criar um cartão de preço de grande visibilidade com CSS inline para o tema escuro
    st.markdown(
        f"""
        <style>
        .price-card {{
            background-color: rgba(47, 128, 237, 0.1);
            color: #2F80ED;
            border: 2px solid #2F80ED;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-top: 20px;
        }}
        .price-header {{
            font-size: 1.2rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .price-value {{
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .price-status {{
            font-size: 1rem;
            color: #2F80ED;
            opacity: 0.8;
        }}
        </style>
        <div class="price-card">
            <div class="price-header">PREÇO DO PROJETO PARA O CLIENTE</div>
            <div class="price-value">R$ {preco_final:,.2f}</div>
            <div class="price-status">Proposta Gerada</div>
        </div>
        """.replace(",", "X").replace(".", ",").replace("X", "."),
        unsafe_allow_html=True,
    )

# 7. Memória de Cálculo e Multiplicadores em uma Tabela Profissional
with st.expander("🔍 Ver memória de cálculo e multiplicadores"):
    st.write("Abaixo está a quebra dos multiplicadores aplicados ao preço base.")

    # Criar um DataFrame para exibição tabular limpa
    multiplicadores = pd.DataFrame({
        "Fator de Multiplicação": ["Preço Base", "Tempo", "Consultores", "Complexidade", "Interesse Estratégico"],
        "Valor Aplicado": [f"R$ {preco_base:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), f"{fator_tempo:.2f}x", f"{fator_consultores:.2f}x", f"{fator_complexidade:.2f}x", f"{fator_interesse:.2f}x"],
        "Descrição": [f"Preço de partida para {metodologia}", "Impacto do tempo total do projeto", "Impacto da equipe alocada", f"Impacto da complexidade {complexidade}", f"Impacto do interesse estratégico {interesse}"]
    })

    # Exibir o DataFrame com largura total e formatação
    st.dataframe(multiplicadores, use_container_width=True, hide_index=True)

    st.caption("Fórmula aplicada: Preço Final = Base * Fator_Tempo * Fator_Consultores * Fator_Complexidade * Fator_Interesse")

# 8. NOVA SEÇÃO: COMPARAÇÃO RÁPIDA (Recurso Profissional Sugerido)
st.divider()
comparison_section = st.container()
with comparison_section:
    st.header("📊 Comparação Rápida")
    st.write("Abaixo estão os preços estimados para as outras metodologias com as mesmas variáveis de projeto.")

    # Criar colunas para cada metodologia de comparação
    comp_col1, comp_col2 = st.columns(2)

    # Função auxiliar para calcular o preço final para uma metodologia alternativa
    def calcular_preco_alternativo(metodologia_alt, base_alt):
        if metodologia_alt == "Plano de Marketing":
            fator_tempo_alt = 1.0 + (tempo * 0.05)
        elif metodologia_alt == "Mapeamento de Processos":
            fator_tempo_alt = 1.0 + (tempo * 0.06)
        else:
            fator_tempo_alt = 8 / tempo

        # Os outros fatores são os mesmos
        preco_final_alt = base_alt * fator_tempo_alt * fator_consultores * fator_complexidade * fator_interesse
        return preco_final_alt

    # Filtrar as metodologias de comparação
    outras_metodologias = ["Plano de Marketing", "Mapeamento de Processos", "Pesquisa de Mercado"]
    outras_metodologias.remove(metodologia)
    bases = {"Plano de Marketing": base_marketing, "Mapeamento de Processos": base_processos, "Pesquisa de Mercado": base_pesquisa}

    for i, met in enumerate(outras_metodologias):
        col = comp_col1 if i == 0 else comp_col2
        with col:
            preco_alt = calcular_preco_alternativo(met, bases[met])
            st.markdown(
                f"""
                <style>
                .comp-card {{
                    background-color: rgba(47, 128, 237, 0.05);
                    border: 1px solid rgba(47, 128, 237, 0.3);
                    padding: 15px;
                    border-radius: 10px;
                    margin-top: 10px;
                }}
                .comp-header {{
                    font-size: 1rem;
                    font-weight: bold;
                    color: #2F80ED;
                }}
                .comp-value {{
                    font-size: 1.8rem;
                    font-weight: bold;
                    color: #2F80ED;
                }}
                </style>
                <div class="comp-card">
                    <div class="comp-header">Precificação para {met}</div>
                    <div class="comp-value">R$ {preco_alt:,.2f}</div>
                </div>
                """.replace(",", "X").replace(".", ",").replace("X", "."),
                unsafe_allow_html=True,
            )
