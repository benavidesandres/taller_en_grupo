"""
Frontend - Sistema de Triage y Flujo de Sala de Urgencias
Ejecutar: python -m streamlit run app.py
"""

import time
import streamlit as st
from triage_system import HospitalTriageSystem, TRIAGE_LEVELS


st.set_page_config(
    page_title="Triage - Sala de Urgencias",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

/* Variables de color */
:root {
    --bg-deep:      #130d08;
    --bg-base:      #1a1108;
    --bg-card:      #231608;
    --bg-card2:     #2a1c0d;
    --bg-input:     #1f1509;
    --border:       #4a3018;
    --border-light: #5e3d20;
    --gold:         #c8922a;
    --gold-light:   #e8b84b;
    --gold-pale:    #f5d98a;
    --cream:        #f2e6cc;
    --cream-dim:    #c8b08a;
    --brown-mid:    #9a7040;
    --brown-dim:    #6a4a28;
    --brown-faint:  #3a2810;
    --red-triage:   #d44a3a;
    --orange-triage:#d47a2a;
    --yellow-triage:#c8a830;
    --green-triage: #5a9a4a;
    --blue-triage:  #4a7aaa;
}

/* Reset y base */
html, body, .stApp {
    background-color: var(--bg-deep) !important;
    color: var(--cream) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Textura de fondo sutil */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(200,146,42,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(180,80,30,0.05) 0%, transparent 60%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8922a' fill-opacity='0.015'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0a05 0%, #130d08 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

/* Ocultar elementos de Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* Metricas */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(200,146,42,0.1) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,0,0,0.5), 0 0 0 1px rgba(200,146,42,0.2) !important;
}
[data-testid="metric-container"] label {
    color: var(--brown-mid) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--gold-pale) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 36px !important;
    font-weight: 600 !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] {
    color: var(--gold) !important;
    font-size: 11px !important;
}

/* Titulos */
h1, h2, h3, h4, h5 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    color: var(--gold-light) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--cream) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(200,146,42,0.15), 0 2px 8px rgba(0,0,0,0.3) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--brown-dim) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--cream) !important;
}
.stSelectbox > div > div:hover { border-color: var(--gold) !important; }

