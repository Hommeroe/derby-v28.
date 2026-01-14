import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado - Derby V28")
    password = st.text_input("Ingresa la clave del Palenque:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop()

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="SISTEMA DERBY V28", layout="centered")
DB_FILE = "datos_derby.txt"

def cargar_datos():
    partidos = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 5:
                    partidos.append({
                        "PARTIDO": partes[0],
                        "P1": float(partes[1]), "P2": float(partes[2]),
                        "P3": float(partes[3]), "P4": float(partes[4])
                    })
    return partidos

def guardar_todos(lista_partidos):
    with open(DB_FILE, "w") as f:
        for p in lista_partidos:
            f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

# --- 3. INTERFAZ DE REGISTRO ---
st.title("🏆 Registro de Pesos")

with st.expander("➕ REGISTRAR NUEVO PARTIDO", expanded=True):
    nombre = st.text_input("Nombre del Partido:", key="n_input").upper()
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("Peso 1", value=0.0, format="%.3f", step=0.001, key="p1_i")
        p2 = st.number_input("Peso 2", value=0.0, format="%.3f", step=0.001, key="p2_i")
    with c2:
        p3 = st.number_input("Peso 3", value=0.0, format="%.3f", step=0.001, key="p3_i")
        p4 = st.number_input("Peso 4", value=0.0, format="%.3f", step=0.001, key="p4_i")
    
    if st.button("✅ GUARDAR Y LIMPIAR", use_container_width=True):
        if nombre:
            partidos_actuales = cargar_datos()
            partidos_actuales.append({"PARTIDO": nombre, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
            guardar_todos(partidos_actuales)
            st.success("¡Guardado!")
            st.rerun()

# --- 4. GENERACIÓN DE COTEJO ESTILO PROFESIONAL ---
partidos = cargar_datos()
if len(partidos) >= 2:
    st.divider()
    st.subheader("📋 Hoja de Cotejo Oficial")
    
    # Creamos las rondas
    for ronda in range(1, 5):
        st.markdown(f"### 🥊 RONDA {ronda}")
        col_peso = f"P{ronda}"
        
        # Lógica de emparejamiento simple (1 vs 2, 3 vs 4...)
        filas_ronda = []
        for i in range(0, len(partidos) - 1, 2):
            p_rojo = partidos[i]
            p_verde = partidos[i+1]
            diff = abs(p_rojo[col_peso] - p_verde[col_peso])
            
            filas_ronda.append({
                "Cotejo": (i//2) + 1,
                "ROJO": p_rojo['PARTIDO'],
                "Peso R": f"{p_rojo[col_peso]:.3f}",
                "VS": "⚔️",
                "Peso V": f"{p_verde[col_peso]:.3f}",
                "VERDE": p_verde['PARTIDO'],
                "Dif (kg)": f"{diff:.3f}"
            })
        
        df_ronda = pd.DataFrame(filas_ronda)
        st.table(df_ronda)

    # BOTÓN PARA IMPRIMIR
    if st.button("🖨️ PREPARAR IMPRESIÓN (PDF)", use_container_width=True):
        st.info("Usa la función de 'Imprimir' de tu navegador (Ctrl+P) para guardar como PDF.")
