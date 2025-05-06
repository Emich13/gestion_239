import streamlit as st
import pandas as pd
from datetime import date
import json

from database import (
    agregar_usuario,
    obtener_usuarios,
    agregar_movimiento,
    obtener_movimientos,
    eliminar_movimiento,
    editar_descripcion_movimiento,
    editar_monto_movimiento,
    editar_fecha_movimiento,
    eliminar_usuario,
    editar_usuario
)

st.set_page_config(page_title="Gestión 239", page_icon="💸", layout="centered")
st.title("💸 Gestión 239")

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs([
    "Registrar movimiento",
    "Ver movimientos",
    "Gestionar usuarios",
    "Resumen mensual"
])

# --- TAB 1: Registrar movimiento ---
with tab1:
    st.header("Registrar gasto o ingreso")

    tipo = st.selectbox("Tipo", ["gasto", "ingreso"])
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto", min_value=0.0, format="%.2f")
    fecha = st.date_input("Fecha", value=date.today(), key="fecha_registro")

    usuarios = obtener_usuarios()
    if usuarios:
        opciones = {nombre: id for id, nombre in usuarios}
        id_usuario = st.selectbox("¿Quién paga o gana?", opciones.keys())
        participantes = st.multiselect("¿Quiénes participan?", opciones.keys(), default=list(opciones.keys()))

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
        df = pd.DataFrame(movimientos, columns=[
            "ID", "Tipo", "Descripción", "Monto", "Fecha", "ID Usuario", "Participantes"])
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)
        df["Participantes"] = df["Participantes"].apply(
            lambda x: ", ".join(map(str, json.loads(x))) if x else "")
        usuarios_dict = dict(obtener_usuarios())
        df["Nombre Usuario"] = df["ID Usuario"].map(usuarios_dict)
        df = df.drop(columns=["ID Usuario"])

        # Filtro por mes
        meses_disponibles = df["Mes"].sort_values().unique().tolist()
        mes_filtrado = st.selectbox("Filtrar por mes", ["Todos"] + meses_disponibles, key="mes_filtrado")
        if mes_filtrado != "Todos":
            df = df[df["Mes"] == mes_filtrado]

        st.dataframe(df.drop(columns=["Mes", "Participantes"]))

        st.subheader("Eliminar movimiento")
        id_borrar = st.number_input("ID de movimiento a eliminar", min_value=1, step=1, key="id_eliminar")
        if st.button("Eliminar movimiento"):
            eliminar_movimiento(id_borrar)
            st.success("✅ Movimiento eliminado")

        st.subheader("Editar descripción")
        id_desc = st.number_input("ID de movimiento a editar", min_value=1, step=1, key="id_editar_desc")
        nueva_desc = st.text_input("Nueva descripción")
        if st.button("Actualizar descripción"):
            editar_descripcion_movimiento(id_desc, nueva_desc)
            st.success("✅ Descripción actualizada")

        st.subheader("Editar monto")
        id_monto = st.number_input("ID de monto a editar", min_value=1, step=1, key="id_editar_monto")
        nuevo_monto = st.number_input("Nuevo monto", key="nuevo_monto")
        if st.button("Actualizar monto"):
            editar_monto_movimiento(id_monto, nuevo_monto)
            st.success("✅ Monto actualizado")

        st.subheader("Editar fecha")
        id_fecha = st.number_input("ID de fecha a editar", min_value=1, step=1, key="id_editar_fecha")
        nueva_fecha = st.date_input("Nueva fecha", value=date.today(), key="nueva_fecha")
        if st.button("Actualizar fecha"):
            editar_fecha_movimiento(id_fecha, nueva_fecha.isoformat())
            st.success("✅ Fecha actualizada")

    else:
        st.info("Todavía no hay movimientos registrados.")