/* Labels */
label, .stTextInput label, .stSelectbox label, .stTextArea label, .stNumberInput label {
    color: var(--brown-mid) !important;
    font-size: 11.5px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* Boton normal */
.stButton > button {
    background: linear-gradient(135deg, #5a2e10 0%, #7a3e18 100%) !important;
    color: var(--cream) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 18px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    white-space: pre-line !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7a3e18 0%, #a05020 100%) !important;
    border-color: var(--gold) !important;
    color: var(--gold-pale) !important;
    box-shadow: 0 6px 20px rgba(160,80,30,0.4), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* Boton submit del form */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #8a4a18 0%, #b86020 100%) !important;
    color: #fff8ec !important;
    border: 1px solid var(--gold) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    padding: 12px !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(184,96,32,0.35) !important;
    transition: all 0.2s !important;
}
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #b86020 0%, #d87030 100%) !important;
    box-shadow: 0 8px 24px rgba(200,112,48,0.5) !important;
    transform: translateY(-2px) !important;
}

/* Formulario contenedor */
[data-testid="stForm"] {
    background: linear-gradient(145deg, var(--bg-card) 0%, #1e1208 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(200,146,42,0.08);
}

/* Tarjeta de cama */
.bed-card {
    border-radius: 10px;
    padding: 10px 8px;
    margin: 3px 0;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
    line-height: 1.6;
    transition: transform 0.15s, box-shadow 0.15s;
    cursor: default;
}
.bed-card:hover { transform: translateY(-2px); }
.bed-free {
    background: linear-gradient(135deg, #0f1e0a 0%, #172a0f 100%);
    border: 1px solid #2a4a1a;
    color: #7ab85a;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3), inset 0 1px 0 rgba(100,180,60,0.08);
}
.bed-busy {
    background: linear-gradient(135deg, #1e0e06 0%, #2e1a0a 100%);
    border: 1px solid #6a3018;
    color: #e08050;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3), inset 0 1px 0 rgba(220,120,60,0.08);
}

/* Items de cola de espera */
.queue-item {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
    border-left: 3px solid;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 13px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    transition: transform 0.15s, box-shadow 0.15s;
    animation: slideIn 0.3s ease;
}
.queue-item:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

/* Log de eventos */
.log-item {
    font-family: 'Outfit', monospace;
    font-size: 11.5px;
    padding: 5px 10px;
    border-radius: 6px;
    margin: 3px 0;
    background: rgba(20,12,4,0.8);
    border: 1px solid rgba(74,48,24,0.4);
    color: var(--cream-dim);
    transition: background 0.15s;
}
.log-item:hover { background: rgba(35,22,8,0.9); }

/* Badges de estructuras */
.struct-badge {
    background: linear-gradient(135deg, #2a1a08 0%, #3a2410 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 13px;
    font-size: 11px;
    color: var(--gold);
    margin: 3px;
    display: inline-block;
    letter-spacing: 0.5px;
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

/* Pila items */
.stack-item {
    border-radius: 8px;
    padding: 7px 12px;
    margin: 4px 0;
    font-size: 12px;
    color: var(--gold-pale);
    border-left: 3px solid;
    transition: all 0.15s;
}
.stack-item:hover { transform: translateX(2px); }

/* Alta item */
.alta-item {
    border-radius: 8px;
    padding: 8px 12px;
    margin: 5px 0;
    font-size: 12px;
    border-left: 3px solid;
    transition: all 0.15s;
}
.alta-item:hover { transform: translateX(2px); }

/* Animaciones */
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-8px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-up { animation: fadeUp 0.4s ease; }

/* Dividers */
hr, [data-testid="stDivider"] hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
    margin: 14px 0 !important;
}

/* Captions */
.stCaption p, small {
    color: var(--brown-dim) !important;
    font-size: 11px !important;
    letter-spacing: 0.3px;
}

/* Info / success / warning / error */
.stAlert {
    border-radius: 10px !important;
    font-size: 13px !important;
    border: 1px solid !important;
}
div[data-baseweb="notification"] {
    background: var(--bg-card2) !important;
    border-radius: 10px !important;
}

/* Sidebar triage cards */
.triage-card {
    border-radius: 10px;
    padding: 10px 14px;
    margin: 7px 0;
    border-left: 4px solid;
    transition: transform 0.15s, box-shadow 0.15s;
    background: linear-gradient(135deg, #0e0a05 0%, #1a1008 100%);
}
.triage-card:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
}

/* Seccion card wrapper */
.section-card {
    background: linear-gradient(145deg, var(--bg-card) 0%, #1e1208 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35), inset 0 1px 0 rgba(200,146,42,0.06);
}

/* Numeros de numero input */
.stNumberInput button {
    background: var(--bg-card2) !important;
    border-color: var(--border) !important;
    color: var(--gold) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* Multiselect dropdown items */
li[role="option"] {
    background: var(--bg-card2) !important;
    color: var(--cream) !important;
}
</style>
""", unsafe_allow_html=True)


# Estado de sesion
if "system" not in st.session_state:
    st.session_state.system = HospitalTriageSystem()
    st.session_state.msg = None

sys = st.session_state.system


# Header con linea decorativa y subtitulo
st.markdown("""
<div style='text-align:center; padding: 10px 0 18px 0; animation: fadeUp 0.6s ease;'>
    <div style='font-family: Outfit, sans-serif; font-size:11px; font-weight:600;
                letter-spacing:4px; color:#6a4a28; text-transform:uppercase;
                margin-bottom:8px;'>
        Hospital Central &bull; Sistema Digital
    </div>
    <h1 style='font-family: Cormorant Garamond, serif; color:#e8b84b;
               font-size:38px; font-weight:700; margin:0; letter-spacing:3px;
               text-shadow: 0 2px 20px rgba(232,184,75,0.25);'>
        Sala de Urgencias
    </h1>
    <div style='font-family: Cormorant Garamond, serif; font-size:16px;
                color:#9a7040; letter-spacing:2px; margin-top:4px;'>
        Sistema de Triage y Gestion de Flujo
    </div>
    <div style='margin-top:12px; line-height:2;'>
        <span class='struct-badge'>Array &rarr; Camas</span>
        <span class='struct-badge'>Pila &rarr; Historial</span>
        <span class='struct-badge'>Cola &rarr; Espera</span>
        <span class='struct-badge'>Lista Enlazada &rarr; Log</span>
        <span class='struct-badge'>Lista &rarr; Altas</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Metricas
stats = sys.get_stats()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Camas Totales",  stats["total_beds"])
c2.metric("Ocupadas",       stats["occupied_beds"])
c3.metric("Disponibles",    stats["free_beds"])
c4.metric("En Espera",      stats["waiting"],
          delta=f"+{stats['waiting']}" if stats["waiting"] else None)
c5.metric("Dados de Alta",  stats["discharged"])

st.divider()

# Retroalimentacion
if st.session_state.msg:
    kind, text = st.session_state.msg
    if kind == "success":   st.success(text)
    elif kind == "error":   st.error(text)
    elif kind == "warning": st.warning(text)
    elif kind == "info":    st.info(text)
    st.session_state.msg = None


# Layout 3 columnas
left, mid, right = st.columns([1.05, 1.45, 1])


# ── Columna izquierda ──────────────────────────────────────────
with left:

    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:2px; letter-spacing:1px;'>
        Registro de Paciente
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:12px;'>
        Cola de Prioridad &mdash; enqueue()
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=True):
        name     = st.text_input("Nombre completo", placeholder="Ej: Ana Garcia")
        age      = st.number_input("Edad", min_value=0, max_value=130, value=35)
        symptoms = st.text_area("Sintomas principales", placeholder="Describa los sintomas...", height=75)
        priority = st.selectbox(
            "Nivel de triage",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: f"Nivel {x}  -  {TRIAGE_LEVELS[x]['name']} ({TRIAGE_LEVELS[x]['label']})"
        )
        submitted = st.form_submit_button("Registrar en Cola", use_container_width=True)

    if submitted:
        if not name.strip():
            st.session_state.msg = ("error", "Ingrese el nombre del paciente.")
        elif not symptoms.strip():
            st.session_state.msg = ("error", "Ingrese los sintomas.")
        else:
            p = sys.register_patient(name.strip(), age, symptoms.strip(), priority)
            st.session_state.msg = (
                "success",
                f"{p['name']} registrado  |  ID: {p['id']}  |  {TRIAGE_LEVELS[priority]['name']}"
            )
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:10px; letter-spacing:1px;'>
        Acciones Rapidas
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Asignar\nCama", use_container_width=True):
            result = sys.assign_bed()
            if result:
                st.session_state.msg = ("success", f"Cama {result['bed']+1} asignada a {result['name']}")
            elif sys.waiting_queue.is_empty():
                st.session_state.msg = ("warning", "No hay pacientes en espera.")
            else:
                st.session_state.msg = ("error", "No hay camas disponibles.")
            st.rerun()

    with col_b:
        if st.button("Deshacer\nAccion", use_container_width=True):
            msg = sys.undo_last_action()
            st.session_state.msg = ("info", msg)
            st.rerun()

    # Nota de estructuras
    st.markdown("""
    <div style='margin-top:14px; background:linear-gradient(135deg,#1a1008,#231808);
                border:1px solid #3a2810; border-radius:10px; padding:12px 14px;'>
        <div style='font-size:10px; color:#6a4a28; letter-spacing:1px; margin-bottom:6px;
                    font-weight:600; text-transform:uppercase;'>Operaciones activas</div>
        <div style='font-size:11.5px; color:#9a7040; line-height:1.9;'>
            <span style='color:#c87030;'>enqueue()</span> &rarr; inserta en cola<br>
            <span style='color:#c87030;'>dequeue()</span> &rarr; saca de la cola<br>
            <span style='color:#c87030;'>push() / pop()</span> &rarr; pila historial<br>
            <span style='color:#c87030;'>Array.set()</span> &rarr; asigna cama
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Columna central ────────────────────────────────────────────
with mid:

    # Mapa de camas
    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:2px; letter-spacing:1px;'>
        Mapa de Camas
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:10px;'>
        Array fijo de 10 elementos &mdash; get() / set() O(1)
    </div>
    """, unsafe_allow_html=True)

    bed_status = sys.get_bed_status()
    rows = [bed_status[i:i+5] for i in range(0, 10, 5)]

    for row in rows:
        cols = st.columns(5)
        for col, bed in zip(cols, row):
            with col:
                if bed["status"] == "Libre":
                    st.markdown(
                        f"<div class='bed-card bed-free'>"
                        f"<div style='font-size:16px;'>+</div>"
                        f"<div style='font-size:11px;font-weight:700;'>C{bed['bed']}</div>"
                        f"<div style='font-size:9px;color:#4a8030;letter-spacing:1px;'>LIBRE</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                else:
                    p = bed["patient"]
                    tc = p["triage"]["color"]
                    tn = p["triage"]["name"][:3]
                    st.markdown(
                        f"<div class='bed-card bed-busy' style='border-color:{tc}44;'>"
                        f"<div style='font-size:10px;font-weight:800;color:{tc};'>{tn}</div>"
                        f"<div style='font-size:11px;font-weight:700;'>C{bed['bed']}</div>"
                        f"<div style='font-size:9px;color:#8a5030;'>{p['name'][:8]}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Alta medica
    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:18px;
                color:#c8a840; font-weight:600; margin:10px 0 4px; letter-spacing:1px;'>
        Alta Medica
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:8px;'>
        Array.set(slot, None) &rarr; DischargeList.add(paciente)
    </div>
    """, unsafe_allow_html=True)

    occupied = [(i, sys.active_patients[i]) for i in sys.active_patients]
    if occupied:
        options = {f"C{i+1}  -  {p['name']}  ({p['id']})": i for i, p in occupied}
        selected = st.selectbox("Cama a liberar", list(options.keys()), key="discharge_sel")
        notes = st.text_input("Notas medicas", placeholder="Diagnostico / instrucciones al paciente", key="discharge_notes")
        if st.button("Confirmar Alta", use_container_width=True):
            idx = options[selected]
            patient = sys.discharge_patient(idx, notes)
            if patient:
                st.session_state.msg = ("success", f"{patient['name']} dado de alta desde C{idx+1}")
            else:
                st.session_state.msg = ("error", "Error al dar de alta.")
            st.rerun()
    else:
        st.markdown(
            "<div style='background:#0e1a0a;border:1px solid #2a4018;border-radius:8px;"
            "padding:10px 14px;font-size:12px;color:#4a8030;text-align:center;'>"
            "No hay pacientes en cama actualmente"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # Cola de espera
    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:2px; letter-spacing:1px;'>
        Cola de Espera
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:10px;'>
        Cola de Prioridad &mdash; FIFO por nivel de triage
    </div>
    """, unsafe_allow_html=True)

    queue = sys.waiting_queue.to_list()
    if not queue:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#0f1e0a,#162810);"
            "border:1px solid #2a4018;border-radius:10px;padding:14px;"
            "color:#5a8840;font-size:13px;text-align:center;"
            "font-family:Cormorant Garamond,serif;font-weight:500;letter-spacing:1px;'>"
            "Cola vacia &mdash; no hay pacientes en espera"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        for i, p in enumerate(queue):
            color = p["triage"]["color"]
            wait_s = int(time.time() - p["timestamp"])
            mins, secs = wait_s // 60, wait_s % 60
            wait_str = f"{mins}m {secs}s"
            level_name = p["triage"]["name"]
            st.markdown(
                f"<div class='queue-item' style='border-left-color:{color};'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<span style='color:{color};font-weight:700;font-size:13px;'>"
                f"#{i+1} &nbsp; {p['name']}</span>"
                f"<span style='background:{color}22;color:{color};font-size:10px;"
                f"font-weight:700;padding:2px 8px;border-radius:12px;letter-spacing:1px;'>"
                f"{level_name}</span>"
                f"</div>"
                f"<div style='color:#7a5a38;font-size:11px;margin-top:3px;'>"
                f"{p['id']} &bull; {p['age']} anios &bull; Espera: {wait_str}"
                f"</div>"
                f"<div style='color:#8a6a48;font-size:11.5px;margin-top:3px;"
                f"font-style:italic;'>{p['symptoms'][:60]}...</div>"
                f"</div>",
                unsafe_allow_html=True
            )


# ── Columna derecha ────────────────────────────────────────────
with right:

    # Log de eventos
    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:2px; letter-spacing:1px;'>
        Log de Eventos
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:10px;'>
        Lista Enlazada Simple &mdash; prepend O(1)
    </div>
    """, unsafe_allow_html=True)

    event_colors = {
        "REGISTRO":   "#c87030",
        "ASIGNACION": "#c8a030",
        "ALTA":       "#5a9840",
        "DESHACER":   "#b04838",
    }

    events = sys.event_log.to_list()
    if not events:
        st.markdown(
            "<div style='color:#4a3018;font-size:12px;text-align:center;"
            "padding:10px;font-style:italic;'>Sin eventos registrados</div>",
            unsafe_allow_html=True
        )
    else:
        for ev in events[:14]:
            c = event_colors.get(ev["type"], "#6a4a28")
            st.markdown(
                f"<div class='log-item'>"
                f"<span style='color:{c};font-weight:700;font-size:10px;"
                f"letter-spacing:1px;'>{ev['type']}</span>"
                f"<span style='color:#4a3018;'> &bull; </span>"
                f"<span style='color:#6a4a28;font-size:10px;'>{ev['time']}</span>"
                f"<span style='color:#4a3018;'> &bull; </span>"
                f"<span style='color:#9a7a50;font-size:11px;'>{ev['patient_id']}</span>"
                f"<br><span style='color:#7a5a38;font-size:11px;'>{ev['description']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        if len(events) > 14:
            st.caption(f"... y {len(events)-14} eventos mas en la lista enlazada.")

    st.divider()

    # Altas
    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:2px; letter-spacing:1px;'>
        Historial de Altas
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:8px;'>
        Lista Python &mdash; append / index O(1)
    </div>
    """, unsafe_allow_html=True)

    alta_list = sys.discharged.all()
    if not alta_list:
        st.markdown(
            "<div style='color:#4a3018;font-size:12px;text-align:center;"
            "padding:10px;font-style:italic;'>Sin altas registradas</div>",
            unsafe_allow_html=True
        )
    else:
        for p in reversed(alta_list[-7:]):
            color = p["triage"]["color"]
            stay  = p.get("stay_minutes", "-")
            st.markdown(
                f"<div class='alta-item' style='background:linear-gradient(135deg,#1a1208,#221a0a);"
                f"border-left-color:{color};box-shadow:0 2px 8px rgba(0,0,0,0.3);'>"
                f"<div style='display:flex;justify-content:space-between;'>"
                f"<span style='color:{color};font-weight:600;font-size:12.5px;'>{p['name']}</span>"
                f"<span style='color:#5a3a18;font-size:10px;'>{p['id']}</span>"
                f"</div>"
                f"<div style='color:#7a5a38;font-size:10.5px;margin-top:2px;'>"
                f"Alta: {p.get('discharged_at','?')} &bull; Estancia: {stay} min"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.divider()

    # Pila
    st.markdown("""
    <div style='font-family: Cormorant Garamond, serif; font-size:20px;
                color:#e8b84b; font-weight:600; margin-bottom:2px; letter-spacing:1px;'>
        Pila de Acciones
    </div>
    <div style='font-size:10.5px; color:#6a4a28; letter-spacing:1px; margin-bottom:8px;'>
        Stack LIFO &mdash; tope = ultima accion
    </div>
    """, unsafe_allow_html=True)

    stack_items = sys.action_history.to_list()
    if not stack_items:
        st.markdown(
            "<div style='color:#4a3018;font-size:12px;text-align:center;"
            "padding:10px;font-style:italic;'>Pila vacia</div>",
            unsafe_allow_html=True
        )
    else:
        action_labels = {
            "register":   "Registro",
            "assign_bed": "Asignacion cama",
            "discharge":  "Alta medica",
        }
        for i, item in enumerate(stack_items[:6]):
            is_top = i == 0
            border_c = "#c87030" if is_top else "#3a2810"
            bg = "linear-gradient(135deg,#2a1808,#1a1008)" if is_top else "linear-gradient(135deg,#1a1008,#120e06)"
            label = "TOPE" if is_top else f"[{i+1}]"
            label_c = "#c87030" if is_top else "#4a3018"
            aname = action_labels.get(item["action"], item["action"])
            st.markdown(
                f"<div class='stack-item' style='background:{bg};border-left-color:{border_c};'>"
                f"<span style='color:{label_c};font-size:9px;font-weight:700;"
                f"letter-spacing:1.5px;'>{label}</span>"
                f"  <span style='color:#c4a070;font-weight:600;'>{aname}</span>"
                f"  <span style='color:#5a3a18;font-size:11px;'>{item['patient_id']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        if len(stack_items) > 6:
            st.caption(f"+{len(stack_items)-6} acciones mas.")


# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 16px;'>
        <div style='font-family:Cormorant Garamond,serif; font-size:22px;
                    color:#e8b84b; font-weight:600; letter-spacing:2px;'>
            Escala de Triage
        </div>
        <div style='font-size:10px; color:#5a3a18; letter-spacing:2px; margin-top:2px;'>
            SISTEMA MANCHESTER
        </div>
    </div>
    """, unsafe_allow_html=True)

    for lvl, info in TRIAGE_LEVELS.items():
        st.markdown(
            f"<div class='triage-card' style='border-left-color:{info['color']};'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
            f"<span style='color:{info['color']};font-weight:700;font-size:13px;"
            f"font-family:Outfit,sans-serif;letter-spacing:1px;'>"
            f"NIV {lvl} &mdash; {info['name']}</span>"
            f"<span style='background:{info['color']}22;color:{info['color']};"
            f"font-size:9px;padding:2px 7px;border-radius:10px;font-weight:700;'>"
            f"{info['max_wait_min']}m</span>"
            f"</div>"
            f"<div style='color:#9a7a50;font-size:11.5px;margin-top:3px;'>"
            f"{info['label']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("""
    <div style='font-family:Cormorant Garamond,serif; font-size:20px;
                color:#e8b84b; font-weight:600; letter-spacing:1px; margin-bottom:10px;'>
        Estructuras Usadas
    </div>
    """, unsafe_allow_html=True)

    structs = [
        ("Array",           "Camas - slots fijos",     "#c87030", "get/set O(1)"),
        ("Pila (Stack)",    "Historial y deshacer",    "#c8a030", "push/pop O(1)"),
        ("Cola (Queue)",    "Pacientes en espera",     "#5a9840", "enqueue O(n log n)"),
        ("Lista Enlazada",  "Log de eventos",          "#4a7aaa", "prepend O(1)"),
        ("Lista (list)",    "Pacientes dados de alta", "#c07888", "append O(1)"),
    ]
    for sname, sdesc, scolor, scomplexity in structs:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#100c06,#1a1208);"
            f"border-left:3px solid {scolor};border-radius:8px;"
            f"padding:8px 12px;margin:5px 0;'>"
            f"<div style='color:{scolor};font-weight:700;font-size:12.5px;"
            f"font-family:Outfit,sans-serif;'>{sname}</div>"
            f"<div style='color:#7a5a38;font-size:11px;'>{sdesc}</div>"
            f"<div style='color:#4a3018;font-size:10px;font-family:monospace;"
            f"margin-top:2px;'>{scomplexity}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown(
        "<div style='text-align:center;color:#4a3018;font-size:10.5px;"
        "line-height:1.8;letter-spacing:0.5px;'>"
        "Taller &bull; Grupo max. 3 personas<br>"
        "Frontend: Streamlit &bull; Backend: Python"
        "</div>",
        unsafe_allow_html=True
    )