import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Clave del Palenque:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="DERBY V28", layout="wide")

st.markdown("""
    <style>
    .rojo { color: #ff4b4b; font-weight: bold; }
    .verde { color: #00c853; font-weight: bold; }
    @media print {
        .no-print { display: none !important; }
        .stMarkdown, .stTable { width: 100% !important; }
    }
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
                    partidos.append({"PARTIDO": p[0], "P1": float(p[1]), "P2": float(p[2]), "P3": float(p[3]), "P4": float(p[4])})
    return partidos

def guardar_todos(lista):
    with open(DB_FILE, "w") as f:
        for p in lista:
            f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

# --- 3. REGISTRO (Oculto en Impresión) ---
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.title("🏆 Derby V28 - Registro")
with st.expander("➕ REGISTRAR PARTIDO", expanded=False):
    nombre = st.text_input("Nombre del Partido:").upper()
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("Peso 1", value=0.0, format="%.3f")
        p2 = st.number_input("Peso 2", value=0.0, format="%.3f")
    with c2:
        p3 = st.number_input("Peso 3", value=0.0, format="%.3f")
        p4 = st.number_input("Peso 4", value=0.0, format="%.3f")
    if st.button("✅ GUARDAR REGISTRO", use_container_width=True):
        if nombre:
            d = cargar_datos(); d.append({"PARTIDO": nombre, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
            guardar_todos(d); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. REPORTE PARA IMPRESIÓN (IDÉNTICO A LA FOTO) ---
partidos = cargar_datos()
if len(partidos) >= 2:
    st.markdown("## 📋 HOJA DE COTEJO OFICIAL")
    st.write("Fecha: 13/01/2026")
    
    for r in range(1, 5):
        st.markdown(f"### RONDA {r}")
        col_p = f"P{r}"
        
        datos_impresion = []
        for i in range(0, len(partidos) - 1, 2):
            rojo = partidos[i]
            verde = partidos[i+1]
            dif = abs(rojo[col_p] - verde[col_p])
            
            # Formato idéntico a la foto
            datos_impresion.append({
                "N°": (i//2) + 1,
                "GAN (R)": "__",
                "PARTIDO (ROJO)": rojo['PARTIDO'],
                "PESO (R)": f"{rojo[col_p]:.3f}",
                "ANILLO (R)": f"{(i+1):03}",
                "EMPATE": "__",
                "ANILLO (V)": f"{(i+2):03}",
                "PESO (V)": f"{verde[col_p]:.3f}",
                "PARTIDO (VERDE)": verde['PARTIDO'],
                "GAN (V)": "__",
                "DIF KG": f"{dif:.3f}"
            })
        
        st.table(pd.DataFrame(datos_impresion))
    
    st.markdown('<div class="no-print">', unsafe_allow_html=True)
    if st.button("🗑️ BORRAR TODO", type="secondary"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
