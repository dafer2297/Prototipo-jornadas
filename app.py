import streamlit as st
import time

# 1. Configuración principal de la página
st.set_page_config(page_title="Jornadas Deportivas", layout="wide")

# --- PANTALLA DE CARGA (SPLASH SCREEN) ---
# Creamos un contenedor vacío
pantalla_carga = st.empty()

# Mostramos el GIF dentro del contenedor
with pantalla_carga.container():
    # Asegúrate de que el nombre coincida con tu archivo GIF
    st.image("logo_manzana.gif", use_container_width=True)

# Hacemos que la página espere 2.5 segundos
time.sleep(2.5)

# Borramos el GIF de la pantalla para mostrar la página web
pantalla_carga.empty()


# --- PÁGINA PRINCIPAL (VISTA DE HOY) ---
st.title("🏆 Jornadas Deportivas - Hoy")

# Carrusel superior de equipos (simulado con columnas)
st.write("### Equipos Participantes")
cols_logos = st.columns(6)
equipos = ["Manzanas FC", "Los Pumas", "Real Cuenca", "Atlético", "Halcones", "Titanes"]
for i, col in enumerate(cols_logos):
    col.button(equipos[i])

st.divider()

# Tarjetas de Partidos de Hoy
st.subheader("📅 Calendario del Día")

# Tarjeta 1: Fútbol Sub 12
with st.container(border=True):
    st.markdown("#### ⚽ Fútbol - Sub 12")
    st.write("🕒 **14:00** | Manzanas FC  vs.  Los Pumas")
    st.write("🕒 **16:00** | Real Cuenca  vs.  Titanes")
    
    # Botón para desplegar más detalles
    if st.button("Ver todo el calendario y tabla de posiciones", key="btn_sub12"):
        st.info("Aquí se desplegará hacia abajo el calendario infinito y la tabla ancha de posiciones.")

st.write("") # Espaciador

# Tarjeta 2: Fútbol Categoría Barrio
with st.container(border=True):
    st.markdown("#### ⚽ Fútbol - Categoría Barrio")
    st.write("🕒 **18:00** | Atlético  vs.  Halcones")
    
    if st.button("Ver todo el calendario y tabla de posiciones", key="btn_barrio"):
        st.info("Aquí se desplegará hacia abajo el calendario infinito y la tabla ancha de posiciones.")

st.write("") 

# Tarjeta 3: Ecuavoley
with st.container(border=True):
    st.markdown("#### 🏐 Ecuavoley")
    st.write("🕒 **19:30** | Equipo A  vs.  Equipo B")
    
    if st.button("Ver todo el calendario y tabla de posiciones", key="btn_ecuavoley"):
        st.info("Aquí se desplegará hacia abajo el calendario infinito y la tabla ancha de posiciones.")
