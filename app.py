import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import streamlit as st
import google.generativeai as genai

API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

# 1. At the beginning of your code:
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Inside the 'analizar_resultado_z' function:
def analizar_resultado_z(media_m, media_h, n, sigma, alpha, tipo_prueba, z_stat, p_value):
    model_ia = genai.GenerativeModel('gemini-2.5-flash')  # <--- Changed here
    # ... rest of the code remains the same


    prompt = f"""
    Se realizó una prueba Z con los siguientes parámetros:
    - Media muestral = {media_m}, Media hipotética = {media_h}
    - n = {n}, sigma = {sigma}, alpha = {alpha}
    - Tipo de prueba = {tipo_prueba}
    - El estadístico Z fue = {z_stat}
    - El p-value fue = {p_value}

    ¿Se rechaza H0? Explica la decisión y si los supuestos de la prueba son razonables.
    """

    try:
        # IMPORTANTE: No uses "models/" antes del nombre si usas la versión más reciente
        response = model_ia.generate_content(prompt)
        return response.text
    except Exception as e:
        # Esto te dirá exactamente qué está pasando si falla
        return f"Error detallado: {str(e)}"



# --- SIDEBAR ---
st.sidebar.title("Menú de Navegación")
opcion = st.sidebar.selectbox(
    "Selecciona un Módulo",
    ["Carga de Datos", "Visualización", "Prueba Z", "Asistente IA"]
)

# --- PERSISTENCIA ---
if 'df' not in st.session_state:
    st.session_state.df = None

# --- MÓDULO 1 ---
if opcion == "Carga de Datos":
    st.header("Carga o Generación de Datos")

    metodo = st.radio(
        "¿Cómo quieres ingresar los datos?",
        ["Subir CSV", "Generar Datos Sintéticos"]
    )

    if metodo == "Subir CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            st.session_state.df = pd.read_csv(archivo)
            st.success("¡Archivo cargado!")
    else:
        n_sintetico = st.number_input("Tamaño de muestra (n)", min_value=30, value=100)
        media_sintetica = st.number_input("Media deseada", value=50.0)
        desv_sintetica = st.number_input("Desviación estándar", value=5.0)

        if st.button("Generar Datos"):
            datos = np.random.normal(media_sintetica, desv_sintetica, n_sintetico)
            st.session_state.df = pd.DataFrame(datos, columns=["Valores_Generados"])
            st.success("Datos generados correctamente")

    if st.session_state.df is not None:
        st.write(st.session_state.df.head())

# --- MÓDULO 2 ---
elif opcion == "Visualización":
    st.header("Visualización")

    if st.session_state.df is not None:
        cols = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()

        if cols:
            columna = st.selectbox("Selecciona variable", cols)

            fig, ax = plt.subplots()
            sns.histplot(st.session_state.df[columna], kde=True, ax=ax)
            st.pyplot(fig)

            sesgo = st.session_state.df[columna].skew()
            st.write(f"Sesgo: {sesgo:.4f}")
        else:
            st.error("No hay columnas numéricas.")
    else:
        st.warning("Carga datos primero.")

# --- MÓDULO 3 ---
elif opcion == "Prueba Z":
    st.header("Prueba Z")

    if st.session_state.df is not None:
        cols = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()
        columna = st.selectbox("Variable", cols)

        datos = st.session_state.df[columna].dropna()

        mu_h0 = st.number_input("μ H0", value=0.0)
        sigma = st.number_input("σ conocida", value=1.0, min_value=0.01)
        tipo = st.selectbox("Tipo", ["Bilateral", "Cola Izquierda", "Cola Derecha"])
        alpha = st.slider("α", 0.01, 0.10, 0.05)

        if st.button("Calcular"):
            x_bar = datos.mean()
            n = len(datos)

            z_stat = (x_bar - mu_h0) / (sigma / np.sqrt(n))

            if tipo == "Bilateral":
                p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            elif tipo == "Cola Izquierda":
                p_val = stats.norm.cdf(z_stat)
            else:
                p_val = 1 - stats.norm.cdf(z_stat)

            st.metric("Z", f"{z_stat:.4f}")
            st.metric("p-value", f"{p_val:.4f}")

            if p_val < alpha:
                st.error("RECHAZAR H0")
            else:
                st.success("NO RECHAZAR H0")

            # GUARDAMOS DATOS BIEN (no string)
            st.session_state.resultado_z = {
                "media_m": x_bar,
                "media_h": mu_h0,
                "n": n,
                "sigma": sigma,
                "alpha": alpha,
                "tipo": tipo,
                "z": z_stat,
                "p": p_val
            }

# --- MÓDULO 4 ---
elif opcion == "Asistente IA":
    st.header("Asistente IA")

    if "resultado_z" in st.session_state:
        datos = st.session_state.resultado_z
        st.write(datos)

        if st.button("Analizar con IA"):
            respuesta = analizar_resultado_z(
                datos["media_m"],
                datos["media_h"],
                datos["n"],
                datos["sigma"],
                datos["alpha"],
                datos["tipo"],
                datos["z"],
                datos["p"]
            )
            st.write(respuesta)
    else:
        st.warning("Primero ejecuta la Prueba Z.")