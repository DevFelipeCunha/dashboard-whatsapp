import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Enquetes", layout="wide")

st.title("📊 Painel de Apuração - Enquetes WhatsApp")
st.markdown("Acompanhe os resultados consolidados da votação.")

# Abre o arquivo que você vai subir no GitHub
try:
    df = pd.read_csv("dados_enquete.csv")
except FileNotFoundError:
    st.error("Aguardando o envio do arquivo 'dados_enquete.csv' no GitHub...")
    st.stop()

# Filtro de Perguntas
perguntas = df["Pergunta"].unique()
pergunta_selecionada = st.selectbox("Selecione a Enquete para analisar:", perguntas)
df_filtrado = df[df["Pergunta"] == pergunta_selecionada]

# Cartões de Métricas
total_votos = df_filtrado["Votos"].sum()
opcao_vencedora = df_filtrado.loc[df_filtrado["Votos"].idxmax()]["Opção"]

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total de Votos Computados", value=total_votos)
with col2:
    st.metric(label="Opção Líder / Vencedora", value=opcao_vencedora)

st.markdown("---")

# Seção Gráfica
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.subheader("Visualização em Barras")
    fig_barra = px.bar(df_filtrado, x="Opção", y="Votos", text="Votos", color="Opção", color_discrete_sequence=px.colors.qualitative.Dark2)
    fig_barra.update_traces(textposition="outside")
    st.plotly_chart(fig_barra, use_container_width=True)

with col_g2:
    st.subheader("Visualização em Pizza")
    fig_pizza = px.pie(df_filtrado, values="Votos", names="Opção", hole=0.4)
    st.plotly_chart(fig_pizza, use_container_width=True)
