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
        else:
            st.error("Falta el nombre")

# --- 4. HOJA DE COTEJO PROFESIONAL ---
partidos = cargar_datos()
if len(partidos) >= 2:
    st.divider()
    st.subheader("📋 Hoja de Cotejo Oficial")
    st.write("Presiona *Ctrl + P* para imprimir este reporte.")

    # Generamos las Rondas (P1 es Ronda 1, P2 es Ronda 2, etc.)
    for r in range(1, 5):
        st.markdown(f"### 🏁 RONDA {r}")
        col_peso = f"P{r}"
        
        # Lista para guardar los enfrentamientos de la ronda
        enfrentamientos = []
        # Emparejamos 0 con 1, 2 con 3, etc.
        for i in range(0, len(partidos) - 1, 2):
            rojo = partidos[i]
            verde = partidos[i+1]
            dif = abs(rojo[col_peso] - verde[col_peso])
            
            enfrentamientos.append({
                "Cotejo": (i // 2) + 1,
                "ROJO (Partido)": rojo['PARTIDO'],
                "Peso (R)": f"{rojo[col_peso]:.3f}",
                "Anillo (R)": "_____",
                "vs": "⚔️",
                "Anillo (V)": "_____",
                "Peso (V)": f"{verde[col_peso]:.3f}",
                "VERDE (Partido)": verde['PARTIDO'],
                "Dif (kg)": f"{dif:.3f}"
            })
        
        if enfrentamientos:
            df_ronda = pd.DataFrame(enfrentamientos)
            st.table(df_ronda)
        else:
            st.info(f"No hay suficientes partidos para completar la Ronda {r}")

    # Opción para borrar
    st.divider()
    if st.button("🗑️ BORRAR TODO EL DERBY", type="secondary", use_container_width=True):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
