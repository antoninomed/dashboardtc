import streamlit as st
from streamlit import switch_page
# Configuração da página (Deve ser a primeira linha)
st.set_page_config(
    page_title="The Crew | Painel de Testes",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== ESTILIZAÇÃO CSS CUSTOMIZADA ======
st.markdown("""
    <style>
    /* Importação de fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo da aplicação */
    .stApp {
        background-color: #f8fafc;
    }

    /* Esconder o menu padrão do Streamlit para parecer um App real */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Customização do Header */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Estilização dos Cards de Teste */
    .test-card {
        background: white;
        padding: 0px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 380px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
    }

    .test-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #2563eb;
    }

    .card-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 12px 12px 0 0;
    }

    .card-content {
        padding: 1.2rem;
        flex-grow: 1;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }

    .card-text {
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* Estilo das métricas (KPIs) */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #2563eb !important;
    }
    
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
            
    </style>
    """, unsafe_allow_html=True)

# ====== CABEÇALHO ======
st.markdown("""
    <div class="main-header">
        <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; opacity: 0.8;">Dashboard TC 2026</span>
        <h1 style="margin:0; font-weight:800;">Painel de Testes The Crew</h1>
        <p style="opacity: 0.9; margin-top: 5px;">Análise de dadose visualização gráfica para melhora de desempenho</p>
    </div>
    """, unsafe_allow_html=True)

# ====== KPIs EM COLUNAS ======
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Tipos de Teste", "12", help="Categorias ativas")
with col2:
    st.metric("✅ Concluídos", "1.378", "+12%")
with col3:
    st.metric("⚙️ Melhorias", "142", "Ativas")

st.write("##")

# ====== GRID DE TESTES ======
st.subheader("🛠️ Testes Disponíveis")

testes = [
    {
        "imagem": "https://assets.education.lego.com/v3/assets/blt293eea581807678a/blt20b62d8158413a83/5ec7c6bffc3b8f0fa6d04d7f/curved-move-connect.png?locale=pt-br",
        "titulo": "Parâmetros PID",
        "descricao": "Otimização de KP, KI e KD para controle preciso dos giros e correção de erro.",
        "tag": "Movimento"
    },
    {
        "imagem": "https://img.freepik.com/vetores-premium/linha-reta-do-inicio-ao-fim-dos-pontos-simbolo-da-direcao-objetivo-alvo-caminho-curto-desafio-facil_254622-847.jpg",
        "titulo": "Estabilidade de Reta",
        "descricao": "Avaliação de variação de movimento e estabilidade de frenagem em movimentos retos.",
        "tag": "Movimento"
    },
    {
        "imagem": "https://d2nmr6p48f8xwg.cloudfront.net/content_pictures/9037/3dc7cdd947e9c50ee5253f8537a23bff/3526-who-lived-here-bags-13-and-14-first-lego-league-2025-2026-unearthed.png",
        "titulo": "Missões",
        "descricao": "Verificar e registrar melhorias na realização das missões.",
        "tag": "Desempenho"
    },
    {
        "imagem": "https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltf76076ba4de385b1/5ec63928bda9fc0fb1cdaeb7/turnusingsensorconnectjpg.png?locale=es-es",
        "titulo": "Análise de Giro",
        "descricao": "Comparativo entre giro simples vs giro com giroscópio.",
        "tag": "Movimento"
    },
    {
        "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9Z3xafAvuz-c7Oihi9TuuTzOcE8WusVyvfQ&s",
        "titulo": "Rounds",
        "descricao": "Simulação e testes dos rounds nos 2 minutos e 30 segundos.",
        "tag": "Desempenho"
    },
    {
        "imagem": "https://themomentmakers.org/wp-content/uploads/2021/09/dscf6064.png",
        "titulo": "Motores",
        "descricao": "Testes para verificar integridade e paridade dos motores.",
        "tag": "Componentes"
    },
    {
        "imagem": "https://themomentmakers.org/wp-content/uploads/2021/09/dscf6064.png",
        "titulo": "Saídas",
        "descricao": "Testes para verificar integridade e paridade dos motores.",
        "tag": "Desempenho"
    }
]




page_map = {
    "Parâmetros PID": "pages/teste_parametrospid.py",
    "Estabilidade de Reta": "pages/teste_reta.py",
    "Missões": "pages/teste_missoes.py",
    "Análise de Giro": "pages/teste_giro.py",
    "Rounds": "pages/teste_rounds.py",
    "Motores": "pages/teste_motores.py",
    "Saídas": "pages/teste_saidas.py",
}

# Gerando o grid dinamicamente
cols = st.columns(4)
for i, teste in enumerate(testes):
    with cols[i % 4]:
        if st.button(f"Abrir {teste['titulo']}", key=f"btn_{i}", use_container_width=True):
            st.switch_page(page_map[teste["titulo"]])

        st.markdown(f"""
            <div class="test-card">
                <img src="{teste['imagem']}" class="card-img">
                <div class="card-content">
                    <span style="background:#e2e8f0; color:#1e3a8a; padding:2px 8px;
                    border-radius:10px; font-size:0.7rem; font-weight:bold;">
                        {teste['tag']}
                    </span>
                    <div class="card-title" style="margin-top:10px;">{teste['titulo']}</div>
                    <div class="card-text">{teste['descricao']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)