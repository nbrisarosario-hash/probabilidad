import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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

elif opcion == "Prueba Z":
    st.header("3. Ejecución de la Prueba Z")
    
    if st.session_state.df is not None:
        columna = st.selectbox("Selecciona los datos para la prueba", st.session_state.df.columns)
        datos = st.session_state.df[columna].dropna()
        
        # Parámetros de la prueba
        mu_h0 = st.number_input("Media poblacional hipotética (H0)", value=0.0)
        sigma = st.number_input("Desviación estándar poblacional (conocida)", value=1.0)
        alpha = st.slider("Nivel de significancia (alpha)", 0.01, 0.10, 0.05)
        
        if st.button("Calcular Prueba Z"):
            # Cálculos estadísticos
            x_bar = datos.mean()
            n = len(datos)
            z_stat = (x_bar - mu_h0) / (sigma / np.sqrt(n))
            p_val = 2 * (1 - stats.norm.cdf(abs(z_stat))) # Bilateral
            
            # Resultados
            st.subheader("Resultados:")
            col1, col2 = st.columns(2)
            col1.metric("Estadístico Z", f"{z_stat:.4f}")
            col2.metric("p-valor", f"{p_val:.4f}")
            
            if p_val < alpha:
                st.error(f"Rechazamos la hipótesis nula (H0). Hay evidencia suficiente.")
            else:
                st.success(f"No se rechaza la hipótesis nula (H0). No hay evidencia suficiente.")
                
    else:
        st.warning("Por favor, primero carga un archivo CSV en la sección 'Carga de Datos'.")





