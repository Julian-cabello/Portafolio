import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Northwind Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── ESTILOS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0a0f1e;
}

[data-testid="stSidebar"] {
    background: #0d1428;
    border-right: 1px solid #1e2d4a;
}

[data-testid="stSidebar"] .stMarkdown h2 {
    color: #4fc3f7;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid #1e2d4a;
    padding-bottom: 8px;
    margin-bottom: 16px;
}

.stMultiSelect [data-baseweb="tag"] {
    background: #1565c0 !important;
    border-radius: 4px !important;
}

.kpi-card {
    background: linear-gradient(135deg, #0d1428 0%, #111d35 100%);
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, #4fc3f7);
}
.kpi-label {
    color: #5c7a9e;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    color: #e8f4fd;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    color: #4fc3f7;
    font-size: 0.78rem;
    font-weight: 500;
}

.section-title {
    color: #e8f4fd;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e2d4a, transparent);
}

.chart-container {
    background: #0d1428;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 20px;
}

.main-header {
    padding: 8px 0 24px 0;
    border-bottom: 1px solid #1e2d4a;
    margin-bottom: 28px;
}
.main-title {
    color: #e8f4fd;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
}
.main-subtitle {
    color: #5c7a9e;
    font-size: 0.85rem;
    margin-top: 4px;
}
.badge {
    display: inline-block;
    background: #0d2137;
    border: 1px solid #1e4a6e;
    color: #4fc3f7;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: 6px;
}

hr { border-color: #1e2d4a !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── COLORES ──────────────────────────────────────────────────────────────────
COLOR_PRIMARY   = "#4fc3f7"
COLOR_SECONDARY = "#00e5ff"
COLOR_ACCENT    = "#1565c0"
COLOR_BG        = "#0d1428"
COLOR_SURFACE   = "#111d35"
COLOR_BORDER    = "#1e2d4a"
COLOR_TEXT      = "#e8f4fd"
COLOR_MUTED     = "#5c7a9e"

PALETTE = ["#4fc3f7", "#00e5ff", "#1565c0", "#0288d1", "#26c6da",
           "#80deea", "#b3e5fc", "#29b6f6", "#039be5", "#0277bd"]

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Inter, sans-serif", color=COLOR_MUTED, size=11),
        xaxis=dict(
            gridcolor=COLOR_BORDER, linecolor=COLOR_BORDER,
            tickfont=dict(color=COLOR_MUTED)
        ),
        yaxis=dict(
            gridcolor=COLOR_BORDER, linecolor=COLOR_BORDER,
            tickfont=dict(color=COLOR_MUTED)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLOR_MUTED)
        ),
        margin=dict(l=16, r=16, t=36, b=16),
    )
)

# ─── DATOS ────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_csv('proyecto-01-ventas/ventas_northwind.csv')
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], format='mixed', dayfirst=False)
    df['Año'] = df['OrderDate'].dt.year.astype(int)
    df['Mes'] = df['OrderDate'].dt.to_period('M').astype(str)
    return df

df = cargar_datos()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Filtros")

    años = sorted(df['Año'].unique())
    año_sel = st.multiselect("Año", años, default=años)

    paises = sorted(df['Country'].dropna().unique())
    pais_sel = st.multiselect("País", paises, default=paises)

    cats = sorted(df['CategoryName'].unique())
    cat_sel = st.multiselect("Categoría", cats, default=cats)

    st.markdown("---")
    st.markdown(f"""
    <div style='color:{COLOR_MUTED}; font-size:0.72rem; line-height:1.8'>
        <div style='color:{COLOR_PRIMARY}; font-weight:600; margin-bottom:6px'>📦 Dataset</div>
        Northwind Traders (Microsoft)<br>
        SQLite · jpwhite3<br>
        <span style='color:{COLOR_PRIMARY}'>{len(df):,}</span> registros totales
    </div>
    """, unsafe_allow_html=True)

# ─── FILTRAR ──────────────────────────────────────────────────────────────────
df_f = df[
    df['Año'].isin(año_sel) &
    df['Country'].isin(pais_sel) &
    df['CategoryName'].isin(cat_sel)
]

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
    <div style='margin-bottom:10px'>
        <span class='badge'>SQL</span>
        <span class='badge'>Python</span>
        <span class='badge'>Streamlit</span>
        <span class='badge'>Plotly</span>
    </div>
    <div class='main-title'>📊 Northwind Sales Analytics</div>
    <div class='main-subtitle'>Dashboard de análisis de ventas · Julián Cabello · Data Analyst</div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ─────────────────────────────────────────────────────────────────────
