import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Clave:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="DERBY V28", layout="wide")

st.markdown("""
    <style>
    /* Estilo para impresión: 2 cuadros por fila */
    @media print {
        .no-print { display: none !important; }
        .print-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }
        .pelea-card-print {
            width: 48%; /* Hace que quepan dos por fila */
            border: 1px solid #000;
            margin-bottom: 10px;
            padding: 10px;
            page-break-inside: avoid;
            color: black !important;
            background: white !important;
        }
        body { background-color: white !important; color: black !important; }
    }
    
    /* Estilo para pantalla (Fichas) */
    .pelea-card {
        background-color: #1e1e1e;
        border: 2px solid #444;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        color: white;
    }
    .rojo-text { color: #ff4b4b; font-weight: bold; }
    .verde-text { color: #00c853; font-weight: bold; }
    .info-box { background: #333; padding: 5px; border-radius: 5px; margin: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "datos_derby.txt"

def cargar_datos():
    partidos = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) == 5:
                    try:
                        partidos.append({"PARTIDO": p[0], "P1": float(p[1]), "P2": float(p[2]), "P3": float(p[3]), "P4": float(p[4])})
                    except ValueError: continue
    return partidos

def guardar_todos(lista):
    with open(DB_FILE, "w") as f:
        for p in lista:
            f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

# --- 3. PESTAÑAS ---
tab1, tab2 = st.tabs(["📝 REGISTRO", "🏆 COTEJO E IMPRESIÓN"])

with tab1:
    st.title("Control de Pesaje")
    partidos = cargar_datos()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Nuevo Partido")
        n = st.text_input("Nombre:").upper()
        p1 = st.number_input("Peso 1", format="%.3f")
        p2 = st.number_input("Peso 2", format="%.3f")
        p3 = st.number_input("Peso 3", format="%.3f")
        p4 = st.number_input("Peso 4", format="%.3f")
        if st.button("💾 GUARDAR", use_container_width=True):
            if n:
                partidos.append({"PARTIDO": n, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
                guardar_todos(partidos); st.rerun()
    with col2:
        st.subheader("Registrados")
        if partidos:
            df = pd.DataFrame(partidos)
            df.index = range(1, len(df)+1)
            st.dataframe(df, use_container_width=True)
            if st.button("🗑️ REINICIAR TODO"):
                if os.path.exists(DB_FILE): os.remove(DB_FILE); st.rerun()

with tab2:
    partidos = cargar_datos()
    if len(partidos) >= 2:
        st.title("📋 Hoja de Cotejo")
        
        # Botón para activar modo impresión
        st.markdown('<div class="no-print">', unsafe_allow_html=True)
        modo_impresion = st.checkbox("📐 Activar modo impresión (2 por fila)")
        st.info("💡 Si activas este modo, presiona Ctrl + P para imprimir.")
        st.markdown('</div>', unsafe_allow_html=True)

        for r in range(1, 5):
            st.header(f"🏁 RONDA {r}")
            col_p = f"P{r}"
            
            # Contenedor que cambia si es para imprimir
            if modo_impresion:
                st.markdown('<div class="print-container">', unsafe_allow_html=True)
            
            for i in range(0, len(partidos) - 1, 2):
                roj, ver = partidos[i], partidos[i+1]
                dif = abs(roj[col_p] - ver[col_p])
                
                clase_card = "pelea-card-print" if modo_impresion else "pelea-card"
                
                st.markdown(f"""
                <div class="{clase_card}">
                    <div style="text-align: center; border-bottom: 1px solid #666; font-weight: bold;">
                        PELEA #{(i//2)+1}
                    </div>
                    <div class="info-box">
                        <span class="rojo-text">🔴 ROJO:</span> {roj['PARTIDO']}<br>
                        P: {roj[col_p]:.3f} | A: {(i+1):03} [ ]
                    </div>
                    <div style="text-align: center; font-size: 10px;">⚡ VS ⚡</div>
                    <div class="info-box">
                        <span class="verde-text">🟢 VERDE:</span> {ver['PARTIDO']}<br>
                        P: {ver[col_p]:.3f} | A: {(i+2):03} [ ]
                    </div>
                    <div style="text-align: right; font-size: 10px;">
                        EMPATE [ ] | DIF: {dif:.3f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if modo_impresion:
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Registre partidos para generar el cotejo.")
