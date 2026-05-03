import streamlit as st
import time
import base64

# --- CONFIGURACIÓN PRINCIPAL ---
st.set_page_config(page_title="Torneo General - Calendario", layout="wide")

# --- CSS: DISEÑO CORREGIDO ---
css = """
<style>
.stApp { background-color: #f0f2f6; }
h1, h2, h3 { color: #1a237e !important; } 
h4 { color: #d32f2f !important; margin-bottom: 2px !important;} 

/* --- CABECERA --- */
.header-top-bar {
    background-color: #d32f2f; 
    height: 15px;
    width: 100%;
    margin-top: -60px; 
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
    gap: 5px !important;
    padding-bottom: 10px !important;
    -webkit-overflow-scrolling: touch;
}
/* Forzamos que las columnas del carrusel sean pequeñas */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    min-width: 80px !important;
    max-width: 80px !important;
    flex: 0 0 80px !important;
    display: flex;
    flex-direction: column;
    align-items: center;
}
/* Arreglamos los botones negros para que se vea el texto */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button p {
    color: white !important;
    font-size: 11px !important;
    white-space: normal !important;
    line-height: 1.1 !important;
    text-align: center !important;
}

/* --- BLOQUES DE DÍAS Y TARJETAS --- */
.dia-titulo {
    color: #1a237e;
    font-size: 28px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 10px;
    border-bottom: 2px solid #d32f2f;
    padding-bottom: 5px;
}
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    background-color: white !important;
    border: 2px solid #1a237e !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    padding: 0 !important; 
    overflow: hidden;
}
.tarjeta-header {
    background-color: #1a237e;
    color: white;
    padding: 8px 15px;
    font-weight: bold;
    font-size: 16px;
    display: flex;
    align-items: center;
}
.tarjeta-content { padding: 15px; }

.partido-fila {
    font-size: 14px;
    color: #333;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
}
.partido-info { flex: 1; }
.partido-marcador { font-weight: bold; color: #1a237e; margin-left: 10px; text-align: right;}

.btn-rojo button {
    background-color: #d32f2f !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    width: 100% !important;
    padding: 8px !important;
    margin-top: 10px !important;
}
.btn-rojo button:hover { background-color: #b71c1c !important; }

.btn-back button {
    background-color: transparent !important;
    color: #1a237e !important;
    border: none !important;
    font-size: 16px !important;
    padding: 0 !important;
    font-weight: bold !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- BASE DE DATOS EXTENDIDA (Lunes, Martes, Miércoles) ---
equipos = ["San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", "Sígsig", "Cutchil", "Güel", "San Bartolomé"]

datos_torneo = {
    "Lunes (Ayer)": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "14:00", "eq1": "Profesionales", "eq2": "San Sebastián", "marcador": "2 - 1"},
            {"hora": "15:00", "eq1": "Dangers", "eq2": "Cutchil", "marcador": "0 - 3"},
            {"hora": "16:00", "eq1": "Estudiantes", "eq2": "Atlético", "marcador": "1 - 1"}
        ]},
        {"deporte": "🏐 Ecuavoley - Masculino", "partidos": [
            {"hora": "18:00", "eq1": "Sigsales", "eq2": "Sígsig", "marcador": "2 - 0"},
            {"hora": "19:00", "eq1": "Güel", "eq2": "San Bartolomé", "marcador": "1 - 2"},
            {"hora": "20:00", "eq1": "Sauces", "eq2": "Llactazhungo", "marcador": "2 - 1"}
        ]}
    ],
    "Martes (Hoy)": [
        {"deporte": "🥅 Indor - Masculino", "partidos": [
            {"hora": "14:00", "eq1": "Profesionales", "eq2": "Dangers", "marcador": "5 - 2"},
            {"hora": "15:00", "eq1": "Cutchil", "eq2": "Estudiantes", "marcador": "Pendiente"},
            {"hora": "16:00", "eq1": "San Sebastián", "eq2": "Siete Estrellas", "marcador": "Pendiente"}
        ]},
        {"deporte": "♟️ Ajedrez (Categoría Única)", "partidos": [
            {"hora": "10:00", "eq1": "Coliseo Parroquial", "eq2": "", "marcador": "🥇 1er: Profesionales | 🥈 2do: Güel"}
        ]}
    ],
    "Miércoles (Mañana)": [
        {"deporte": "🏀 Básquetbol - Femenino", "partidos": [
            {"hora": "18:00", "eq1": "San Bartolomé", "eq2": "Sígsig", "marcador": "Pendiente"},
            {"hora": "19:00", "eq1": "Sigsales", "eq2": "Sauces", "marcador": "Pendiente"},
            {"hora": "20:00", "eq1": "Güel", "eq2": "Llactazhungo", "marcador": "Pendiente"}
        ]},
        {"deporte": "🚴 Ciclismo (Ruta Libre)", "partidos": [
            {"hora": "08:00", "eq1": "Parque Central (Salida)", "eq2": "", "marcador": "Pendiente"}
        ]}
    ]
}

# --- CONTROL DE ESTADOS ---
if "pantalla_actual" not in st.session_state:
    st.session_state.pantalla_actual = "HOME"
if "filtro_equipo" not in st.session_state:
    st.session_state.filtro_equipo = None
if "filtro_deporte" not in st.session_state:
    st.session_state.filtro_deporte = None

# --- FUNCIÓN DEL MODAL OSCURO (Calendario Completo) ---
@st.dialog("📅 Calendario Completo")
def modal_calendario(deporte_seleccionado):
    st.markdown(f"<h4 style='text-align:center;'>Todos los partidos de {deporte_seleccionado}</h4>", unsafe_allow_html=True)
    st.divider()
    
    # Buscamos todos los partidos de este deporte en todos los días
    hay_datos = False
    for dia, deportes in datos_torneo.items():
        for dep in deportes:
            if dep["deporte"] == deporte_seleccionado:
                hay_datos = True
                st.markdown(f"**{dia}**")
                for p in dep["partidos"]:
                    if "Ajedrez" in deporte_seleccionado or "Ciclismo" in deporte_seleccionado:
                        st.write(f"🕒 {p['hora']} | 📍 {p['eq1']} | {p['marcador']}")
                    else:
                        resultado = p['marcador'] if p['marcador'] != "Pendiente" else "vs."
                        st.write(f"🕒 {p['hora']} | {p['eq1']} **{resultado}** {p['eq2']}")
                st.write("") # Espacio
    
    if not hay_datos:
        st.info("No hay más partidos programados para esta categoría.")

# --- DIBUJAR CABECERA ---
def dibujar_cabecera():
    st.markdown('<div class="header-top-bar"></div>', unsafe_allow_html=True)
    if st.session_state.filtro_equipo:
        st.markdown(f'<div class="header-title">SIGUIENDO A: {st.session_state.filtro_equipo.upper()}</div>', unsafe_allow_html=True)
        col_back, _ = st.columns([1, 5])
        with col_back:
            st.markdown('<div class="btn-back">', unsafe_allow_html=True)
            if st.button("← Ver todo el torneo"):
                st.session_state.filtro_equipo = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="header-title">TORNEO GENERAL - CALENDARIO</div>', unsafe_allow_html=True)
        st.markdown('<div class="carrusel-container">', unsafe_allow_html=True)
        cols = st.columns(len(equipos))
        for i, col in enumerate(cols):
            with col:
                try:
                    st.image("prueba_logo.png", width=50)
                except:
                    st.write("🛡️")
                # AHORA SÍ PASAMOS EL NOMBRE DEL EQUIPO AL BOTÓN
                if st.button(equipos[i], key=f"btn_{equipos[i]}"):
                    st.session_state.filtro_equipo = equipos[i]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL (HOME) ---
if st.session_state.pantalla_actual == "HOME":
    dibujar_cabecera()
    
    for dia, deportes in datos_torneo.items():
        # Primero filtramos qué deportes tienen partidos hoy (o si el equipo seleccionado juega hoy)
        deportes_a_mostrar = []
        for dep in deportes:
            partidos_filtrados = []
            for p in dep["partidos"]:
                # Lógica del filtro de equipo
                if not st.session_state.filtro_equipo or st.session_state.filtro_equipo in [p["eq1"], p.get("eq2", "")]:
                    partidos_filtrados.append(p)
            
            if len(partidos_filtrados) > 0:
                deportes_a_mostrar.append({"deporte": dep["deporte"], "partidos": partidos_filtrados})

        # SOLUCIÓN: Imprimimos el título del DÍA antes de crear las tarjetas
        if len(deportes_a_mostrar) > 0:
            st.markdown(f'<div class="dia-titulo">{dia}</div>', unsafe_allow_html=True)
            
            for dep in deportes_a_mostrar:
                with st.container(border=True):
                    st.markdown(f'<div class="tarjeta-header">{dep["deporte"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
                    
                    for p in dep["partidos"]:
                        if "Ajedrez" in dep["deporte"] or "Ciclismo" in dep["deporte"]:
                            # Eventos de 1 día (Lugar / Resultado)
                            st.markdown(f'<div class="partido-fila"><div class="partido-info">{p["hora"]} | {p["eq1"]}</div><div class="partido-marcador" style="color:#d32f2f;">{p["marcador"]}</div></div>', unsafe_allow_html=True)
                        else:
                            # Partidos normales con marcador a la derecha
                            texto_vs = f"{p['eq1']} vs. {p['eq2']}" if p['marcador'] == "Pendiente" else f"{p['eq1']} - {p['eq2']}"
                            marcador_display = "" if p['marcador'] == "Pendiente" else p['marcador']
                            st.markdown(f'<div class="partido-fila"><div class="partido-info">{p["hora"]} | {texto_vs}</div><div class="partido-marcador">{marcador_display}</div></div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                    if st.button("Ver más detalles", key=f"det_{dia}_{dep['deporte']}"):
                        st.session_state.pantalla_actual = "DETALLE"
                        st.session_state.filtro_deporte = dep["deporte"]
                        st.rerun()
                    st.markdown('</div></div>', unsafe_allow_html=True)
                st.write("") 

# --- PANTALLA 2: VISTA DETALLADA ---
elif st.session_state.pantalla_actual == "DETALLE":
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
    
    # Tarjeta Compacta
    with st.container(border=True):
        st.markdown(f'<div class="tarjeta-header">RESUMEN DE PARTIDOS</div>', unsafe_allow_html=True)
        st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
        
        st.markdown('<div class="partido-fila"><div class="partido-info">14:00 | Profesionales - San Sebastián</div><div class="partido-marcador">2 - 1</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="partido-fila"><div class="partido-info">15:00 | Dangers - Cutchil</div><div class="partido-marcador">0 - 3</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="partido-fila"><div class="partido-info" style="color:gray;">16:00 | Estudiantes vs. Atlético</div><div class="partido-marcador" style="color:gray;">Pendiente</div></div>', unsafe_allow_html=True)
        
        # EL BOTÓN QUE ACTIVA EL MODAL OSCURO
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("Ver más partidos", key="abrir_modal"):
            modal_calendario(st.session_state.filtro_deporte) # Llama a la función del modal
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.write("")
    
    # Tabla de Posiciones
    if "Ajedrez" not in st.session_state.filtro_deporte and "Ciclismo" not in st.session_state.filtro_deporte:
        with st.container(border=True):
            st.markdown(f'<div class="tarjeta-header" style="background-color:#e0e0e0; color:#333;">Grupo A</div>', unsafe_allow_html=True)
            st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
            st.markdown('**TEAM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; P &nbsp; GF &nbsp; GC &nbsp; +/-**')
            st.markdown('🛡️ Cutchil &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3 &nbsp;&nbsp; 3 &nbsp;&nbsp; 0 &nbsp;&nbsp; +3')
            st.markdown('🛡️ Profesionales &nbsp;&nbsp;&nbsp;&nbsp; 3 &nbsp;&nbsp; 2 &nbsp;&nbsp; 1 &nbsp;&nbsp; +1')
            st.markdown('</div>', unsafe_allow_html=True)
