
# 🩸 Sistema de Gestión de Donantes de Sangre

El **Sistema de Gestión de Donantes de Sangre** es una plataforma web diseñada para optimizar el proceso de donación y abastecimiento de sangre en hospitales y centros de salud.  
Permite a los donantes registrarse, gestionar sus turnos y mantener un historial de donaciones, mientras que los doctores y administradores pueden aprobar solicitudes, coordinar campañas y buscar donantes según tipo de sangre y disponibilidad.  
El sistema asegura una gestión eficiente mediante la asignación de roles de usuario, control de disponibilidad según la última donación y la automatización de procesos clave en la planificación de donaciones.
Este proyecto es una aplicación **monolítica** desarrollada con **Flask**, **HTML**, **CSS** y **JavaScript**, utilizando **PostgreSQL** como base de datos.  
El objetivo es ofrecer una estructura base limpia y modular para construir un sistema de gestión con rutas, vistas y base de datos conectada. 

---

## 🚀 Tecnologías utilizadas

- **Flask** (Python)
- **PostgreSQL**
- **SQLAlchemy**
- **HTML / CSS / JS**
- **dotenv** (para manejo de variables de entorno)

---

## 📂 Estructura del proyecto

```

sistema/
│
├── app/
│   ├── **init**.py          # Inicializa la app y la conexión con la BD
│   ├── routes.py            # Rutas principales
│   ├── static/              # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/           # Archivos HTML (vistas)
│
├── .env                     # Variables de entorno (NO se sube al repo)
├── .gitignore
├── requirements.txt         # Dependencias del proyecto
├── run.py                   # Punto de entrada de la aplicación
└── venv/                    # Entorno virtual (NO se sube al repo)

````

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/sistema-flask.git
cd sistema-flask
````

### 2️⃣ Crear entorno virtual

En Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

En Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Crear archivo `.env`

En la raíz del proyecto, crear un archivo llamado `.env` con el siguiente contenido:

```bash
FLASK_ENV=development
SECRET_KEY=clave_super_secreta

DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sistema_gestion

DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

⚠️ **Importante:** asegurate de que la base de datos `sistema_gestion` exista en PostgreSQL antes de ejecutar la app.

---

### 5️⃣ Ejecutar la aplicación

```bash
flask run
```

Si todo está correcto, deberías ver en consola:

```
✅ Conexión exitosa a la base de datos PostgreSQL
 * Running on http://127.0.0.1:5000
```

Luego podés abrir el navegador y acceder a:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🧠 Notas

* El archivo `.env` **no se sube a GitHub**.
* Si querés cambiar el nombre de la base de datos, actualizá también el valor de `DB_NAME` en el `.env`.
* Podés extender las rutas y modelos en `app/routes.py` y `app/models.py`.

---

## 👥 Colaboradores

* **@TuUsuario** – Desarrollador principal
* **@Compañero** – Colaborador

---

## 🪪 Licencia

Este proyecto está bajo la licencia **MIT**. Podés usarlo, modificarlo y distribuirlo libremente.

```

---

¿Querés que te adapte este `README.md` para que el proyecto también pueda desplegarse fácilmente (por ejemplo en **Render** o **Railway**, conectando con PostgreSQL online)?
```
