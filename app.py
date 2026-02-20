import streamlit as st
import pandas as pd



def load_data():
    df = pd.read_csv("spotify.csv")
    return df
    
st.title("Dashboard Musical")
df = load_data()

#filtros 
st.sidebar.header("Filtros")

artistas = st.sidebar.multiselect(
    "Artista",
    sorted(df["artist_name"].dropna().unique()),
    default=sorted(df["artist_name"].dropna().unique())
)

album_type = st.sidebar.multiselect(
    "Filtrar por Tipo de Álbum",
    options=df["album_type"].unique(),
    default=df["album_type"].unique()
)

pop_range = st.sidebar.slider(
    "Rango de Popularidad",
    0, 100, (0, 100)
)

#Crear columnas
df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower().str.replace(" ", "_")

#CONVERTIR FECHA 
df["album_release_date"] = pd.to_datetime(df["album_release_date"])
df["year"] = df["album_release_date"].dt.year

anio = st.sidebar.slider(
    "Año de Lanzamiento",
    df["year"].min(),
    df["year"].max(),
    (df["year"].min(), df["year"].max())
)

# Aplicar filtros 
df_filtrado = df[
    (df["artist_name"].isin(artistas)) &
    (df["album_type"].isin(album_type)) &
    (df["artist_popularity"].between(pop_range[0], pop_range[1])) &
    (df["year"].between(anio[0], anio[1]))
]
 


 #Graficos 

tab1, tab2, tab3 = st.tabs([" KPIs", "Gráficos", " Tabla"])
with tab1:

# KPIs
  st.subheader(" Métricas principales")
 
col1, col2, col3, col4 = st.columns(4)
 
avg_pop = round(df_filtrado["artist_popularity"].mean(), 2)
total_artistas = df_filtrado["artist_name"].nunique()
avg_duration = round(df_filtrado["track_duration_min"].mean(), 2)
total_canciones = len(df_filtrado)
 
pop_por_año = df_filtrado.groupby("year")["artist_popularity"].mean()
growth = round(pop_por_año.pct_change().mean() * 100, 2)
 
col1.metric("Popularidad Promedio", avg_pop)
col2.metric("Total Artistas", total_artistas)
col3.metric("Duración Promedio", f"{avg_duration} min")
col4.metric("Total Canciones", total_canciones)

with tab2:
 
    st.subheader(" Top 10 artistas más populares")
    top_artistas = (
        df_filtrado.groupby("artist_name")["artist_popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_artistas)
 
    st.subheader(" Duración vs Popularidad")
    scatter_data = df_filtrado[["track_duration_min", "artist_popularity"]]
    st.scatter_chart(scatter_data)
 
    st.subheader(" Popularidad por año y tipo de álbum")
    pop_album = (
        df_filtrado.groupby(["year", "album_type"])["artist_popularity"]
        .mean()
        .unstack()
    )
    st.bar_chart(pop_album)
 