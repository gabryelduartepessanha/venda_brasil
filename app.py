
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Dashboard Executivo de Vendas no Brasil",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
CAMINHO_DADOS = BASE_DIR / "dados" / "vendas_brasil.csv"
CAMINHO_BANCO = BASE_DIR / "database" / "vendas_brasil.sqlite"

sns.set_theme(style="whitegrid")


@st.cache_data
def carregar_dados_csv():
    df = pd.read_csv(CAMINHO_DADOS)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)

    # Variáveis derivadas
    df["margem_lucro"] = df["lucro"] / df["receita"]
    df["ticket_medio"] = df["receita"] / df["quantidade"]
    return df


def criar_banco_sqlite(df):
    CAMINHO_BANCO.parent.mkdir(exist_ok=True)
    engine = create_engine(f"sqlite:///{CAMINHO_BANCO}")
    df.to_sql("vendas", engine, if_exists="replace", index=False)
    return engine


df = carregar_dados_csv()
engine = criar_banco_sqlite(df)

st.title("Dashboard Executivo de Vendas no Brasil")
st.write("""
Este dashboard apresenta uma análise de vendas no Brasil, com foco em receita, lucro, margem,
ticket médio e desempenho por canal, UF, categoria e segmento.

A proposta é demonstrar um projeto completo de análise de dados, integrando Pandas, visualização
de dados, SQLAlchemy, SQLite e Streamlit.
""")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filtros")

ufs = sorted(df["uf"].dropna().unique())
canais = sorted(df["canal"].dropna().unique())
categorias = sorted(df["categoria"].dropna().unique())
segmentos = sorted(df["segmento"].dropna().unique())

uf_sel = st.sidebar.multiselect("UF", options=ufs, default=ufs)
canal_sel = st.sidebar.multiselect("Canal", options=canais, default=canais)
categoria_sel = st.sidebar.multiselect("Categoria", options=categorias, default=categorias)
segmento_sel = st.sidebar.multiselect("Segmento", options=segmentos, default=segmentos)

data_min = df["data"].min().date()
data_max = df["data"].max().date()

intervalo_datas = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if isinstance(intervalo_datas, tuple) and len(intervalo_datas) == 2:
    inicio, fim = intervalo_datas
else:
    inicio, fim = data_min, data_max

df_filtrado = df[
    (df["uf"].isin(uf_sel)) &
    (df["canal"].isin(canal_sel)) &
    (df["categoria"].isin(categoria_sel)) &
    (df["segmento"].isin(segmento_sel)) &
    (df["data"].dt.date >= inicio) &
    (df["data"].dt.date <= fim)
]

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ---------------- KPIs ----------------
st.subheader("Indicadores-chave de desempenho")

receita_total = df_filtrado["receita"].sum()
lucro_total = df_filtrado["lucro"].sum()
margem_media = lucro_total / receita_total if receita_total > 0 else 0
ticket_medio = df_filtrado["receita"].sum() / df_filtrado["quantidade"].sum()
qtd_total = df_filtrado["quantidade"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Lucro Total", f"R$ {lucro_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("Margem de Lucro", f"{margem_media:.1%}")
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col5.metric("Itens Vendidos", f"{qtd_total:,.0f}".replace(",", "."))

st.divider()

# ---------------- TABS ----------------
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Visão Geral",
    "Canais e Categorias",
    "Análise Geográfica",
    "Consulta SQL",
    "Dados"
])

with aba1:
    st.subheader("Evolução mensal da receita e do lucro")

    serie_mensal = (
        df_filtrado.groupby("ano_mes")[["receita", "lucro"]]
        .sum()
        .reset_index()
        .sort_values("ano_mes")
    )

    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    ax.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000_000:.1f} mi')
)

    sns.lineplot(data=serie_mensal, x="ano_mes", y="receita", marker="o", label="Receita", ax=ax)
    sns.lineplot(data=serie_mensal, x="ano_mes", y="lucro", marker="o", label="Lucro", ax=ax)
    ax.set_title("Evolução Mensal da Receita e do Lucro")
    ax.set_xlabel("Ano-Mês")
    ax.set_ylabel("Valor (R$)")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    st.info("""
    Este gráfico ajuda a identificar crescimento, queda ou sazonalidade no desempenho comercial.
    O gestor deve observar meses de queda e investigar possíveis causas, como redução de vendas,
    aumento de custos ou mudança de canal.
    """)

