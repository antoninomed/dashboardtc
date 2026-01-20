import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Análise de Missões FLL | The Crew",
    page_icon="🤖",
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
    margin-bottom: 14px;
}

.card:hover {
    border-color: #2563eb;
    box-shadow: 0 10px 18px -6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
    transition: 0.2s ease;
}

[data-testid="stMetricValue"] {
    font-size: 28px !important;
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
    <span style="opacity:0.8; letter-spacing:1px">ANÁLISE TÉCNICA – FUTURE LEAGUE LEGO</span>
    <h1 style="margin:0;">Análise de Missões</h1>
    <p style="margin-top:6px; opacity:0.9">
        Avaliação detalhada de desempenho, pontuação e histórico das missões testadas.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# BASE PLANILHA
# =========================
BASE_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub"
)

MISSOES = {
    "M01": "1328389352","M02": "2081596503","M03": "1851247677",
    "M04": "1520590222","M05": "1999701476","M06": "1653076161",
    "M07": "1775788177","M08": "855854989","M09": "667614461",
    "M10": "218456511","M11": "1002944230","M12": "1887688551",
    "M13": "202334414","M14": "838222531","M15": "703330322",
}

# =========================
# SELEÇÃO DE MISSÃO
# =========================
missao = st.selectbox("Selecione a Missão", list(MISSOES.keys()))

@st.cache_data
def carregar_missao(gid):
    url = f"{BASE_URL}?gid={gid}&single=true&output=csv"
    return pd.read_csv(url)

df = carregar_missao(MISSOES[missao])

# =========================
# ORGANIZAÇÃO
# =========================
df["ID Teste"] = df["ID Teste"].astype(str)
df = df.sort_values("ID Teste")

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🏁 Pontuação Máxima", int(df["Pontuação"].max()))
col2.metric("📊 Média de Pontuação", round(df["Pontuação"].mean(), 1))
col3.metric("🧪 Total de Testes", df["ID Teste"].nunique())

st.write("")

# =========================
# GRÁFICO PRINCIPAL
# =========================
st.subheader("📈 Evolução de Pontuação")

fig = px.scatter(
    df,
    x="ID Teste",
    y="Pontuação",
    title=f"Pontuação por Teste – {missao}",
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# HISTÓRICO DE MUDANÇAS
# =========================
st.subheader("🔧 Histórico Técnico de Mudanças")

mudancas = df[df["Mudança"].notna() & (df["Mudança"].astype(str).str.strip() != "")]

if mudancas.empty:
    st.info("Nenhuma mudança registrada ainda para esta missão.")
else:
    for _, row in mudancas.iterrows():
        with st.expander(f"🧪 Teste {row['ID Teste']} – Resultado: {row['Resultado']}"):
            st.markdown(f"""
            <div class="card">
                <b>🎯 Pontuação:</b> {row['Pontuação']}<br>
                <b>🔎 Tipo:</b> {row['Tipo']}<br><br>
                <b>🛠️ O que foi alterado:</b><br>
                {row['Mudança']}
            </div>
            """, unsafe_allow_html=True)

# =========================
# TIPO DE MUDANÇAS
# =========================
st.subheader("📊 Tipos de Mudança")

fig_tipo = px.histogram(
    df,
    x="Tipo",
    color="Tipo",
    text_auto=True,
    title="Distribuição de Tipos de Alteração"
)
st.plotly_chart(fig_tipo, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
