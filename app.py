import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Prueba Z", layout="centered")

st.title("📊 Prueba Z - Test de API")

st.write("Ingresa los datos para probar tu API de prueba Z")

# Inputs
data_input = st.text_input("Datos (separados por coma)", "10,12,9,11,10,13")
mu = st.number_input("Media poblacional (mu)", value=10.0)
sigma = st.number_input("Desviación estándar (sigma)", value=2.0)
alpha = st.number_input("Nivel de significancia (alpha)", value=0.05)
tipo = st.selectbox("Tipo de prueba", ["bilateral", "izquierda", "derecha"])

# Convertir datos
try:
    data = [float(x) for x in data_input.split(",")]
    df = pd.DataFrame(data, columns=["valores"])

    st.write("📊 Datos:")
    st.dataframe(df)

except:
    st.error("❌ Error en los datos. Usa solo números separados por coma.")
    st.stop()

# Botón para llamar API
if st.button("🚀 Enviar a API"):

    payload = {
        "data": data,
        "mu": mu,
        "sigma": sigma,
        "alpha": alpha,
        "tipo": tipo
    }

    st.write("📡 Enviando:")
    st.json(payload)

    try:
        url = "http://127.0.0.1:3000/prueba-z"  # cambia si tu endpoint es otro
        response = requests.post(url, json=payload)

        st.success("✅ Respuesta de la API:")
        st.json(response.json())

    except Exception as e:
        st.error("❌ No se pudo conectar a la API")
        st.write(e)