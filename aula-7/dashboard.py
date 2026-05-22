import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página para ocupar a largura total
st.set_page_config(page_title="Kensei Cyber Dashboard", page_icon="🛡️", layout="wide")

# Caminho do arquivo CSV na pasta local
CSV_PATH = os.path.join(os.path.dirname(__file__), "cyber_attacks.csv")

@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        # Garantir que a coluna de data seja tratada corretamente se existir
        for col in ['Timestamp', 'Date']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df
    return None

df = load_data()

if df is not None:
    st.title("🛡️ Cyber Security Intelligence Dashboard")
    st.markdown("Análise em tempo real de tentativas de intrusão e vetores de ataque.")

    # --- SIDEBAR COM FILTROS ---
    st.sidebar.header("⚙️ Filtros Globais")
    
    # Filtro de Tipo de Ataque
    tipos_ataque = ["Todos"] + sorted(list(df['Attack Type'].unique()))
    filtro_ataque = st.sidebar.selectbox("Vetor de Ataque", tipos_ataque)
    
    # Filtro de País (se a coluna existir)
    if 'Country' in df.columns:
        paises = ["Todos"] + sorted(list(df['Country'].unique()))
        filtro_pais = st.sidebar.multiselect("Países de Origem", paises, default="Todos")

    # Lógica de Filtragem
    df_filtered = df.copy()
    if filtro_ataque != "Todos":
        df_filtered = df_filtered[df_filtered['Attack Type'] == filtro_ataque]
    if 'Country' in df.columns and "Todos" not in filtro_pais:
        df_filtered = df_filtered[df_filtered['Country'].isin(filtro_pais)]

    # --- KPIs NO TOPO ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("Total de Alertas", len(df_filtered))
    with kpi2:
        top_attack = df_filtered['Attack Type'].mode()[0] if not df_filtered.empty else "N/A"
        st.metric("Vetor Mais Comum", top_attack)
    with kpi3:
        paises_count = df_filtered['Country'].nunique() if 'Country' in df_filtered.columns else 0
        st.metric("Países Envolvidos", paises_count)
    with kpi4:
        avg_severity = "Alta" # Exemplo estático ou cálculo baseado em severidade
        st.metric("Risco Médio", avg_severity)

    st.divider()

    # --- GRÁFICOS ---
    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.subheader("📊 Volume por Tipo de Ataque")
        st.bar_chart(df_filtered['Attack Type'].value_counts())

    with col_graph2:
        st.subheader("🌍 Top 10 Origens de Ataque")
        if 'Country' in df_filtered.columns:
            st.line_chart(df_filtered['Country'].value_counts().head(10))

    # --- MAPA MUNDI ---
    st.divider()
    st.subheader("🗺️ Distribuição Global de Incidentes")
    if 'Country' in df_filtered.columns:
        # Preparando os dados para o mapa
        country_stats = df_filtered['Country'].value_counts().reset_index()
        country_stats.columns = ['País', 'Alertas']
        
        fig_map = px.choropleth(
            country_stats,
            locations="País",
            locationmode="country names",
            color="Alertas",
            color_continuous_scale="Reds",
            template="plotly_dark"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # --- TABELA DE DADOS ---
    st.subheader("🔍 Detalhes dos Eventos")
    st.dataframe(df_filtered, use_container_width=True)
else:
    st.error(f"Erro: O arquivo '{CSV_PATH}' não foi encontrado na pasta aula-7.")
    st.info("Dica: Copie o arquivo CSV de ataques para a pasta aula-7 para visualizar o dashboard.")