total_ventas   = df_f['TotalVenta'].sum()
total_pedidos  = df_f['OrderID'].nunique()
total_paises   = df_f['Country'].nunique()
ticket_prom    = total_ventas / total_pedidos if total_pedidos > 0 else 0
top_cat        = df_f.groupby('CategoryName')['TotalVenta'].sum().idxmax() if not df_f.empty else "—"

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='kpi-card' style='--accent:#4fc3f7'>
        <div class='kpi-label'>💰 Total Ventas</div>
        <div class='kpi-value'>${total_ventas/1e6:.1f}M</div>
        <div class='kpi-sub'>USD acumulado</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card' style='--accent:#00e5ff'>
        <div class='kpi-label'>📦 Pedidos</div>
        <div class='kpi-value'>{total_pedidos:,}</div>
        <div class='kpi-sub'>órdenes únicas</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card' style='--accent:#26c6da'>
        <div class='kpi-label'>🌍 Países</div>
        <div class='kpi-value'>{total_paises}</div>
        <div class='kpi-sub'>mercados activos</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card' style='--accent:#80deea'>
        <div class='kpi-label'>🏆 Top Categoría</div>
        <div class='kpi-value' style='font-size:1.2rem;margin-top:6px'>{top_cat}</div>
        <div class='kpi-sub'>mayor volumen</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ─── FILA 1: Categorías + Países ──────────────────────────────────────────────
c1, c2 = st.columns([1.1, 0.9])

with c1:
    st.markdown("<div class='section-title'>Ventas por Categoría</div>", unsafe_allow_html=True)
    df_cat = df_f.groupby('CategoryName')['TotalVenta'].sum().reset_index()
    df_cat = df_cat.sort_values('TotalVenta', ascending=True)
    fig1 = go.Figure(go.Bar(
        x=df_cat['TotalVenta'],
        y=df_cat['CategoryName'],
        orientation='h',
        marker=dict(
            color=df_cat['TotalVenta'],
            colorscale=[[0, '#0d2137'], [0.5, '#1565c0'], [1, '#4fc3f7']],
            line=dict(width=0)
        ),
        text=[f"${v/1e6:.1f}M" for v in df_cat['TotalVenta']],
        textposition='outside',
        textfont=dict(color=COLOR_TEXT, size=10)
    ))
    fig1.update_layout(**PLOTLY_TEMPLATE['layout'], height=320)
    fig1.update_xaxes(showgrid=False, showticklabels=False)
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with c2:
    st.markdown("<div class='section-title'>Top 10 Países</div>", unsafe_allow_html=True)
    df_pais = df_f.groupby('Country')['TotalVenta'].sum().reset_index()
    df_pais = df_pais.nlargest(10, 'TotalVenta').sort_values('TotalVenta')
    fig2 = go.Figure(go.Bar(
        x=df_pais['TotalVenta'],
        y=df_pais['Country'],
        orientation='h',
        marker=dict(
            color=PALETTE[:len(df_pais)],
            line=dict(width=0)
        ),
        text=[f"${v/1e6:.1f}M" for v in df_pais['TotalVenta']],
        textposition='outside',
        textfont=dict(color=COLOR_TEXT, size=10)
    ))
    fig2.update_layout(**PLOTLY_TEMPLATE['layout'], height=320)
    fig2.update_xaxes(showgrid=False, showticklabels=False)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

# ─── MAPA: Distribución Geográfica ────────────────────────────────────────────
st.markdown("<div class='section-title'>Distribución Geográfica de Clientes</div>", unsafe_allow_html=True)

df_mapa = df_f.groupby('Country').agg(
    TotalVenta=('TotalVenta', 'sum'),
    Pedidos=('OrderID', 'nunique')
).reset_index()

fig_mapa = px.choropleth(
    df_mapa,
    locations='Country',
    locationmode='country names',
    color='TotalVenta',
    hover_name='Country',
    hover_data={
        'TotalVenta': ':$.0f',
        'Pedidos': ':,',
        'Country': False
    },
    color_continuous_scale=[
        [0.0, '#0d2137'],
        [0.3, '#1565c0'],
        [0.7, '#0288d1'],
        [1.0, '#4fc3f7']
    ],
    labels={'TotalVenta': 'Ventas (USD)'}
)

