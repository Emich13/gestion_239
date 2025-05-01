import streamlit as st
import pandas as pd
from database import init_db, agregar_usuario, obtener_usuarios, agregar_movimiento, obtener_movimientos, eliminar_movimiento
from datetime import date
import json

# Inicializar base de datos
init_db()

st.title("💸 Gestión 239")

# Tabs principales
tab1, tab2, tab3 = st.tabs(["Registrar movimiento", "Ver movimientos", "Gestionar usuarios"])

# --- TAB 1: Registrar movimiento ---
with tab1:
    st.header("Registrar gasto o ingreso")

    tipo = st.selectbox("Tipo", ["gasto", "ingreso"])
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto", min_value=0.0, format="%.2f")
    fecha = st.date_input("Fecha", value=date.today())

    usuarios = obtener_usuarios()
    if usuarios:
        opciones = {nombre: id for id, nombre in usuarios}
        id_usuario = st.selectbox("¿Quién paga o gana?", opciones.keys())
        participantes = st.multiselect("¿Quiénes participan?", opciones.keys(), default=[id_usuario])

        if st.button("Guardar movimiento"):
            agregar_movimiento(
                tipo,
                descripcion,
                monto,
                fecha.isoformat(),
                opciones[id_usuario],
                [opciones[p] for p in participantes]
            )
            st.success("✅ Movimiento registrado correctamente")
    else:
        st.warning("Primero debes agregar usuarios en la pestaña 'Gestionar usuarios'")

# --- TAB 2: Ver movimientos ---
with tab2:
    st.header("Movimientos registrados")

    movimientos = obtener_movimientos()
    if movimientos:
        df = pd.DataFrame(movimientos, columns=["ID", "Tipo", "Descripción", "Monto", "Fecha", "ID Usuario", "Participantes"])
        df["Participantes"] = df["Participantes"].apply(lambda x: ", ".join(map(str, json.loads(x))) if x else "")
        st.dataframe(df)

        id_borrar = st.number_input("ID de movimiento a eliminar", min_value=1, step=1)
        if st.button("Eliminar movimiento"):
            eliminar_movimiento(id_borrar)
            st.success("✅ Movimiento eliminado")
    else:
        st.info("Todavía no hay movimientos registrados.")

# --- TAB 3: Gestionar usuarios ---
with tab3:
    st.header("Usuarios")

    usuarios = obtener_usuarios()
    if usuarios:
        st.table(pd.DataFrame(usuarios, columns=["ID", "Nombre"]))

    nuevo_usuario = st.text_input("Agregar nuevo usuario")
    if st.button("Agregar usuario"):
        agregar_usuario(nuevo_usuario)
        st.success(f"✅ Usuario '{nuevo_usuario}' agregado")
