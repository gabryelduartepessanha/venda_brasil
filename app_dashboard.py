# -*- coding: utf-8 -*-
"""Dashboard Analitico - Vendas do Varejo Brasileiro"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================
st.set_page_config(
    page_title="Dashboard Varejo BR",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas_brasil_clean.csv")
    df["data"] = pd.to_datetime(df["data"])
    return df

df = carregar_dados()

# ============================================================
# SIDEBAR - FILTROS
# ============================================================
st.sidebar.header("Filtros")

# Filtro de Canal
canais = df["canal"].unique().tolist()
canal_selecionado = st.sidebar.multiselect("Canal de Venda", canais, default=canais)

# Filtro de Categoria
categorias = df["categoria"].unique().tolist()
categoria_selecionada = st.sidebar.multiselect("Categoria", categorias, default=categorias)

# Filtro de UF
ufs = df["uf"].unique().tolist()
uf_selecionada = st.sidebar.multiselect("Estado (UF)", ufs, default=ufs)

# Filtro de Periodo
data_min = df["data"].min().date()
data_max = df["data"].max().date()
periodo = st.sidebar.date_input("Periodo", value=(data_min, data_max),
                                 min_value=data_min, max_value=data_max)

# Aplicar filtros
df_filtro = df[
    (df["canal"].isin(canal_selecionado)) &
    (df["categoria"].isin(categoria_selecionada)) &
    (df["uf"].isin(uf_selecionada))
]

if len(periodo) == 2:
    df_filtro = df_filtro[
        (df_filtro["data"].dt.date >= periodo[0]) &
        (df_filtro["data"].dt.date <= periodo[1])
    ]

# ============================================================
# TITULO E KPIs
# ============================================================
st.title("Dashboard de Vendas - Varejo Brasileiro")
st.markdown("Analise completa do desempenho de vendas por canal, categoria e regiao.")

# KPIs no topo
col1, col2, col3, col4 = st.columns(4)

receita_total = df_filtro["receita"].sum()
lucro_total = df_filtro["lucro"].sum()
margem = (lucro_total / receita_total * 100) if receita_total > 0 else 0
ticket_medio = df_filtro["receita"].mean()

with col1:
    st.metric("Receita Total", f"R$ {receita_total:,.2f}")
with col2:
    st.metric("Lucro Total", f"R$ {lucro_total:,.2f}")
with col3:
    st.metric("Margem de Lucro", f"{margem:.1f}%")
with col4:
    st.metric("Ticket Medio", f"R$ {ticket_medio:,.2f}")

st.divider()

# ============================================================
# GRAFICOS
# ============================================================

# Linha 1: Evolucao temporal + Composicao por canal
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Evolucao Mensal da Receita")
    receita_mes = df_filtro.groupby(df_filtro["data"].dt.to_period("M"))["receita"].sum().reset_index()
    receita_mes["data_str"] = receita_mes["data"].astype(str)
    fig = px.line(receita_mes, x="data_str", y="receita", markers=True,
                  labels={"data_str": "Mes", "receita": "Receita (R$)"})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Composicao por Canal")
    canal_data = df_filtro.groupby("canal")["receita"].sum().reset_index()
    fig = px.pie(canal_data, names="canal", values="receita",
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Linha 2: Ranking por UF + Scatter
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Receita por Estado")
    uf_data = df_filtro.groupby("uf")["receita"].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(uf_data, x="receita", y="uf", orientation="h",
                 labels={"uf": "Estado", "receita": "Receita (R$)"},
                 color="receita", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

with col_d:
    st.subheader("Receita vs Lucro")
    fig = px.scatter(df_filtro, x="receita", y="lucro", color="canal",
                     hover_data=["uf", "categoria"], opacity=0.6)
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TABELA DE DADOS
# ============================================================
st.divider()
st.subheader("Dados Detalhados")
st.dataframe(df_filtro, use_container_width=True)

# Download
csv = df_filtro.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "vendas_filtradas.csv", "text/csv")

# ============================================================
# STORYTELLING
# ============================================================
st.divider()
st.subheader("Insights Analiticos")

st.markdown(f"""
### Principais Descobertas

- **Receita Total:** R$ {receita_total:,.2f} no periodo filtrado
- **Margem de Lucro:** {margem:.1f}% - {'Saudavel' if margem > 10 else 'Atencao necessaria'}
- **Ticket Medio:** R$ {ticket_medio:,.2f} por transacao
- **Canal Lider:** {df_filtro.groupby("canal")["receita"].sum().idxmax()} com maior volume de vendas
- **Estado Lider:** {df_filtro.groupby("uf")["receita"].sum().idxmax()} em receita total

### Recomendacoes

1. Investir no canal com maior margem de lucro
2. Explorar oportunidades nos estados com menor participacao
3. Monitorar categorias com margem negativa
4. Avaliar sazonalidade para campanhas promocionais
""")
