import streamlit as st
import pandas as pd
import plotly.express as px

# Leitura da planilha
df = pd.read_excel("ESCOLA DE FUNDAMENTOS MATRÍCULA - AGO2025 (respostas).xlsx")
df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes

# Título do dashboard
st.title("📊 Dashboard Interativo - Escola de Fundamentos")

# Filtros interativos
col1, col2 = st.columns(2)

with col1:
    geracoes = st.multiselect("Filtrar por Geração:", df['GERACÃO'].dropna().unique(), default=df['GERACÃO'].dropna().unique())

with col2:
    pastores = st.multiselect("Filtrar por Pastor(a):", df['PASTOR(A)'].dropna().unique(), default=df['PASTOR(A)'].dropna().unique())

# Aplicar os filtros
df_filtrado = df[df['GERACÃO'].isin(geracoes) & df['PASTOR(A)'].isin(pastores)]

# Exibir total de alunos filtrados
st.metric("👥 Total de Alunos", len(df_filtrado))

# Gráfico de barras: Alunos por Geração
contagem_geracao = df_filtrado['GERACÃO'].value_counts().reset_index()
contagem_geracao.columns = ['Geração', 'Qtd de Alunos']

fig_geracao = px.bar(contagem_geracao,
                     x='Geração', y='Qtd de Alunos',
                     title="Alunos por Geração")

# Gráfico de pizza: Distribuição por Pastor(a)
fig_pastor = px.pie(df_filtrado, names='PASTOR(A)', title="Distribuição por Pastor(a)")
st.plotly_chart(fig_pastor)

# Gráfico: Alunos por Dia da Aula
fig_dia = px.histogram(df_filtrado, x='DIA DE AULA', color='GERACÃO', barmode='group',
                       title="Alunos por Dia da Aula")
st.plotly_chart(fig_dia)

# Tabela detalhada
with st.expander("📋 Ver Tabela de Alunos Filtrados"):
    st.dataframe(df_filtrado[['NOME', 'GERACÃO', 'PASTOR(A)', 'DIA DE AULA']])
