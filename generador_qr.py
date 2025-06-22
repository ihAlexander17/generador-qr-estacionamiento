import streamlit as st
import qrcode
from PIL import Image
import random
from datetime import datetime
import pytz
import io
import json

def generar_placa():
    letras = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = ''.join(random.choices("0123456789", k=3))
    return letras + numeros

st.title("Generador de Código QR para Estacionamiento")

# Usamos session_state para controlar si ya se descargó el QR
if 'descargado' not in st.session_state:
    st.session_state.descargado = False

# Solo mostrar el input si aún no se ha descargado
if not st.session_state.descargado:
    nombre_usuario = st.text_input("Ingresa tu nombre:")
else:
    nombre_usuario = None  # Para evitar errores más adelante

if nombre_usuario and not st.session_state.descargado:
    placa = generar_placa()

    zona_horaria = pytz.timezone("America/Mexico_City")
    hora_actual = datetime.now(zona_horaria).strftime("%Y-%m-%d %H:%M")

    # Crear el contenido del QR con hora de entrada
    contenido_qr = {
        "nombre": nombre_usuario,
        "placa": placa,
        "hora_entrada": hora_actual
    }

    # Convertir a JSON para el QR
    contenido_json = json.dumps(contenido_qr)

    # Generar imagen del QR
    qr_img = qrcode.make(contenido_json).convert("RGB")

    # Mostrar el QR
    st.image(qr_img, caption="Código QR Generado")

    # Convertir la imagen a bytes para permitir descarga
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Botón de descarga
    st.download_button(
        label="Descargar mi QR",
        data=buffer,
        file_name=f"{placa}_qr.png",
        mime="image/png"
    )

    # Mostrar los datos de manera clara
    st.subheader("🧾 Datos de tu ticket de entrada:")
    st.write(f"👤 Nombre: {nombre_usuario}")
    st.write(f"🚗 Placa: {placa}")
    st.write(f"⏰ Hora de Entrada: {hora_actual}")

    # Mensaje de advertencia para el usuario
    st.info("📌 No cierres esta página hasta escanear o descargar tu código QR.")

    # Marcar como descargado
    st.session_state.descargado = True

elif st.session_state.descargado:
    st.success("Ya descargaste el QR. Si deseas generar otro, por favor recarga la página.")

else:
    st.warning("Por favor, ingresa tu nombre para generar el QR.")