fig_mapa.update_layout(
    **PLOTLY_TEMPLATE['layout'],
    height=420,
    geo=dict(
        bgcolor=COLOR_BG,
        landcolor='#111d35',
        oceancolor=COLOR_BG,
        showocean=True,
        lakecolor=COLOR_BG,
        showlakes=True,
        coastlinecolor=COLOR_BORDER,
        countrycolor=COLOR_BORDER,
        showcoastlines=True,
        showcountries=True,
        showframe=False,
        projection_type='natural earth'
    ),
    coloraxis_colorbar=dict(
        title=dict(text='Ventas USD', font=dict(color=COLOR_MUTED, size=10)),
        tickfont=dict(color=COLOR_MUTED, size=9),
        bgcolor=COLOR_BG,
        bordercolor=COLOR_BORDER,
        thickness=12,
        len=0.6
    )
)

st.plotly_chart(fig_mapa, use_container_width=True, config={'displayModeBar': False})

# ─── FILA 2: Tendencia ────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Tendencia de Ventas Mensual</div>", unsafe_allow_html=True)

df_tiempo = df_f.groupby('Mes')['TotalVenta'].sum().reset_index()
df_tiempo = df_tiempo.sort_values('Mes')

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=df_tiempo['Mes'],
    y=df_tiempo['TotalVenta'],
    mode='lines',
    line=dict(color=COLOR_PRIMARY, width=1.5),
    fill='tozeroy',
    fillcolor='rgba(79,195,247,0.06)',
    name='Ventas mensuales'
))
fig3.add_trace(go.Scatter(
    x=df_tiempo['Mes'],
    y=df_tiempo['TotalVenta'].rolling(6, min_periods=1).mean(),
    mode='lines',
    line=dict(color=COLOR_SECONDARY, width=2.5, dash='dot'),
    name='Media móvil 6M'
))
fig3.update_layout(**PLOTLY_TEMPLATE['layout'], height=260)
fig3.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

# ─── FILA 3: Producto + Distribución ──────────────────────────────────────────
c3, c4 = st.columns([1.2, 0.8])

with c3:
    st.markdown("<div class='section-title'>Top 10 Productos</div>", unsafe_allow_html=True)
    df_prod = df_f.groupby('ProductName')['TotalVenta'].sum().reset_index()
    df_prod = df_prod.nlargest(10, 'TotalVenta').sort_values('TotalVenta')
    fig4 = go.Figure(go.Bar(
        x=df_prod['TotalVenta'],
        y=df_prod['ProductName'],
        orientation='h',
        marker=dict(color=COLOR_ACCENT, line=dict(width=0)),
        text=[f"${v/1e3:.0f}K" for v in df_prod['TotalVenta']],
        textposition='outside',
        textfont=dict(color=COLOR_TEXT, size=10)
    ))
    fig4.update_layout(**PLOTLY_TEMPLATE['layout'], height=320)
    fig4.update_xaxes(showgrid=False, showticklabels=False)
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

with c4:
    st.markdown("<div class='section-title'>Mix de Categorías</div>", unsafe_allow_html=True)

    todas_cats = sorted(df_f['CategoryName'].unique())
    cats_donut = st.multiselect(
        "Categorías visibles",
        todas_cats,
        default=todas_cats,
        key="donut_cats",
        label_visibility="collapsed"
    )

    df_pie = df_f[df_f['CategoryName'].isin(cats_donut)]
    df_pie_agg = df_pie.groupby('CategoryName')['TotalVenta'].sum().reset_index()
    total_donut = df_pie_agg['TotalVenta'].sum()  # ← recalcula según selección

    fig5 = go.Figure(go.Pie(
        labels=df_pie_agg['CategoryName'],
        values=df_pie_agg['TotalVenta'],
        hole=0.55,
        marker=dict(colors=PALETTE, line=dict(color=COLOR_BG, width=2)),
        textinfo='percent',
        textfont=dict(size=10, color=COLOR_TEXT),
        showlegend=True
    ))
    fig5.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        height=320,
        annotations=[dict(
            text=f'<b>${total_donut/1e6:.1f}M</b>',  # ← total dinámico
            x=0.5, y=0.5, font=dict(size=16, color=COLOR_TEXT),
            showarrow=False
        )]
    )
    fig5.update_layout(legend=dict(font=dict(size=9, color=COLOR_MUTED), bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center; color:{COLOR_MUTED}; font-size:0.72rem; padding:8px 0'>
    Julián Cabello · Data Analyst · 
    <a href='https://github.com/Julian-cabello' style='color:{COLOR_PRIMARY}'>GitHub</a> · 
    Dataset: Northwind Traders (Microsoft) · SQLite
</div>
""", unsafe_allow_html=True)