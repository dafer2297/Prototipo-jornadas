import streamlit as st
import time
import base64

# --- CONFIGURACIÓN PRINCIPAL ---
st.set_page_config(page_title="Torneo General - Calendario", layout="wide")

# --- CSS: DISEÑO BASADO EN TUS MOCKUPS (image_12, image_13, image_14) ---
css = """
<style>
/* Reset de colores de fondo */
.stApp { background-color: #f0f2f6; }

/* Tipografía y colores base */
h1, h2, h3 { color: #1a237e !important; } /* Azul oscuro */
h4 { color: #d32f2f !important; margin-bottom: 2px !important;} /* Rojo */

/* --- CABECERA ESTILO image_12.png --- */
.header-top-bar {
    background-color: #d32f2f; /* Franja roja superior */
    height: 15px;
    width: 100%;
    margin-top: -60px; /* Ajuste para Streamlit */
    margin-bottom: 10px;
}
.header-title {
    text-align: center;
    color: #1a237e;
    font-weight: 800;
    font-size: 14px;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

/* --- CARRUSEL DE EQUIPOS --- */
.carrusel-container {
    background-color: #1a237e;
    border-radius: 12px;
    border: 3px solid #d32f2f;
    padding: 15px 5px 5px 5px;
    margin-bottom: 20px;
}
[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    gap: 15px !important;
    padding-bottom: 10px !important;
    -webkit-overflow-scrolling: touch;
}
[data-testid="column"] {
    min-width: 70px !important;
    max-width: 70px !important;
    flex: 0 0 70px !important;
    display: flex;
    flex-direction: column;
    align-items: center;
}
/* Botones invisibles sobre los logos para hacerlos clickeables */
.logo-btn button {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    width: 60px !important;
    height: 60px !important;
}
.logo-btn button:hover { background-color: rgba(255,255,255,0.2) !important; border-radius: 50%; }

/* --- BLOQUES DE DÍAS Y TARJETAS --- */
.dia-titulo {
    color: #1a237e;
    font-size: 28px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 10px;
}
/* Estilo de la tarjeta blanca con borde azul */
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    background-color: white !important;
    border: 2px solid #1a237e !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    padding: 0 !important; /* Quitamos el padding por defecto para la cabecera azul */
    overflow: hidden;
}

/* Cabecera azul dentro de la tarjeta */
.tarjeta-header {
    background-color: #1a237e;
    color: white;
    padding: 8px 15px;
    font-weight: bold;
    font-size: 16px;
    display: flex;
    align-items: center;
}
.tarjeta-content {
    padding: 15px;
}

/* Lista de partidos compacta */
.partido-fila {
    font-size: 14px;
    color: #333;
    margin-bottom: 8px;
    display: flex;
    justify-content: flex-start;
}
/* Botón Rojo (Ver más detalles) */
.btn-rojo button {
    background-color: #d32f2f !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    width: 100% !important;
    padding: 8px !important;
    margin-top: 10px !important;
    box-shadow: 0 2px 4px rgba(211,47,47,0.4) !important;
}
.btn-rojo button:hover { background-color: #b71c1c !important; }

/* Botón de retroceso */
.btn-back button {
    background-color: transparent !important;
    color: #1a237e !important;
    border: none !important;
    font-size: 18px !important;
    padding: 0 !important;
    justify-content: flex-start !important;
}

/* Animación de carga */
.spin-logo { animation: spin 1s linear infinite; width: 120px; display: block; margin: 0 auto; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- BASE DE DATOS FAKE (Simulando partidos y deportes) ---
equipos = ["San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", "Sígsig Sporting", "Cutchil", "Güel", "San Bartolomé"]

datos_torneo = {
    "Lunes": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "14:00", "eq1": "Profesionales", "eq2": "San Sebastián", "marcador": "2 - 1", "estado": "Fin"},
            {"hora": "15:00", "eq1": "Dangers", "eq2": "Cutchil", "marcador": "0 - 3", "estado": "Fin"},
            {"hora": "16:00", "eq1": "Estudiantes", "eq2": "Atlético", "marcador": "1 - 1", "estado": "Fin"}
        ]},
        {"deporte": "🏀 Básquetbol - Femenino", "partidos": [
            {"hora": "18:00", "eq1": "Profesionales", "eq2": "Güel", "marcador": "", "estado": "Pendiente"},
            {"hora": "19:00", "eq1": "Sauces", "eq2": "Sigsales", "marcador": "", "estado": "Pendiente"}
        ]}
    ],
    "Martes": [
        {"deporte": "⚽ Fulbito - Sub 15", "partidos": [
            {"hora": "14:00", "eq1": "Llactazhungo", "eq2": "San Bartolomé", "marcador": "", "estado": "Pendiente"},
            {"hora": "15:00", "eq1": "Sígsig Sporting", "eq2": "Siete Estrellas", "marcador": "", "estado": "Pendiente"}
        ]},
        {"deporte": "♟️ Ajedrez (Categoría Única)", "partidos": [
            # Evento de un solo día
            {"hora": "10:00", "eq1": "Coliseo Parroquial", "eq2": "Torneo General", "marcador": "", "estado": "Pendiente"} 
        ]}
    ]
}


# --- CONTROL DE ESTADO DE NAVEGACIÓN ---
if "pantalla_actual" not in st.session_state:
    st.session_state.pantalla_actual = "HOME"
if "filtro_equipo" not in st.session_state:
    st.session_state.filtro_equipo = None
if "filtro_deporte" not in st.session_state:
    st.session_state.filtro_deporte = None
if "cargando" not in st.session_state:
    st.session_state.cargando = True # Activa la pantalla de carga la primera vez

# --- FUNCIÓN: PANTALLA DE CARGA ---
if st.session_state.cargando:
    pantalla_carga = st.empty()
    with pantalla_carga.container():
        try:
            with open("logo.png", "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            st.markdown(f'<div style="height: 60vh; display: flex; flex-direction: column; justify-content: center;"><img src="data:image/png;base64,{img_data}" class="spin-logo"><h3 style="text-align:center; margin-top:20px;">Cargando calendario...</h3></div>', unsafe_allow_html=True)
        except:
             st.markdown('<div style="height: 60vh; display: flex; justify-content: center; align-items: center;"><h3>Cargando...</h3></div>', unsafe_allow_html=True)
    time.sleep(1.5)
    pantalla_carga.empty()
    st.session_state.cargando = False


# --- FUNCIÓN: DIBUJAR CABECERA Y CARRUSEL ---
def dibujar_cabecera():
    st.markdown('<div class="header-top-bar"></div>', unsafe_allow_html=True)
    
    # Si estamos viendo un equipo en específico, mostramos botón de regresar
    if st.session_state.filtro_equipo:
        st.markdown(f'<div class="header-title">SIGUIENDO A: {st.session_state.filtro_equipo.upper()}</div>', unsafe_allow_html=True)
        col_back, _ = st.columns([1, 5])
        with col_back:
            st.markdown('<div class="btn-back">', unsafe_allow_html=True)
            if st.button("← Ver todo el torneo"):
                st.session_state.filtro_equipo = None
                st.session_state.pantalla_actual = "HOME"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="header-title">TORNEO GENERAL - CALENDARIO</div>', unsafe_allow_html=True)
        
        # El Carrusel azul solo se muestra si NO hay filtro de equipo
        st.markdown('<div class="carrusel-container">', unsafe_allow_html=True)
        cols = st.columns(len(equipos))
        for i, col in enumerate(cols):
            with col:
                # Usamos el logo blanco de prueba
                try:
                    st.image("prueba_logo.png", width=50)
                except:
                    st.write("🛡️")
                # Botón transparente para filtrar
                st.markdown('<div class="logo-btn">', unsafe_allow_html=True)
                if st.button(" ", key=f"btn_{equipos[i]}"):
                    st.session_state.filtro_equipo = equipos[i]
                    st.session_state.pantalla_actual = "HOME" # Recarga la home pero filtrada
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# --- RENDERIZADO DE PANTALLAS ---

if st.session_state.pantalla_actual == "HOME":
    dibujar_cabecera()
    
    # Recorremos la base de datos por días
    for dia, deportes in datos_torneo.items():
        # Bandera para saber si hay partidos de ese equipo este día
        dia_tiene_partidos = False 
        html_tarjetas = ""

        for deporte_info in deportes:
            nombre_deporte = deporte_info["deporte"]
            partidos = deporte_info["partidos"]
            
            # FILTRO: Si hay un equipo seleccionado, revisamos si juega en este deporte
            partidos_a_mostrar = []
            if st.session_state.filtro_equipo:
                for p in partidos:
                    if st.session_state.filtro_equipo in [p["eq1"], p["eq2"]]:
                        partidos_a_mostrar.append(p)
            else:
                partidos_a_mostrar = partidos

            # Si hay partidos para mostrar, construimos la tarjeta
            if len(partidos_a_mostrar) > 0:
                dia_tiene_partidos = True
                
                with st.container(border=True):
                    # Cabecera azul de la tarjeta
                    st.markdown(f'<div class="tarjeta-header">{nombre_deporte}</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
                    # Lista de partidos
                    for p in partidos_a_mostrar:
                        if "Ajedrez" in nombre_deporte:
                            # Formato especial un solo día
                            st.markdown(f'<div class="partido-fila">{p["hora"]} | {p["eq1"]}</div>', unsafe_allow_html=True)
                        else:
                            # Formato normal equipos
                            st.markdown(f'<div class="partido-fila">{p["hora"]} | {p["eq1"]} vs. {p["eq2"]}</div>', unsafe_allow_html=True)
                    
                    # Botón rojo
                    st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                    if st.button("Ver más detalles", key=f"detalle_{dia}_{nombre_deporte}"):
                        st.session_state.pantalla_actual = "DETALLE"
                        st.session_state.filtro_deporte = nombre_deporte
                        st.rerun()
                    st.markdown('</div></div>', unsafe_allow_html=True)
                st.write("") # Espacio
        
        # Solo dibujamos el título del DÍA si hay tarjetas debajo
        if dia_tiene_partidos:
            st.markdown(f'<div class="dia-titulo">Día {dia}</div>', unsafe_allow_html=True)
            # Volvemos a recorrer para dibujar realmente los contenedores de Streamlit debajo del título
            # (Lo anterior era para verificar si el día no quedaba vacío por el filtro)


elif st.session_state.pantalla_actual == "DETALLE":
    # --- PANTALLA 2: VISTA DETALLADA DEL DEPORTE (Estilo Champions) ---
    st.markdown('<div class="header-top-bar"></div>', unsafe_allow_html=True)
    
    col_back, col_title = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="btn-back">', unsafe_allow_html=True)
        if st.button("← Volver"):
            st.session_state.pantalla_actual = "HOME"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_title:
        st.markdown(f'<h3 style="margin:0; padding-top:5px;">{st.session_state.filtro_deporte}</h3>', unsafe_allow_html=True)
    
    st.write("")
    
    # Tarjeta de Resumen (Sección A)
    with st.container(border=True):
        st.markdown(f'<div class="tarjeta-header">RESUMEN DE PARTIDOS</div>', unsafe_allow_html=True)
        st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
        
        # Aquí buscaríamos en la BD real los 3 partidos más relevantes
        st.markdown('<div class="partido-fila" style="justify-content: space-between;"><span>14:00 | Profesionales vs. San Sebastián</span> <span style="font-weight:bold;">2 - 1</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="partido-fila" style="justify-content: space-between;"><span>15:00 | Dangers vs. Cutchil</span> <span style="font-weight:bold;">0 - 3</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="partido-fila" style="justify-content: space-between;"><span>16:00 | Estudiantes vs. Atlético</span> <span style="font-weight:bold;">1 - 1</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("Ver más partidos", key="modal_partidos"):
            # Aquí iría la lógica del MODAL OSCURO (En Streamlit usamos st.dialog o st.expander como alternativa)
            st.info("ℹ️ Al presionar esto, subirá el cuadro negro desde abajo con el calendario completo.")
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.write("")
    
    # Tarjetas de Posiciones (Sección C)
    if "Ajedrez" not in st.session_state.filtro_deporte:
        with st.container(border=True):
            st.markdown(f'<div class="tarjeta-header" style="background-color:#e0e0e0; color:#333;">Grupo A</div>', unsafe_allow_html=True)
            st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
            st.markdown('**TEAM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; P &nbsp; GF &nbsp; GC &nbsp; +/-**')
            st.markdown('🛡️ Cutchil &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3 &nbsp;&nbsp; 3 &nbsp;&nbsp; 0 &nbsp;&nbsp; +3')
            st.markdown('🛡️ Profesionales &nbsp;&nbsp;&nbsp;&nbsp; 3 &nbsp;&nbsp; 2 &nbsp;&nbsp; 1 &nbsp;&nbsp; +1')
            st.markdown('</div>', unsafe_allow_html=True)
