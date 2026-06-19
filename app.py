import streamlit as st
import pandas as pd
import datetime

# 1. Configuração da Página
st.set_page_config(
    page_title="Sistema de Precificação | JR",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injeção de CSS para esconder a "cara de Streamlit"
ocultar_elementos = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Ajuste para o banner azul colar no topo da tela */
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
            }
            /* Garante que o texto dos botões numéricos na barra lateral fiquem visíveis */
            [data-testid="stSidebar"] input {
                color: #0C1C4C !important;
            }
            </style>
            """
st.markdown(ocultar_elementos, unsafe_allow_html=True)

# 3. Cabeçalho Banner (Estilo Site da JR Consultoria)
st.markdown(
    """
    <div style='background-color: #0C1C4C; padding: 40px 20px; text-align: center; border-radius: 0px 0px 15px 15px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h1 style='color: #FFFFFF; margin-bottom: 0; font-weight: bold;'>Sistema Integrado de Precificação</h1>
        <p style='color: #E2E8F0; font-size: 1.1rem; margin-top: 5px;'>Geração de propostas comerciais e análise de viabilidade</p>
    </div>
    """, 
    unsafe_allow_html=True
)
# 4. Painel Lateral: Valores Base
st.sidebar.title("⚙️ Parâmetros Base")
st.sidebar.caption("Defina o piso de precificação das metodologias.")

base_marketing = st.sidebar.number_input("Plano de Marketing (R$)", value=3000, step=100)
base_processos = st.sidebar.number_input("Mapeamento de Processos (R$)", value=4000, step=100)
base_pesquisa = st.sidebar.number_input("Pesquisa de Mercado (R$)", value=3500, step=100)

st.sidebar.divider()
st.sidebar.caption(f"© {datetime.date.today().year} Consultoria de Projetos")

# 5. Sistema de Navegação em Abas
aba_calculo, aba_memoria, aba_comparacao = st.tabs(["📋 Nova Proposta", "🔍 Memória de Cálculo", "📊 Comparações de Cenário"])

# --- CONTEÚDO DA ABA 1: NOVA PROPOSTA ---
with aba_calculo:
    col_input1, col_input2 = st.columns(2, gap="large")
    
    with col_input1:
        st.subheader("Escopo do Projeto")
        metodologia = st.selectbox("Metodologia", ["Plano de Marketing", "Mapeamento de Processos", "Pesquisa de Mercado"])
        tempo = st.number_input("Tempo de Execução (Semanas)", min_value=2, max_value=24, value=6)
        consultores = st.number_input("Consultores Alocados", min_value=1, max_value=10, value=3)

    with col_input2:
        st.subheader("Variáveis Estratégicas")
        complexidade = st.radio("Grau de Complexidade", ["Baixa", "Média", "Alta"], horizontal=True, index=1)
        interesse = st.select_slider("Interesse Estratégico", options=["Baixo", "Médio", "Alto"], value="Médio")

    # Lógica Matemática Oculta
    if metodologia == "Plano de Marketing":
        preco_base = base_marketing
        fator_tempo = 1.0 + (tempo * 0.05)
    elif metodologia == "Mapeamento de Processos":
        preco_base = base_processos
        fator_tempo = 1.0 + (tempo * 0.06)
    else:
        preco_base = base_pesquisa
        fator_tempo = 8 / tempo if tempo > 0 else 1

    fator_consultores = 1.0 + (max(0, consultores - 1) * 0.10)
    
    if complexidade == "Baixa": fator_complexidade = 0.85
    elif complexidade == "Média": fator_complexidade = 1.0
    else: fator_complexidade = 1.25

    if interesse == "Alto": fator_interesse = 0.90
    elif interesse == "Médio": fator_interesse = 1.0
    else: fator_interesse = 1.15

    preco_final = preco_base * fator_tempo * fator_consultores * fator_complexidade * fator_interesse

    # Exibição do Preço Final usando a cor #0C1C4C
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color: #0C1C4C; padding: 25px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="color: #FFFFFF; font-size: 1.1rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Valor Final para o Cliente</p>
            <h1 style="color: #FFFFFF; font-size: 3.5rem; margin: 10px 0;">R$ {preco_final:,.2f}</h1>
            <p style="color: #E2E8F0; font-size: 0.9rem; margin: 0;">Proposta baseada em {tempo} semanas com {consultores} consultores.</p>
        </div>
        """.replace(",", "X").replace(".", ",").replace("X", "."),
        unsafe_allow_html=True
    )

# --- CONTEÚDO DA ABA 2: MEMÓRIA DE CÁLCULO ---
with aba_memoria:
    st.subheader("Auditoria de Fatores")
    st.write("Visão detalhada dos multiplicadores aplicados na proposta atual para prestação de contas.")
    
    tabela_dados = {
        "Variável": ["Ponto de Partida", "Prazo", "Equipe", "Complexidade", "Estratégia"],
        "Descrição": [f"Base: {metodologia}", f"{tempo} Semanas", f"{consultores} Consultores", f"Nível {complexidade}", f"Interesse {interesse}"],
        "Multiplicador": [f"R$ {preco_base:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), f"x {fator_tempo:.2f}", f"x {fator_consultores:.2f}", f"x {fator_complexidade:.2f}", f"x {fator_interesse:.2f}"]
    }
    st.table(pd.DataFrame(tabela_dados))

# --- CONTEÚDO DA ABA 3: COMPARAÇÕES ---
with aba_comparacao:
    st.subheader("Análise de Cenários Alternativos")
    st.write("Valor de venda caso o mesmo escopo técnico (tempo, equipe, complexidade) fosse aplicado em outros serviços.")
    
    outras = ["Plano de Marketing", "Mapeamento de Processos", "Pesquisa de Mercado"]
    outras.remove(metodologia)
    bases_dict = {"Plano de Marketing": base_marketing, "Mapeamento de Processos": base_processos, "Pesquisa de Mercado": base_pesquisa}
    
    col_comp1, col_comp2 = st.columns(2)
    for i, met in enumerate(outras):
        base_alt = bases_dict[met]
        if met == "Plano de Marketing": fat_t_alt = 1.0 + (tempo * 0.05)
        elif met == "Mapeamento de Processos": fat_t_alt = 1.0 + (tempo * 0.06)
        else: fat_t_alt = 8 / tempo if tempo > 0 else 1
        
        preco_alt = base_alt * fat_t_alt * fator_consultores * fator_complexidade * fator_interesse
        
        col = col_comp1 if i == 0 else col_comp2
        with col:
            st.markdown(
                f"""
                <div style="background-color: #FFFFFF; border-left: 5px solid #0C1C4C; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;">
                    <p style="color: #64748B; margin: 0; font-size: 0.9rem; font-weight: bold;">Cenário: {met}</p>
                    <h2 style="color: #0C1C4C; margin: 5px 0 0 0;">R$ {preco_alt:,.2f}</h2>
                </div>
                """.replace(",", "X").replace(".", ",").replace("X", "."),
                unsafe_allow_html=True
            )
