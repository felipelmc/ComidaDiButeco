import streamlit as st
import pandas as pd
import folium
from folium import Popup, CustomIcon
from streamlit_folium import folium_static

st.set_page_config(layout="wide")  # Define o layout da página como wide

@st.cache_data
def load_data():
    return pd.read_excel("datasets/butecos_2025_detailed.xlsx")

# Carrega os dados
df = load_data()

# Filtros na barra lateral
st.sidebar.header("Filtros")

ufs = df['UF'].dropna().unique()
uf_selecionado = st.sidebar.selectbox("Selecione o estado (UF):", ["Todos"] + sorted(ufs.tolist()))

if uf_selecionado != "Todos":
    df = df[df['UF'] == uf_selecionado]

cidades = df['Cidade'].dropna().unique()
cidade_selecionada = st.sidebar.selectbox("Selecione a cidade:", ["Todas"] + sorted(cidades.tolist()))

if cidade_selecionada != "Todas":
    df = df[df['Cidade'] == cidade_selecionada]

bairros = df['Bairro'].dropna().unique()
bairro_selecionado = st.sidebar.selectbox("Selecione o bairro:", ["Todos"] + sorted(bairros.tolist()))

if bairro_selecionado != "Todos":
    df = df[df['Bairro'] == bairro_selecionado]

# Título
st.title("🍻Comida di Buteco 2025🍻")
st.markdown("Esse é um mapa com informações de **(praticamente) todos** os butecos do **Comida di Buteco 2025**! Feito por [@felipelmc](https://www.instagram.com/felipelmc/)")

# Centralização do mapa
if uf_selecionado == "Todos":
    mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)  # Brasil inteiro
else:
    lat_media = df["lat"].mean()
    lon_media = df["lon"].mean()
    mapa = folium.Map(location=[lat_media, lon_media], zoom_start=12)  # Região filtrada

# Define o caminho para o ícone personalizado
icon_url = "img/988934.png"

# Adiciona os marcadores ao mapa
for _, row in df.iterrows():
    nome = row['Nome']
    prato = row["Detalhamento Prato"]
    telefone = row['Telefone']
    horario = row['Horario']
    endereco = row['Endereço']
    cidade = row['Cidade']
    uf = row['UF']
    lat = row['lat']
    lon = row['lon']
    link = row['Detalhes']
    imagem = row['Imagem']

    # Verifica se latitude ou longitude estão ausentes
    if pd.isna(lat) or pd.isna(lon):
        continue

    # Cria um ícone personalizado para cada marcador
    icon = CustomIcon(icon_url, icon_size=(25, 25))

    # Cria o conteúdo do popup
    html = f"""
    <h3><strong>{nome}</strong></h3><br>
    <strong>Prato:</strong> {prato}<br><br>
    
    <strong>Endereço:</strong> {endereco}<br>
    {telefone}<br>
    <strong>Horário:</strong> {horario}<br> <br>
    
    <a href="{link}" target="_blank">Ver mais detalhes</a><br>
    <img src="{imagem}" width="220px">
    """
    popup = Popup(html, max_width=250)

    # Adiciona o marcador ao mapa
    folium.Marker(location=[lat, lon], popup=popup, icon=icon).add_to(mapa)

# Exibe o mapa no Streamlit
folium_static(mapa, width=1400, height=500)
