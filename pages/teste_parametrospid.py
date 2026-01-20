import streamlit as st
import pandas as pd
import requests

# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(
    page_title="Parâmetros PID | The Crew",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# CSS MODERNO
# -------------------------------
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

.change-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 10px;
}

.change-card:hover {
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

# -------------------------------
# CABEÇALHO
# -------------------------------
st.markdown("""
<div class="header-box">
    <span style="opacity:0.8; letter-spacing:1px">PARÂMETROS DO CONTROLE PID</span>
    <h1 style="margin:0;">Testes de Parâmetros PID</h1>
    <p style="margin-top:6px; opacity:0.9">
        Monitoramento dos parâmetros e influencia nos movimentos de giro do robô.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# LINK DA PLANILHA CSV
# -------------------------------
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=0&single=true&output=csv"

# -------------------------------
# LER PLANILHA
# -------------------------------
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(url)

# -------------------------------
# SIDEBAR - FILTROS
# -------------------------------
st.sidebar.header("🔎 Filtros")
search = st.sidebar.text_input("Buscar em qualquer campo")

if search:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

# Filtro por resultado se existir
if "Resultado" in df.columns:
    resultado_sel = st.sidebar.multiselect("Filtrar por resultado", sorted(df["Resultado"].dropna().unique()))
    if resultado_sel:
        df = df[df["Resultado"].isin(resultado_sel)]

# -------------------------------
# KPIs
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🧪 Total de Testes", len(df))
col2.metric("⚙️ Testes com Mudança", df["Mudança"].notna().sum())
if "Resultado" in df.columns:
    col3.metric("🏁 Resultados Diferentes", df["Resultado"].nunique())
else:
    col3.metric("🏁 Resultados", "--")

st.write("")

# -------------------------------
# TABELA PRINCIPAL (limpa)
# -------------------------------
st.subheader("📋 Visão Geral dos Testes")

df_exibir = df.drop(columns=["Antes", "Depois"], errors="ignore")
st.dataframe(
    df_exibir,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# LISTA DE MUDANÇAS
# -------------------------------
st.write("")
st.subheader("🛠️ Ajustes Aplicados nos Testes")

mudancas = df[df["Mudança"].notna() & (df["Mudança"].astype(str).str.strip() != "")]

if mudancas.empty:
    st.info("Nenhuma mudança registrada nos testes até agora.")
else:
    for i, row in mudancas.iterrows():
        with st.expander(f"Teste {row['ID Teste']} — {row['Mudança']}"):
            st.markdown(f"""
            <div class="change-card">
                <b>📅 Data:</b> {row.get('Data','-')}<br>
                <b🎯 Alvo:</b> {row.get('Alvo','-')}<br>
                <b>🏁 Resultado:</b> {row.get('Resultado','-')}<br><br>
                <b>📝 Descrição:</b><br>{row.get('Mudança','-')}<br><br>
                <b>Valores Antes:</b> {row.get('Antes','-')}<br>
                <b>Valores Depois:</b> {row.get('Depois','-')}
            </div>
            """, unsafe_allow_html=True)
