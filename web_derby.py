import streamlit as st
import pandas as pd
import random
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

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SISTEMA DERBY V28", layout="centered") # 'centered' ayuda a que se vea mejor en celular

# Archivo donde se guardan los datos
DB_FILE = "datos_derby.txt"

def cargar_datos():
    partidos = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 5:
                    nombre, p1, p2, p3, p4 = partes
                    partidos.append({
                        "PARTIDO": nombre,
                        "P1": float(p1), "P2": float(p2),
                        "P3": float(p3), "P4": float(p4)
                    })
    return partidos

def guardar_partido(nombre, p1, p2, p3, p4):
    with open(DB_FILE, "a") as f:
        f.write(f"{nombre}|{p1}|{p2}|{p3}|{p4}\n")

# --- 3. INTERFAZ DE USUARIO ---
st.title("🏆 Registro de Pesos")

# Formulario para celular
with st.expander("➕ REGISTRAR NUEVO PARTIDO", expanded=True):
    nombre = st.text_input("Nombre del Partido:").upper()
    
    # Aquí es donde usamos las columnas de forma simple
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("Peso 1", value=0.0, format="%.3f", step=0.001)
        p2 = st.number_input("Peso 2", value=0.0, format="%.3f", step=0.001)
    with c2:
        p3 = st.number_input("Peso 3", value=0.0, format="%.3f", step=0.001)
        p4 = st.number_input("Peso 4", value=0.0, format="%.3f", step=0.001)
    
    # Botón ancho para el dedo
    if st.button("✅ GUARDAR REGISTRO", use_container_width=True):
        if nombre:
            guardar_partido(nombre, p1, p2, p3, p4)
            st.success("¡Guardado correctamente!")
            st.rerun()
        else:
            st.error("Falta el nombre")

# --- 4. LISTA Y COTEJO ---
partidos = cargar_datos()

if partidos:
    st.divider()
    st.subheader("📊 Partidos Registrados")
    df = pd.DataFrame(partidos)
    st.dataframe(df, use_container_width=True)

    if st.button("🗑️ BORRAR TODO EL DERBY", type="secondary"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()

    st.divider()
    st.subheader("⚔️ Sugerencia de Cotejo")
    if len(partidos) >= 2:
        # Lógica simple de cotejo para visualización rápida
        df_cotejo = df.copy()
        st.table(df_cotejo)
        
        # Botón para descargar reporte
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DESCARGAR REPORTE PARA IMPRIMIR", csv, "cotejo_derby.csv", "text/csv", use_container_width=True
