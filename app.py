import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Menú de Navegación")
opcion = st.sidebar.selectbox("Ir a:", ["Carga de Datos", "Visualización", "Prueba Z", "Asistente IA"])

# Inicializamos el dataframe en la sesión para que no se borre al cambiar de menú
if 'df' not in st.session_state:
    st.session_state.df = None

if opcion == "Carga de Datos":
    st.header("1. Carga de información")
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        st.session_state.df = pd.read_csv(archivo)
        st.success("¡Archivo cargado con éxito!")
        st.write(st.session_state.df.head())

elif opcion == "Visualización":
    st.header("2. Análisis Gráfico")
    if st.session_state.df is not None:
        columna = st.selectbox("Selecciona la columna a graficar", st.session_state.df.columns)
        fig, ax = plt.subplots()
        sns.histplot(st.session_state.df[columna], kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Primero carga un archivo en el menú 'Carga de Datos'")