with aba2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Receita por canal")
        receita_canal = (
            df_filtrado.groupby("canal")["receita"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000_000:.1f} mi')
)
        
        sns.barplot(data=receita_canal, x="canal", y="receita", ax=ax)
        ax.set_title("Receita por Canal")
        ax.set_xlabel("Canal")
        ax.set_ylabel("Receita")
        ax.tick_params(axis="x", rotation=30)
        st.pyplot(fig)

    with col_b:
        st.subheader("Margem de lucro por canal")
        margem_canal = (
            df_filtrado.groupby("canal")
            .agg(receita=("receita", "sum"), lucro=("lucro", "sum"))
            .reset_index()
        )
        margem_canal["margem_lucro"] = margem_canal["lucro"] / margem_canal["receita"]

        fig, ax = plt.subplots(figsize=(8, 5))


        sns.barplot(data=margem_canal, x="canal", y="margem_lucro", ax=ax)
        ax.set_title("Margem de Lucro por Canal")
        ax.set_xlabel("Canal")
        ax.set_ylabel("Margem")
        ax.yaxis.set_major_formatter(
            mtick.PercentFormatter(xmax=1.0)
        )
        ax.tick_params(axis="x", rotation=30)
        st.pyplot(fig)

    st.subheader("Receita por categoria")
    receita_categoria = (
        df_filtrado.groupby("categoria")["receita"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000_000:.1f} mi')
)
    sns.barplot(data=receita_categoria, x="categoria", y="receita", ax=ax)
    ax.set_title("Receita por Categoria")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Receita")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

with aba3:
    st.subheader("Receita por UF")

    receita_uf = (
        df_filtrado.groupby("uf")["receita"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000_000:.1f} mi')
)
    sns.barplot(data=receita_uf, x="uf", y="receita", ax=ax)
    ax.set_title("Receita por UF")
    ax.set_xlabel("UF")
    ax.set_ylabel("Receita")
    st.pyplot(fig)

    uf_top = receita_uf.iloc[0]["uf"]
    receita_top = receita_uf.iloc[0]["receita"]
    st.success(
        f"A UF com maior receita no recorte filtrado é {uf_top}, com receita de "
        f"R$ {receita_top:,.2f}.".replace(",", "X").replace(".", ",").replace("X", ".")
    )

with aba4:
    st.subheader("Consulta SQL com SQLAlchemy")

    st.write("""
    Nesta seção, os dados filtrados foram gravados em um banco SQLite.
    A consulta abaixo demonstra como usar SQL para gerar indicadores a partir da tabela `vendas`.
    """)

    consulta = """
    SELECT canal,
           SUM(receita) AS receita_total,
           SUM(lucro) AS lucro_total,
           SUM(lucro) / SUM(receita) AS margem_lucro
    FROM vendas
    GROUP BY canal
    ORDER BY receita_total DESC
    """

    resultado_sql = pd.read_sql(consulta, engine)
    st.dataframe(resultado_sql, use_container_width=True)

    st.code(consulta, language="sql")

with aba5:
    st.subheader("Base filtrada")
    st.dataframe(df_filtrado, use_container_width=True)

st.divider()

st.subheader("Conclusão executiva")
st.write("""
A análise permite identificar quais canais, categorias e unidades federativas concentram maior receita
e melhor margem de lucro. O dashboard transforma a base de vendas em uma ferramenta de apoio à decisão,
permitindo que gestores explorem filtros e encontrem rapidamente oportunidades de crescimento,
problemas de rentabilidade e diferenças regionais de desempenho.
""")
