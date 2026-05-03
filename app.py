import streamlit as st
import time
import base64

# Configuración de la página
st.set_page_config(page_title="Jornadas Deportivas", layout="wide")

# --- 1. INYECCIÓN DE CSS (COLORES Y ANIMACIÓN ROTATORIA) ---
css = """
<style>
/* Animación para que el logo gire */
.spin-logo {
    animation: spin 1.5s linear infinite;
    width: 150px; /* Tamaño del logo cargando */
    display: block;
    margin: 0 auto;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Tema de la página basado en el escudo */
h1, h2, h3 {
    color: #1a237e; /* Azul oscuro del escudo */
}
h4 {
    color: #d32f2f; /* Rojo vivo del escudo */
}
hr {
    border-top: 3px solid #d32f2f; 
}

/* Estilo de los botones */
div[data-testid="stButton"] > button {
    background-color: #1a237e;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    transition: 0.3s;
}
div[data-testid="stButton"] > button:hover {
    background-color: #d32f2f;
    color: white;
    border: none;
}
</style>
"""
# Aplicamos el CSS a la página
st.markdown(css, unsafe_allow_html=True)


# --- 2. PANTALLA DE CARGA (SPLASH SCREEN ROTATORIO) ---
pantalla_carga = st.empty()

with pantalla_carga.container():
    # Leemos la imagen local y la convertimos para que el HTML la pueda animar
    try:
        with open("logo.png", "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_html = f'<img src="data:image/png;base64,{img_data}" class="spin-logo">'
    except FileNotFoundError:
        # Si aún no guardas la imagen en la carpeta, sale esto por defecto para que no de error
        img_html = '<div class="spin-logo" style="font-size:50px; text-align:center;">⚽</div>'
        st.warning("⚠️ Recuerda guardar tu imagen transparente como 'logo.png' en esta carpeta.")

    # Estructura HTML para centrar el logo girando
    html_loader = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 60vh; flex-direction: column;">
        {img_html}
        <h3 style="color: #1a237e; margin-top: 25px;">Cargando calendario...</h3>
    </div>
    """
    st.markdown(html_loader, unsafe_allow_html=True)

# Simulamos que la página está buscando los partidos (3 segundos)
time.sleep(3)

# Borramos la pantalla de carga para dar paso a la información
pantalla_carga.empty()


# --- 3. PÁGINA PRINCIPAL (VISTA DE HOY) ---
st.title("🏆 Jornadas Deportivas - Hoy")

st.markdown("### Equipos Participantes")
cols_logos = st.columns(6)
equipos = ["Los Profesionales", "Liga Central", "Atlético", "Halcones", "Titanes", "Real"]
for i, col in enumerate(cols_logos):
    col.button(equipos[i])

st.divider()

st.subheader("📅 Calendario del Día")

# Tarjeta de categoría (Fútbol Sub 12)
with st.container(border=True):
    st.markdown("#### ⚽ Fútbol - Sub 12")
    st.write("🕒 **14:00** | Los Profesionales  vs.  Liga Central")
    st.write("🕒 **16:00** | Real  vs.  Titanes")
    st.button("Ver todo el calendario y posiciones", key="btn_sub12")

st.write("")

# Tarjeta de categoría (Fútbol Barrio)
with st.container(border=True):
    st.markdown("#### ⚽ Fútbol - Categoría Barrio")
    st.write("🕒 **18:00** | Atlético  vs.  Halcones")
    st.button("Ver todo el calendario y posiciones", key="btn_barrio")

st.write("")

# Tarjeta de categoría (Baloncesto Femenino)
with st.container(border=True):
    st.markdown("#### 🏀 Baloncesto - Femenino")
    st.write("🕒 **19:30** | Los Profesionales  vs.  Titanes")
    st.button("Ver todo el calendario y posiciones", key="btn_basket_fem")
