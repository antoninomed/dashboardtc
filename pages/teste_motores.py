import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="Motor Analysis | The Crew", layout="wide")

# =========================================
# CSS
# =========================================
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

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="header-box">
    <span style="opacity:0.8; letter-spacing:1px">ANÁLISE DE MOTORES</span>
    <h1 style="margin:0;">Monitoramento e Precisão dos Motores</h1>
    <p style="margin-top:6px; opacity:0.9">
        Avaliação de estabilidade, erro médio, tendência e alinhamento com alvo usando dados reais.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1089137814&single=true&output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()   # limpa espaços
    return df

df = load_data()

# Limpa nomes das colunas
df.columns = df.columns.str.strip()

# ==== ARRUMA PRIMEIRA COLUNA ====
first_col = df.columns[0]
df.rename(columns={first_col: "Rotacao"}, inplace=True)

# Converte "Rotação 1" → 1
df["Rotacao"] = df["Rotacao"].astype(str).str.extract(r'(\d+)').astype(int)

# ==== ARRUMA MOTORES ====
motores = [c for c in df.columns if "Motor" in c]

for m in motores:
    df[m] = (
        df[m]
        .astype(str)
        .str.replace("º","", regex=False)
        .str.replace("°","", regex=False)
        .astype(int)
    )

# Garante coluna Alvo numérica
df["Alvo"] = df["Alvo"].astype(int)
# =========================================
# SIDEBAR
# =========================================
st.sidebar.header("🔎 Filtros")

total = len(df)
inicio = st.sidebar.slider("Início da Rotação", 1, total, 1)
fim = st.sidebar.slider("Fim da Rotação", 1, total, total)

df_filtrado = df.iloc[inicio-1:fim]

# =========================================
# TABELA
# =========================================
st.markdown("### 📋 Leituras dos Motores (dados reais)")
st.dataframe(df_filtrado, hide_index=True, use_container_width=True)

# =========================================
# GRÁFICO PRINCIPAL
# =========================================
st.markdown("### 📈 Alinhamento dos Motores com o Alvo")

df_plot = df_filtrado.melt(
    id_vars=["Rotacao", "Alvo"],
    value_vars=motores,
    var_name="Motor",
    value_name="Grau"
)

fig = px.line(
    df_plot,
    x="Rotacao",
    y="Grau",
    color="Motor",
    markers=True,
    title="Desempenho dos Motores ao longo das Rotações"
)

# linhas de referência
for alvo in sorted(df["Alvo"].unique()):
    fig.add_hline(y=alvo, line_dash="dot", annotation_text=f"{alvo}°")

st.plotly_chart(fig, use_container_width=True)

# =========================================
# MÉTRICAS
# =========================================
st.markdown("### 📊 Estatísticas dos Motores")

metricas = []
for motor in motores:
    erro_medio = (df_filtrado[motor] - df_filtrado["Alvo"]).abs().mean()
    desvio = df_filtrado[motor].std()
    metricas.append([motor, round(erro_medio,2), round(desvio,2)])

metrics_df = pd.DataFrame(metricas, columns=["Motor","Erro Médio (°)","Desvio Padrão"])

col1, col2 = st.columns(2)

with col1:
    st.dataframe(metrics_df.sort_values("Erro Médio (°)"), hide_index=True, use_container_width=True)

with col2:
    fig2 = px.bar(
        metrics_df,
        x="Motor",
        y="Erro Médio (°)",
        title="Erro Médio por Motor",
        color="Erro Médio (°)",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================================
# ASSISTENTE
# =========================================
st.markdown("### 🤖 Assistente de Diagnóstico")

melhor = metrics_df.sort_values("Erro Médio (°)").iloc[0]
melhor2 = metrics_df.sort_values("Erro Médio (°)").iloc[1]
pior = metrics_df.sort_values("Erro Médio (°)").iloc[-1]
mais_instavel = metrics_df.sort_values("Desvio Padrão").iloc[-1]

st.markdown(f"- ✅ Melhor desempenho: **{melhor['Motor']}** (Erro médio {melhor['Erro Médio (°)']}°)")
st.markdown(f"- ✅ Segundo melhor desempenho: **{melhor2['Motor']}** (Erro médio {melhor2['Erro Médio (°)']}°)")
st.markdown(f"- ⚠️ Pior desempenho: **{pior['Motor']}** (Erro médio {pior['Erro Médio (°)']}°)")

if pior["Erro Médio (°)"] > 5:
    st.markdown("- 🔧 Sugestão: revisar calibração e folga mecânica do pior motor.")

