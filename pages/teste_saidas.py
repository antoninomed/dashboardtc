import streamlit as st
import pandas as pd
import plotly.express as px

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Saídas | The Crew",
    layout="wide"
)

# ===================== CSS GLOBAL =====================
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    font-family: 'Segoe UI', sans-serif;
}

.header-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    padding: 25px;
    border-radius: 14px;
    color: white;
    margin-bottom: 25px;
}

.section-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-top: 10px;
    box-shadow: 0 6px 12px rgba(0,0,0,.05);
}

.section-card:hover {
    border-color: #2563eb;
    transition: 0.2s;
}

[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 900 !important;
    color: #2563eb !important;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
<div class="header-box">
    <span style="opacity:0.8; letter-spacing:1px">ANÁLISE DE SAÍDAS</span>
    <h1 style="margin:0;">Análise de Saídas</h1>
    <p style="margin-top:6px; opacity:0.9">
        Evolução de pontuação, taxa de sucesso e melhoria das saídas.
    </p>
</div>
""", unsafe_allow_html=True)

# ===================== LINKS =====================
saidas_links = {
    "Saída 1": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1008601803&single=true&output=csv",
    "Saída 2": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=2064448046&single=true&output=csv",
    "Saída 3": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1760261047&single=true&output=csv",
    "Saída 4": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1456659526&single=true&output=csv",
    "Saída 5": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1257836641&single=true&output=csv"
}

# ===================== SIDEBAR =====================
colA, colB, colC = st.columns([2,1,1])

with colA:
    saida_escolhida = st.selectbox(
        "Escolha a Saída a ser analisada:",
        list(saidas_links.keys()),
        index=0
    )

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        "nº teste": "Teste",
        "Nº Teste": "Teste",
        "pontuação": "Pontuação",
        "mudança": "Mudança",
        "resultado": "Resultado"
    }
    df.rename(columns=rename_map, inplace=True)

    return df

df = load_data(saidas_links[saida_escolhida])

# ===================== TABELA =====================
st.markdown(f"### 📋 Tabela - {saida_escolhida}")
st.dataframe(df, use_container_width=True, hide_index=True)

# ===================== EVOLUÇÃO DA PONTUAÇÃO =====================
st.markdown("### 📈 Evolução da Pontuação")

fig = px.line(
    df,
    x="Teste",
    y="Pontuação",
    markers=True,
    title=f"Evolução da Pontuação - {saida_escolhida}"
)
st.plotly_chart(fig, use_container_width=True)

# ===================== TAXA DE SUCESSO =====================
st.markdown("### 🎯 Taxa de Sucesso")

if "Resultado" in df.columns:
    sucesso = df[df["Resultado"].astype(str).str.contains("Sucesso|OK|1", case=False, na=False)]
    taxa = (len(sucesso) / len(df)) * 100 if len(df) > 0 else 0
else:
    taxa = 0

col1, col2 = st.columns(2)
with col1:
    st.metric("Tentativas", len(df))
with col2:
    st.metric("Taxa de Sucesso (%)", f"{taxa:.1f}%")

# ===================== CREW ASSISTENTE =====================
st.markdown("### 🤖 Crew Assistente — Insights")

recomendacoes = []

if taxa < 60:
    recomendacoes.append("⚠️ Taxa de sucesso baixa. Revisar estratégia e consistência da saída.")
elif taxa > 85:
    recomendacoes.append("✅ Excelente taxa de sucesso! Manter abordagem atual.")

if df["Pontuação"].std() > 10:
    recomendacoes.append("⚡ Pontuação muito instável. Trabalhar padronização da execução.")

if df["Pontuação"].mean() < df["Pontuação"].max() * 0.6:
    recomendacoes.append("🎯 Ainda há grande espaço para melhorar a média de pontuação.")

if len(recomendacoes) == 0:
    recomendacoes.append("👌 Tudo consistente até agora. Continuar monitorando.")

for r in recomendacoes:
    st.markdown(f"- {r}")
