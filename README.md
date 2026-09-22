
# Dashboard Executivo de Vendas no Brasil

## 1. Descricao do projeto

Este projeto apresenta uma **analise executiva completa** de vendas no Brasil, cobrindo todo o pipeline de dados: desde a importacao dos dados brutos ate a publicacao de um dashboard interativo.

O projeto foi desenvolvido como avaliacao G2 da disciplina **Linguagem de Programacao — Analise e Visualizacao de Dados com Python**.

### Fluxo do Projeto

```
vendas_brasil.csv (dados brutos)
    ↓ Limpeza (pandas)
vendas_brasil_clean.csv (dados tratados)
    ↓ Persistencia (SQLAlchemy)
vendas.db (banco SQLite)
    ↓ Dashboard (Streamlit)
app_dashboard.py (aplicacao web)
    ↓ Deploy
Streamlit Cloud (online)
```

---

## 2. Problema de negocio

Uma empresa de varejo que atua em diferentes estados, canais e categorias precisa responder:

- Qual e a receita total do negocio?
- Qual e o lucro total?
- Qual e a margem de lucro?
- Qual canal gera mais receita?
- Qual canal apresenta melhor margem?
- Quais categorias tem melhor desempenho?
- Quais UFs concentram maior receita?
- Ha variacao temporal relevante nas vendas?

---

## 3. Tecnologias utilizadas

| Tecnologia | Funcao |
|------------|--------|
| Python | Linguagem principal |
| pandas | Manipulacao e analise de dados |
| matplotlib | Visualizacao estatica |
| seaborn | Visualizacao estatistica |
| plotly | Visualizacao interativa |
| SQLAlchemy | Conexao com banco de dados |
| SQLite | Persistencia de dados |
| Streamlit | Dashboard interativo |
| Git/GitHub | Versionamento |

---

## 4. Estrutura do projeto

```text
projeto-venda-brasil-g2/
|
|-- README.md                    # Este arquivo
|-- requirements.txt             # Dependencias
|-- app.py                       # App Streamlit (avaliacao G2)
|-- app_dashboard.py             # Dashboard completo (projeto integrador)
|
|-- dados/
|   |-- vendas_brasil.csv        # Dados brutos (2.500 registros)
|
|-- database/
|   |-- vendas_brasil.sqlite     # Banco SQLite
|
|-- notebooks/
|   |-- analise_venda_brasil.ipynb     # Notebook da avaliacao G2
|   |-- projeto_integrador.ipynb        # Notebook completo (12 aulas)
|
|-- imagens/
```

---

## 5. Como executar localmente

### 5.1 Clonar o repositorio

```bash
git clone https://github.com/AlexandreLouzada/projeto-venda-brasil-g2.git
cd projeto-venda-brasil-g2
```

### 5.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5.3 Executar o dashboard

```bash
# Dashboard da avaliacao G2
streamlit run app.py

# Dashboard completo (projeto integrador)
streamlit run app_dashboard.py
```

### 5.4 Executar o notebook

```bash
# Abrir no Jupyter/VSCode e executar celula por celula
jupyter notebook notebooks/projeto_integrador.ipynb
```

---

## 6. KPIs utilizados

| KPI | Descricao |
|-----|-----------|
| Receita Total | Soma da receita das vendas |
| Lucro Total | Soma do lucro das vendas |
| Margem de Lucro % | Lucro total dividido pela receita total |
| Ticket Medio | Receita media por transacao |
| Itens Vendidos | Soma da quantidade de produtos vendidos |

---

## 7. Funcionalidades do dashboard

### Dashboard G2 (`app.py`)

- Filtros por UF, canal, categoria e segmento
- KPIs dinamicos
- Graficos de evolucao temporal
- Consulta SQL demonstrativa
- Tabela interativa dos dados filtrados

### Dashboard Completo (`app_dashboard.py`)

- Filtros por UF, canal, categoria e periodo
- 4 KPIs no topo com metricas
- Graficos Plotly interativos (linhas, barras, scatter, pizza)
- Tabela de dados com download CSV
- Storytelling analitico com insights

---

## 8. Projeto Integrador — Notebook Completo

O notebook `projeto_integrador.ipynb` cobre as **12 aulas** da disciplina:

| Secao | Aula | Biblioteca | Conteudo |
|-------|------|------------|----------|
| 1. Introducao e Setup | Aula 1 | pandas | Pipeline de dados, importacao |
| 2. Exploracao Inicial | Aula 2 | pandas | shape, info, selecao, filtragem |
| 3. Limpeza e Preparacao | Aula 3 | pandas | Tipos, nulos, feature engineering |
| 4. KPIs e Indicadores | Aula 4 | pandas | Metricas de negocio, groupby |
| 5. Visualizacao Estatica | Aula 5 | matplotlib/seaborn | Barras, linhas, boxplot, heatmap |
| 6. Visualizacao Interativa | Aula 6 | plotly | Graficos dinamicos com tooltips |
| 7. SQL + Python | Aula 7 | sqlalchemy | Tabelas Fato/Dimensao, consultas |
| 8-9. Dashboard Streamlit | Aulas 8-9 | streamlit | App com sidebar, KPIs, storytelling |
| 10. Git e Portfolio | Aula 10 | git | Versionamento, README |
| 11. Deploy | Aula 11 | streamlit cloud | Publicacao na web |
| 12. Pitch Analitico | Aula 12 | markdown | Resumo executivo |

---

## 9. Principais insights esperados

O projeto permite identificar:

- Canais mais relevantes para receita
- Canais com melhor rentabilidade
- Categorias mais importantes
- Estados com maior concentracao de vendas
- Variacoes temporais de receita e lucro
- Diferencas entre volume financeiro e eficiencia operacional

---

## 10. Publicacao

| Etapa | Ferramenta | Status |
|-------|------------|--------|
| Versionamento | GitHub | Concluido |
| Dashboard G2 | Streamlit Cloud | Pendente |
| Dashboard Completo | Streamlit Cloud | Pendente |

---

## 11. Objetivo pedagogico

Este projeto demonstra aos alunos como transformar uma base de dados em um produto analitico completo.

O foco nao esta apenas em gerar graficos, mas em responder perguntas de negocio e apoiar a tomada de decisao.
