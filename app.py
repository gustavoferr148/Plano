import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Precificador de Projetos - JR Consultoria",
    page_icon="📊",
    layout="centered"
)

# Título do App
st.title("📊 Precificador de Projetos")
st.write("Insira as variáveis do projeto abaixo para calcular uma estimativa de preço.")

# --- PAINEL LATERAL: CONFIGURAÇÃO DE VALORES BASE ---
st.sidebar.header("⚙️ Configurações de Valores Base")
st.sidebar.write("Altere os valores padrão que servem de ponto de partida para o cálculo:")

base_marketing = st.sidebar.number_input("Preço Base: Plano de Marketing (R$)", value=3000)
base_processos = st.sidebar.number_input("Preço Base: Mapeamento de Processos (R$)", value=4000)
base_pesquisa = st.sidebar.number_input("Preço Base: Pesquisa de Mercado (R$)", value=3500)

# --- CORPO PRINCIPAL: ENTRADA DE VARIÁVEIS DO PROJETO ---
st.header("📋 Dados do Projeto")

# 1. Seleção da Metodologia
metodologia = st.selectbox(
    "Metodologia do Projeto",
    ["Plano de Marketing", "Mapeamento de Processos", "Pesquisa de Mercado"]
)

# 2. Tempo do Projeto
tempo = st.slider("Tempo de Execução (em semanas)", min_value=2, max_value=16, value=6)

# 3. Número de Consultores
consultores = st.slider("Número de Consultores Alocados", min_value=1, max_value=6, value=3)

# 4. Complexidade
complexidade = st.select_slider(
    "Grau de Complexidade",
    options=["Baixa", "Média", "Alta"],
    value="Média"
)

# 5. Interesse da JR Consultoria
interesse = st.select_slider(
    "Interesse Estratégico da JR no Projeto",
    options=["Baixo", "Médio", "Alto"],
    value="Médio"
)

# --- LÓGICA DE CÁLCULO DE PRECIFICAÇÃO ---

# Definição do preço base e fator tempo de acordo com a metodologia
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
st.subheader("💰 Estimativa de Preço Final")

# Formatação de moeda para o padrão brasileiro
preco_formatado = f"R$ {preco_final:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
st.metric(label="Preço do Projeto para o Cliente", value=preco_formatado)

# Detalhamento dos multiplicadores para transparência
with st.expander("🔍 Ver memória de cálculo e multiplicadores"):
    st.write(f"**Preço Base Selecionado:** R$ {preco_base:,.2f}")
    st.write(f"**Multiplicador de Tempo:** {fator_tempo:.2f}x")
    st.write(f"**Multiplicador de Consultores:** {fator_consultores:.2f}x")
    st.write(f"**Multiplicador de Complexidade:** {fator_complexidade:.2f}x")
    st.write(f"**Multiplicador de Interesse Estratégico:** {fator_interesse:.2f}x")
    st.caption("Fórmula aplicada: Preço Final = Base * Tempo * Consultores * Complexidade * Interesse")
  