# --- TAB 3: Gestionar usuarios ---
with tab3:
    st.header("Usuarios registrados")
    usuarios = obtener_usuarios()
    usuarios_dict = {id: nombre for id, nombre in usuarios}

    if usuarios:
        st.dataframe(pd.DataFrame(usuarios, columns=["ID", "Nombre"]))

        st.subheader("Editar usuario")
        id_seleccionado = st.selectbox("Seleccionar usuario", usuarios_dict.keys(), format_func=lambda x: usuarios_dict[x])
        nuevo_nombre = st.text_input("Nuevo nombre", value=usuarios_dict[id_seleccionado])
        if st.button("Guardar cambios"):
            editar_usuario(id_seleccionado, nuevo_nombre)
            st.success("✅ Nombre actualizado correctamente")
            st.rerun()

        st.subheader("Eliminar usuario")
        id_borrar = st.selectbox("Seleccionar usuario a eliminar", usuarios_dict.keys(), format_func=lambda x: usuarios_dict[x])
        if st.button("Eliminar usuario"):
            eliminar_usuario(id_borrar)
            st.success("✅ Usuario eliminado correctamente")
            st.rerun()
    else:
        st.info("No hay usuarios registrados.")

    st.subheader("Agregar nuevo usuario")
    nuevo_usuario = st.text_input("Nombre del nuevo usuario")
    if st.button("Agregar usuario"):
        agregar_usuario(nuevo_usuario)
        st.success(f"✅ Usuario '{nuevo_usuario}' agregado")
        st.rerun()

# --- TAB 4: Resumen mensual ---
with tab4:
    st.header("📊 Resumen mensual")

    usuarios = dict(obtener_usuarios())
    movimientos = obtener_movimientos()

    if not movimientos:
        st.info("No hay movimientos registrados aún.")
    else:
        df = pd.DataFrame(movimientos, columns=["ID", "Tipo", "Descripción", "Monto", "Fecha", "ID Usuario", "Participantes"])
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)
        df["Monto"] = df["Monto"].astype(float)
        df["ID Usuario"] = df["ID Usuario"].astype(int)
        df["Nombre Usuario"] = df["ID Usuario"].map(usuarios)

        meses_disponibles = df["Mes"].sort_values().unique().tolist()
        mes_seleccionado = st.selectbox("Seleccioná un mes", meses_disponibles)
        df_mes = df[df["Mes"] == mes_seleccionado]

        df_mes["Monto firmado"] = df_mes.apply(
            lambda x: x["Monto"] if x["Tipo"] == "ingreso" else -x["Monto"], axis=1
        )

        # Calcular totales
        total_gastos = df_mes[df_mes["Tipo"] == "gasto"]["Monto"].sum()
        total_ingresos = df_mes[df_mes["Tipo"] == "ingreso"]["Monto"].sum()

        # Mostrar métricas
        st.subheader("Totales del mes")
        col1, col2 = st.columns(2)
        col1.metric("💰 Total de ingresos", f"${total_ingresos:,.2f}")
        col2.metric("💸 Total de gastos", f"${total_gastos:,.2f}")


        aporte_por_persona = df_mes.groupby("Nombre Usuario")["Monto firmado"].sum().to_dict()

        for nombre in usuarios.values():
            aporte_por_persona.setdefault(nombre, 0.0)

        total_mes = sum(aporte_por_persona.values())
        num_personas = len(usuarios)
        promedio = round(total_mes / num_personas, 2)

        balances = {persona: round(aporte - promedio, 2) for persona, aporte in aporte_por_persona.items()}

        resumen = pd.DataFrame.from_dict(balances, orient="index", columns=["Saldo neto"])
        resumen_ganancia = pd.DataFrame.from_dict({p: promedio for p in usuarios.values()}, orient="index", columns=["Saldo neto"])

        st.subheader("💰 Ganancia/pérdida neta por persona")
        st.dataframe(resumen_ganancia.T)

        # Reparto equitativo
        st.subheader("🤝 Quién le debe a quién")

        saldos = resumen["Saldo neto"].to_dict()
        promedio = round(sum(saldos.values()) / len(saldos), 2)
        balances = {p: round(s - promedio, 2) for p, s in saldos.items()}

        gastos = {p: -v for p, v in balances.items() if v < 0}
        ingresos = {p: v for p, v in balances.items() if v > 0}

        transacciones = []

        for gasto, ingreso in gastos.items():
            for acreedor, credito in ingresos.items():
                if ingreso == 0:
                    break
                pago = min(ingreso, credito)
                if pago > 0:
                    transacciones.append(f"🔁 {acreedor} debe pagarle ${pago:.2f} a {gasto}")
                    gastos[gasto] -= pago
                    ingresos[acreedor] -= pago
                    ingreso -= pago

        if transacciones:
            for t in transacciones:
                st.markdown(t)
        else:
            st.info("Todos están equilibrados este mes 🎉")
