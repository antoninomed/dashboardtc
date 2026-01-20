import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Estabilidade & Velocidade | The Crew",
    page_icon="⚙️",
    layout="wide"
)

# =========================
# CSS MODERNO
# =========================
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

.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 10px;
}

.card:hover {
    border-color: #2563eb;
    box-shadow: 0 10px 18px -6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
    transition: 0.2s ease;
}

[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 900 !important;
    color: #2563eb !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="header-box">
    <span style="opacity:0.8; letter-spacing:1px">ANÁLISE DE ESTABILIDADE E TEMPO</span>
    <h1 style="margin:0;">Estabilidade + Velocidade</h1>
    <p style="margin-top:6px; opacity:0.9">
        Avaliação de estabilidade do robô considerando velocidade do movimento, guinada e tempo de execução.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# CARREGAR PLANILHA
# =========================
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1610789898&single=true&output=csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# =========================
# VALIDAR COLUNAS
# =========================
required_cols = [
    "Teste","Velocidade","Distância Percorrida (mm)",
    "Distância Alvo (mm)","Erro de Movimento (mm)",
    "Guinada Final","Erro de Guinada","Tempo"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"❌ Estão faltando colunas na planilha: {missing}")
    st.stop()

# =========================
# TRATAR DADOS
# =========================
num_cols = [
    "Velocidade","Distância Percorrida (mm)","Distância Alvo (mm)",
    "Erro de Movimento (mm)","Guinada Final","Erro de Guinada","Tempo"
]

for c in num_cols:
    df[c] = (
        df[c].astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
    )
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=["Velocidade","Erro de Movimento (mm)","Erro de Guinada","Tempo"])

# =========================
# CÁLCULOS
# =========================
summary = df.groupby("Velocidade").agg(
    Erro_Medio_Mov=("Erro de Movimento (mm)", "mean"),
    Variacao_Mov=("Erro de Movimento (mm)", "std"),
    Erro_Medio_Guinada=("Erro de Guinada", "mean"),
    Variacao_Guinada=("Erro de Guinada", "std"),
    Tempo_Medio=("Tempo","mean"),
    Tempo_Minimo=("Tempo","min"),
    Tempo_Maximo=("Tempo","max"),
    Testes=("Teste", "count")
).reset_index().fillna(0)

summary["Score_Estabilidade"] = (
    summary["Erro_Medio_Mov"].abs()
    + summary["Variacao_Mov"]
    + summary["Erro_Medio_Guinada"].abs()
    + summary["Variacao_Guinada"]
)

summary["Score_Desempenho"] = (
    summary["Score_Estabilidade"] * 0.7
    + summary["Tempo_Medio"] * 0.3
)

vel_estavel = summary.sort_values("Score_Estabilidade").iloc[0]
vel_rapida = summary.sort_values("Tempo_Medio").iloc[0]
vel_melhor_geral = summary.sort_values("Score_Desempenho").iloc[0]

# GRÁFICOS
# =========================
st.subheader("📊 Ranking de Performance")

with st.container():
    fig = px.scatter(
        summary,
        x="Velocidade",
        y="Score_Desempenho",
        size="Testes",
        color="Tempo_Medio",
        title="Desempenho Geral (Menor é Melhor)"
    )
    st.plotly_chart(fig, use_container_width=True)

col4, col5 = st.columns(2)

with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    fig2 = px.bar(summary, x="Velocidade", y="Tempo_Medio", title="⏱️ Tempo Médio por Velocidade")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    fig3 = px.bar(summary, x="Velocidade", y="Score_Estabilidade", title="🎯 Estabilidade por Velocidade")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TABELA FINAL
# =========================
st.subheader("📋 Tabela")
st.dataframe(summary.style.format(precision=2), use_container_width=True, hide_index=True)
