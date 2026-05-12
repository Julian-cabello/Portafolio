import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración
st.set_page_config(
    page_title="Dashboard Northwind",
    page_icon="📊",
    layout="wide"
)

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('proyecto-01-ventas/ventas_northwind.csv')
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    return df

df = cargar_datos()

# Título
st.title("📊 Dashboard de Ventas — Northwind Traders")
st.markdown("Análisis interactivo de ventas por categoría, país y período")

# Sidebar filtros
st.sidebar.header("🔍 Filtros")
paises = st.sidebar.multiselect(
    "País",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)
categorias = st.sidebar.multiselect(
    "Categoría",
    options=df['CategoryName'].unique(),
    default=df['CategoryName'].unique()
)

# Filtrar datos
df_filtrado = df[
    (df['Country'].isin(paises)) &
    (df['CategoryName'].isin(categorias))
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Ventas", f"${df_filtrado['TotalVenta'].sum():,.0f}")
col2.metric("📦 Total Pedidos", f"{df_filtrado['OrderID'].nunique():,}")
col3.metric("🌍 Países", f"{df_filtrado['Country'].nunique()}")

st.divider()

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ventas por Categoría")
    fig1 = px.bar(
        df_filtrado.groupby('CategoryName')['TotalVenta'].sum().reset_index(),
        x='CategoryName', y='TotalVenta',
        color='TotalVenta', color_continuous_scale='blues'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Ventas por País")
    fig2 = px.bar(
        df_filtrado.groupby('Country')['TotalVenta'].sum().reset_index().nlargest(10, 'TotalVenta'),
        x='TotalVenta', y='Country',
        orientation='h', color='TotalVenta',
        color_continuous_scale='blues'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Ventas por tiempo
st.subheader("Tendencia de Ventas")
df_tiempo = df_filtrado.groupby('OrderDate')['TotalVenta'].sum().reset_index()
fig3 = px.line(df_tiempo, x='OrderDate', y='TotalVenta')
st.plotly_chart(fig3, use_container_width=True)