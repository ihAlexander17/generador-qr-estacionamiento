import streamlit as st
import qrcode
from PIL import Image
import random
from datetime import datetime

# Función para generar placas aleatorias al estilo México (3 letras + 3 números)
def generar_placa():
    letras = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = ''.join(random.choices("0123456789", k=3))
    return letras + numeros

# Título de la página
st.title("Generador de Código QR para Estacionamiento")

# Solicitar el nombre del usuario
nombre_usuario = st.text_input("Ingresa tu nombre:")

# Si el nombre fue ingresado
if nombre_usuario:
    # Generar placa aleatoria
    placa = generar_placa()

    # Obtener la hora actual
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Crear el contenido del QR: Nombre + Placa + Hora actual
    datos = f"Nombre: {nombre_usuario} | Placa: {placa} | Hora: {hora_actual}"

    # Generar y convertir la imagen del QR a formato compatible
    qr_img = qrcode.make(datos)
    qr_img = qr_img.convert("RGB")
    st.image(qr_img, caption="Código QR Generado")

    # Mostrar los datos generados para el usuario
    st.subheader("Datos Generados:")
    st.write(f"Nombre: {nombre_usuario}")
    st.write(f"Placa: {placa}")
    st.write(f"Hora de Generación: {hora_actual}")

    # Mostrar el contenido del QR como texto
    st.success(f"Contenido del QR: {datos}")
else:
    st.warning("Por favor, ingresa tu nombre para generar el QR.")
