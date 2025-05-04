# ✅ Checklist: Actualizar la App de Gastos en Render

### 🧑‍💻 1. Hacer cambios en el código

Modificá archivos como:

* `app.py`
* `database.py`
* `requirements.txt`
* `Dockerfile`

---

### 🧪 2. (Opcional) Probar localmente

**Si usás entorno virtual (recomendado):**

```bash
.venv\Scripts\Activate
streamlit run app.py
```

**O con Docker:**

```bash
docker compose up --build
(si es necesario primero destruir usar: docker compose down -v)
```

---

### 📤 3. Subir los cambios a GitHub

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

> ⚠️ Requiere tener el repo vinculado a GitHub y conectado a Render.

---

### 🚀 4. Verificar el deploy en Render

1. Ir a: [https://dashboard.render.com](https://dashboard.render.com/)
2. Abrir el servicio (Web Service).
3. Ir a la pestaña  **Deploys** .
4. Verificar que diga **"Live"** en verde.

---

### 🔍 5. Verificar que la app funcione

Entrar al link público (https://gestion-239.onrender.com) y comprobar:

* Se ven los nuevos cambios.
* No hay errores al usar la app.
* Revisar la pestaña **Logs** si algo falla.

---

### 💡 Consejos extra

* ⚠️ No incluir `sqlite3` en `requirements.txt`.
* 🔐 Nunca subir archivos `.db` sensibles al repo (usá `.gitignore`).
* ✅ Podés usar `print()` para rastrear ingresos/ediciones en los logs.
* 📧 Activá notificaciones de errores en los Settings del servicio.
