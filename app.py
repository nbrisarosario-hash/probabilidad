import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="App Estadística Prueba Z", layout="wide")

st.sidebar.title("Menú de Navegación")
opcion = st.sidebar.selectbox("Selecciona un Módulo", 
    ["Carga de Datos", "Visualización", "Prueba Z", "Asistente IA"])

# --- PERSISTENCIA DE DATOS ---
if 'df' not in st.session_state:
    st.session_state.df = None

# --- MÓDULO 1: CARGA DE DATOS ---
if opcion == "Carga de Datos":
    st.header("Carga o Generación de Datos")
    metodo = st.radio("¿Cómo quieres ingresar los datos?", ["Subir CSV", "Generar Datos Sintéticos"])
    
    if metodo == "Subir CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            st.session_state.df = pd.read_csv(archivo)
            st.success("¡Archivo cargado!")
    else:
        st.info("Genera datos normales para probar la app")
        n_sintetico = st.number_input("Tamaño de muestra (n)", min_value=30, value=100)
        media_sintetica = st.number_input("Media deseada", value=50.0)
        desv_sintetica = st.number_input("Desviación estándar", value=5.0)
        if st.button("Generar Datos"):
            datos = np.random.normal(media_sintetica, desv_sintetica, n_sintetico)
            st.session_state.df = pd.DataFrame(datos, columns=["Valores_Generados"])
            st.success("Datos generados correctamente")

    if st.session_state.df is not None:
        st.write("Vista previa de los datos:", st.session_state.df.head())

# --- MÓDULO 2: VISUALIZACIÓN ---
elif opcion == "Visualización":
    st.header("Visualización de Distribuciones")
    if st.session_state.df is not None:
        # Filtramos solo columnas numéricas para evitar el error de tu imagen
        cols_numericas = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not cols_numericas:
            st.error("No hay columnas numéricas en tus datos.")
        else:
            columna = st.selectbox("Selecciona variable", cols_numericas)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Histograma y KDE")
                fig, ax = plt.subplots()
                sns.histplot(st.session_state.df[columna], kde=True, ax=ax, color="skyblue")
                st.pyplot(fig)
            
            with col2:
                st.subheader("Boxplot")
                fig, ax = plt.subplots()
                sns.boxplot(x=st.session_state.df[columna], ax=ax, color="lightcoral")
                st.pyplot(fig)

            # --- RESPUESTAS DENTRO DE LA APP (Criterio académico) ---
            st.divider()
            st.subheader("Análisis de la Distribución")
            sesgo = st.session_state.df[columna].skew()
            st.write(f"**Sesgo:** {sesgo:.4f}")
            if abs(sesgo) < 0.5:
                st.write("- La distribución parece **Simétrica (Normal)**.")
            else:
                st.write(f"- Existe un **Sesgo {'Positivo' if sesgo > 0 else 'Negativo'}**.")
    else:
        st.warning("Carga datos primero.")

# --- MÓDULO 3: PRUEBA Z ---
elif opcion == "Prueba Z":
    st.header("Ejecución de Prueba Z")
    if st.session_state.df is not None:
        cols_numericas = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()
        columna = st.selectbox("Variable para la prueba", cols_numericas)
        datos = st.session_state.df[columna].dropna()
        
        mu_h0 = st.number_input("Hipótesis Nula (μ H0)", value=0.0)
        sigma = st.number_input("Varianza poblacional (σ conocida)", value=1.0, min_value=0.01)
        tipo = st.selectbox("Tipo de Prueba (H1)", ["Bilateral", "Cola Izquierda", "Cola Derecha"])
        alpha = st.slider("Significancia (α)", 0.01, 0.10, 0.05, step=0.01)
        
        if st.button("Calcular"):
            x_bar = datos.mean()
            n = len(datos)
            z_stat = (x_bar - mu_h0) / (sigma / np.sqrt(n))
            
            # P-value según tipo
            if tipo == "Bilateral":
                p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            elif tipo == "Cola Izquierda":
                p_val = stats.norm.cdf(z_stat)
            else:
                p_val = 1 - stats.norm.cdf(z_stat)
            
            st.metric("Estadístico Z", f"{z_stat:.4f}")
            st.metric("P-Value", f"{p_val:.4f}")

            # GRAFICA DE REGIÓN CRÍTICA
            x = np.linspace(-4, 4, 1000)
            y = stats.norm.pdf(x, 0, 1)
            fig, ax = plt.subplots()
            ax.plot(x, y, label='Normal Estándar')
            ax.axvline(z_stat, color='red', linestyle='--', label=f'Z={z_stat:.2f}')
            
            # Sombrear región de rechazo (Bilateral ejemplo)
            z_crit = stats.norm.ppf(1 - alpha/2)
            ax.fill_between(x, 0, y, where=(abs(x) > z_crit), color='red', alpha=0.3, label='Región Rechazo')
            st.pyplot(fig)

            if p_val < alpha:
                st.error("Resultado: RECHAZAR H0")
            else:
                st.success("Resultado: NO RECHAZAR H0")
                
            # Guardamos resultados para la IA
            st.session_state.resumen_z = f"Z={z_stat}, p={p_val}, n={n}, media={x_bar}, H0={mu_h0}, alpha={alpha}"

# --- MÓDULO 4: ASISTENTE IA ---
elif opcion == "Asistente IA":
    st.header("Interpretación con Gemini")
    st.write("Copia el resumen de la Prueba Z y pregúntale a la IA.")
    if 'resumen_z' in st.session_state:
        st.code(st.session_state.resumen_z)
        st.info("Próximo paso: Configurar API Key para enviar este texto automáticamente.")
    else:
        st.warning("Primero ejecuta una Prueba Z.")
