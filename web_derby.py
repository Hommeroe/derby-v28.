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
st.set_page_config(page_title="DERBY V28", layout="wide") # Layout wide para horizontal completo

# Estilos CSS
st.markdown("""
    <style>
    @media print { .no-print { display: none !important; } }
    .stTable { width: 100% !important; }
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

# --- 3. CREACIÓN DE PANTALLAS (TABS) ---
tab1, tab2 = st.tabs(["📝 REGISTRO Y DATOS", "🏆 HOJA DE COTEJO FINAL"])

with tab1:
    st.title("Control de Pesaje")
    col_reg, col_lista = st.columns([1, 1])
    
    with col_reg:
        st.subheader("Captura")
        nombre = st.text_input("Nombre del Partido:").upper()
        c1, c2 = st.columns(2)
        with c1:
            p1 = st.number_input("Peso 1", value=0.0, format="%.3f")
            p2 = st.number_input("Peso 2", value=0.0, format="%.3f")
        with c2:
            p3 = st.number_input("Peso 3", value=0.0, format="%.3f")
            p4 = st.number_input("Peso 4", value=0.0, format="%.3f")
        
        if st.button("💾 GUARDAR", use_container_width=True):
            if nombre:
                d = cargar_datos(); d.append({"PARTIDO": nombre, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
                guardar_todos(d); st.rerun()

    with col_lista:
        st.subheader("Registrados")
        partidos = cargar_datos()
        if partidos:
            st.dataframe(pd.DataFrame(partidos), use_container_width=True, height=250)
            if st.button("🗑️ REINICIAR TODO"):
                if os.path.exists(DB_FILE): os.remove(DB_FILE); st.rerun()

with tab2:
    partidos = cargar_datos()
    if len(partidos) >= 2:
        st.markdown("<h1 style='text-align: center;'>📋 HOJA DE COTEJO OFICIAL</h1>", unsafe_allow_html=True)
        st.write("---")
        
        for r in range(1, 5):
            st.markdown(f"## 🏁 RONDA {r}")
            col_p = f"P{r}"
            filas = []
            for i in range(0, len(partidos) - 1, 2):
                rojo = partidos[i]; verde = partidos[i+1]
                dif = abs(rojo[col_p] - verde[col_p])
                filas.append({
                    "PELEA": (i//2) + 1,
                    "GAN (R)": "[  ]",
                    "PARTIDO (ROJO)": rojo['PARTIDO'],
                    "PESO (R)": f"{rojo[col_p]:.3f}",
                    "ANILLO (R)": f"{(i+1):03}",
                    "EMPATE": "[  ]",
                    "ANILLO (V)": f"{(i+2):03}",
                    "PESO (V)": f"{verde[col_p]:.3f}",
                    "PARTIDO (VERDE)": verde['PARTIDO'],
                    "GAN (V)": "[  ]",
                    "DIF KG": f"{dif:.3f}"
                })
            st.table(pd.DataFrame(filas))
            st.write(" ")
    else:
        st.info("La hoja de cotejo aparecerá aquí cuando tengas al menos 2 partidos registrados.")
