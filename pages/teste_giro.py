import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Análise de Giro | The Crew",
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
    <span style="opacity:0.8; letter-spacing:1px">DESEMPENHO NOS GIROS DO ROBÔ</span>
    <h1 style="margin:0;">Análise de Giro</h1>
    <p style="margin-top:6px; opacity:0.9">
        Comparação entre o giro com velocidade fixa e o giro proporcional utilizando feedback do giroscópio.
    </p>
</div>
""", unsafe_allow_html=True)


# ===================== LOAD DATA =====================
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRuYovKK1C-FEzJDE5CzN5cubXHqZuXzGzvD69XQa7Lj15PKZfmmzyRC8zpyjhq7hst0yEYHJdWYYM/pub?gid=2030734909&single=true&output=csv"

@st.cache_data
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()

df["Erro Giro Velocidade Fixa (°)"] = abs(df["Alvo"] - df["Giro com Giroscópio"])
df["Erro Giro Proporcional (°)"] = abs(df["Alvo"] - df["Giro Proporcional com Giroscópio"])


# ===================== SIDEBAR =====================
st.sidebar.header("🔎 Filtros")
angulo = st.sidebar.multiselect(
    "Filtrar por ângulo alvo",
    sorted(df["Alvo"].unique())
)

if angulo:
    df = df[df["Alvo"].isin(angulo)]


# ===================== KPIs =====================
col1, col2, col3, col4 = st.columns(4)

col1.metric("⏱ Tempo médio (Velocidade Fixa)", f"{df['Tempo'].mean():.2f} s")
col2.metric("⏱ Tempo médio (Proporcional)", f"{df['Tempo.1'].mean():.2f} s")
col3.metric("🎯 Erro médio (Velocidade Fixa)", f"{df['Erro Giro Velocidade Fixa (°)'].mean():.2f}°")
col4.metric("🎯 Erro médio (Proporcional)", f"{df['Erro Giro Proporcional (°)'].mean():.2f}°")

st.success(
    "Os dados indicam que o **giro proporcional com giroscópio** apresenta "
    "**menor tempo de execução** e **maior precisão** nos giros avaliados."
)


# ===================== TABELA =====================
with st.container():
    st.markdown("### 📋 Dados dos Testes")

    st.dataframe(
        df[[
            "ID Teste",
            "Alvo",
            "Giro com Giroscópio",
            "Giro Proporcional com Giroscópio",
            "Tempo",
            "Tempo.1",
            "Erro Giro Velocidade Fixa (°)",
            "Erro Giro Proporcional (°)"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ===================== GRÁFICOS =====================
st.markdown("### 📈 Análises Visuais")

colA, colB = st.columns(2)

# ---- Tempo ----
with colA:
    st.markdown("#### ⏱ Tempo médio")
    fig1, ax1 = plt.subplots(figsize=(5, 2.5), dpi=120)
    ax1.bar(["Velocidade Fixa", "Proporcional"], [df["Tempo"].mean(), df["Tempo.1"].mean()])
    ax1.set_ylabel("Tempo (s)")
    st.pyplot(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---- Erro ----
with colB:
    st.markdown("#### 🎯 Erro angular médio")
    fig2, ax2 = plt.subplots(figsize=(5, 2.5), dpi=120)
    ax2.bar(
        ["Velocidade Fixa", "Proporcional"],
        [df["Erro Giro Velocidade Fixa (°)"].mean(), df["Erro Giro Proporcional (°)"].mean()]
    )
    ax2.set_ylabel("Erro (graus)")
    st.pyplot(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---- Dispersão ----
st.markdown("#### 📌 Dispersão do erro por teste")
fig3, ax3 = plt.subplots(figsize=(7, 3), dpi=120)
ax3.scatter(df["ID Teste"], df["Erro Giro Velocidade Fixa (°)"], label="Velocidade Fixa", alpha=0.7)
ax3.scatter(df["ID Teste"], df["Erro Giro Proporcional (°)"], label="Proporcional", alpha=0.7)
ax3.set_xlabel("ID do Teste")
ax3.set_ylabel("Erro (graus)")
ax3.legend()
st.pyplot(fig3, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
