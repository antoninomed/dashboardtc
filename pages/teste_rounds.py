import streamlit as st
import pandas as pd
import plotly.express as px

import requests
from PIL import Image
from io import BytesIO

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Rounds | The Crew",
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
    <span style="opacity:0.8; letter-spacing:1px">ANÁLISE DE ROUNDS</span>
    <h1 style="margin:0;">Análise de Rounds</h1>
    <p style="margin-top:6px; opacity:0.9">
        Evolução da pontuação total, eficiência por missão e dicas do Crew Assistente.
    </p>
</div>
""", unsafe_allow_html=True)


# ===================== LOAD DATA =====================
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=1674634257&single=true&output=csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.date
    return df

df = load_data(url)


# ===================== SIDEBAR =====================
st.sidebar.header("🔎 Filtros")

min_date = df['Data'].min()
max_date = df['Data'].max()

data_range = st.sidebar.date_input(
    "Selecione o período:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(data_range, tuple):
    if len(data_range) == 1:
        start_date = end_date = data_range[0]
    else:
        start_date, end_date = data_range
else:
    start_date = end_date = data_range

df_filtrado = df[
    (df['Data'] >= start_date) &
    (df['Data'] <= end_date)
]


# ===================== TABELA =====================
st.markdown("### 📋 Tabela de Rounds")
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

def load_drive_image(url):
    file_id = url.split("/d/")[1].split("/")[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(download_url, headers=headers)

    if r.status_code != 200:
        return None

    return Image.open(BytesIO(r.content))


st.write("")
st.subheader("🛠️ Histórico de Evoluções")

mudancas = df_filtrado[df_filtrado["Observação"].notna() & (df_filtrado["Observação"].astype(str).str.strip() != "")]

if mudancas.empty:
    st.info("Nenhuma mudança registrada até agora.")
else:
    for i, row in mudancas.iterrows():
        titulo = f"📅 {row['Data']} — {row.get('Round','Round')} | {row['Observação'][:60]}..."

        with st.expander(titulo):
            st.markdown(f"""
            <div style="
                background:#f8fafc;
                border:1px solid #e5e7eb;
                border-radius:12px;
                padding:16px;
                margin-bottom:10px;
            ">
                <b>📝 Alteração:</b><br>{row['Observação']}<br><br>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Antes")
                st.image(load_drive_image(row['Antes']), width=280)

            with col2:
                st.markdown("### Depois")
                st.image(load_drive_image(row['Depois']), width=280)




# ===================== EVOLUÇÃO TOTAL =====================
st.markdown("### 📈 Evolução da Pontuação Total")

fig_total = px.line(
    df_filtrado,
    x='Data',
    y='Total',
    markers=True,
    title="Pontuação Total ao longo do tempo",
    range_y=[0, 545]
)
st.plotly_chart(fig_total, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ===================== EFICIÊNCIA =====================
st.markdown("### 🎯 Eficiência por Missão")
missoes = [col for col in df_filtrado.columns if col.startswith('M')]

maximos = {
    'M01': 30,'M02': 30,'M03': 40,'M04': 40,'M05': 30,'M06': 30,
    'M07': 30,'M08': 30,'M09': 30,'M10': 30,'M11': 30,'M12': 30,
    'M13': 30,'M14': 35,'M15': 30
}

for m in missoes:
    if m not in maximos:
        maximos[m] = 30

precisao = {m: df_filtrado[m].sum() / (len(df_filtrado) * maximos[m]) * 100 for m in missoes}

precisao_df = pd.DataFrame({
    'Missão': precisao.keys(),
    'Precisão (%)': precisao.values()
}).sort_values(by='Precisão (%)', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.dataframe(precisao_df, hide_index=True, use_container_width=True)

with col2:
    fig_precisao = px.bar(
        precisao_df,
        x='Missão',
        y='Precisão (%)',
        text='Precisão (%)',
        title="Precisão Média por Missão",
        color='Precisão (%)',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_precisao, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ===================== ANÁLISE POR MISSÃO =====================
st.markdown("### 🔍 Análise Detalhada por Missão")

selected_missao = st.selectbox("Escolha a missão", missoes)

fig_single = px.line(
    df_filtrado,
    x='Data',
    y=selected_missao,
    markers=True,
    title=f"Pontuação da {selected_missao} ao longo do tempo",
    range_y=[0, maximos[selected_missao]]
)
st.plotly_chart(fig_single, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ===================== ASSISTENTE =====================
melhor_missao = precisao_df.loc[precisao_df['Precisão (%)'].idxmax()]
pior_missao = precisao_df.loc[precisao_df['Precisão (%)'].idxmin()]

if len(df_filtrado) > 1:
    total_diff = df_filtrado['Total'].iloc[-1] - df_filtrado['Total'].iloc[0]
    tendencia = "subindo 📈" if total_diff > 0 else "caindo 📉" if total_diff < 0 else "estável ➖"
else:
    tendencia = "sem dados suficientes"

desvios = {m: df_filtrado[m].std() for m in missoes}
missao_irregular = max(desvios, key=desvios.get)

recomendacoes = []

if pior_missao['Precisão (%)'] < 70:
    recomendacoes.append(f"💡 Focar em treinar a missão **{pior_missao['Missão']}** ({pior_missao['Precisão (%)']:.1f}%).")

if 'total_diff' in locals():
    if total_diff < 0:
        recomendacoes.append("⚠️ A pontuação total está caindo, investigar execução e estratégia.")
    elif total_diff > 0:
        recomendacoes.append("✅ A pontuação total está melhorando, continuar abordagem atual.")

if desvios[missao_irregular] > 5:
    recomendacoes.append(f"⚡ A missão **{missao_irregular}** é a mais instável (desvio {desvios[missao_irregular]:.1f}). Trabalhar consistência.")

for m in missoes:
    if precisao[m] > 97:
        recomendacoes.append(f"🏆 A missão **{m}** está excelente! Manter rotina atual.")

st.markdown("### 🤖 Crew Assistente")
for r in recomendacoes:
    st.markdown(f"- {r}")
st.markdown("</div>", unsafe_allow_html=True)
