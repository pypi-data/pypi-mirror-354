"""
Este módulo contiene un conjunto de variables con el contenido base para los archivos generados
automáticamente en un proyecto FastAPI.
"""

# 🐳 Dockerfile
contenido_docker = """
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# ⚙️ docker-compose.yml con soporte para entornos
contenido_docker_compose = lambda nombre_app, entornos=None: f"""
version: "3.9"

services:
  {nombre_app}:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
    env_file:
      - .env{f".{entornos.lower()}" if entornos and isinstance(entornos, str) else ""}
    environment:
{_formatear_entornos(entornos)}
"""

def _formatear_entornos(entornos):
    # Convierte una cadena con entornos en variables de entorno para docker-compose
    if not entornos:
        return "      # Sin entornos específicos configurados"
    lines = []
    ent_list = [e.strip() for e in entornos.split(",")]
    for e in ent_list:
        key = e.upper().replace(" ", "_")
        lines.append(f"      - ENV_{key}=true")
    return "\n".join(lines)


# 🧠 main.py (sin Jinja2)
contenido_main_base = """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola FastAPI!"}
"""

# 🎨 main.py con Jinja2
contenido_main_jinja2 = """
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
"""

# Contenido base.html
base_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mi APP</title>
    <!-- Estilos -->
    {% block styles %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    <!-- Scripts -->
    {% block scripts %}{% endblock %}
</body>
</html>
"""

# Contenido index.html
index_html = """
{% extends "base.html" %}
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', path='styles/style.css') }}">
{% endblock %}

{% block content %}
<div class="container">
    <a href="https://fastapi.tiangolo.com/es/" target="_blank" rel="noopener noreferrer">
        <img class="fastapi-logo" src="https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-1/fastapi-logo.png" alt="fastapi-logo" />
    </a>
    <span class="plus">+</span>
    <h1><a href="#">¡Start Project!</a></h1><!-- Pendiente link repo -->
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', path='js/index.js') }}"></script>
{% endblock %}
"""

# Estilos CSS index
estilos_index_jinja2 = """
/* Estilos generales */
body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #272525;
    color: #d9d4d4;
    margin: 0;
    padding: 0;
    font-family: sans-serif;
}

.fastapi-logo {
    cursor: pointer;
    max-width: 400px;
    filter: drop-shadow(0 0 5px #019083);
    transition: filter 0.5s;
}
.fastapi-logo:hover {
    filter: drop-shadow(0 0 10px #019083);
}
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.plus {
    font-size: xx-large;
}

h1 {
    margin-top: 5px;
    font-family: "Ancizar Sans", sans-serif;
    font-optical-sizing: auto;
    font-style: italic;
    font-size: 60px;
    color: #019083;
    cursor: pointer;
    transition: text-shadow 0.5s;
    text-shadow: 0 0 5px #019083;
    animation-name: start-project;
}

h1:hover {
    text-shadow: 0 0 10px #019083;
}

/* Animaciones */
@keyframes logo-fade-in {
    0% {
        opacity: 0;
        transform: scale(0.8);
        filter: drop-shadow(0 0 0px #019083);
    }
    100% {
        opacity: 1;
        transform: scale(1);
        filter: drop-shadow(0 0 5px #019083);
    }
}

@keyframes title-glow {
    0% {
        opacity: 0;
        text-shadow: 0 0 0px #019083;
        transform: translateY(-20px);
    }
    50% {
        opacity: 1;
        text-shadow: 0 0 15px #01d4aa;
        transform: translateY(0);
    }
    100% {
        text-shadow: 0 0 5px #019083;
    }
}

@keyframes plus-pulse {
    0% {
        transform: scale(1);
        text-shadow: 0 0 5px #cfb577;
    }
    50% {
        transform: scale(1.2);
        text-shadow: 0 0 15px #f8cc67;
    }
    100% {
        transform: scale(1);
        text-shadow: 0 0 5px #a48336;
    }
}

/* Aplica las animaciones */
.fastapi-logo {
    animation: logo-fade-in 1.2s ease-out forwards;
}

h1 {
    animation: title-glow 1.5s ease-out forwards;
}
.plus {
    font-size: 62px;
    animation: plus-pulse 2s infinite ease-in-out;
    color: #f8cd67af;
    transition: transform 0.3s;
}
a {
    text-decoration: none;
    color: inherit;
}
"""

# 📦 requirements.txt
contenido_requisitos_base = ["fastapi", "uvicorn[standard]", "sqlalchemy", "aiofiles"]
contenido_jinja2 = "jinja2\n"
contenido_mysql = "mysql-connector-python\n"
contenido_postgresql = "psycopg2-binary\n"

# 📒 README.md
contenido_readme = lambda nombre: f"# {nombre}\n\nProyecto generado automáticamente con amor y FastAPI. 🚀"

# 🔐 .env
contenido_env = lambda db_url="", extra_vars=None: f"""# Variables de entorno

# URL de la base de datos
DATABASE_URL={db_url if db_url else "sqlite:///./app.db"}
{_formatear_extra_vars(extra_vars)}
"""

def _formatear_extra_vars(extra_vars):
    if not extra_vars:
        return ""
    lines = []
    for k, v in extra_vars.items():
        lines.append(f"{k}={v}")
    return "\n".join(lines)

# 🧾 database_config.py (para conexión a la base de datos)
database_config = lambda db_url: f"""
# Modulos externos
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Definimos la URL de conexión
DATABASE_URL = "{db_url}"

# Creamos el motor de conexión asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,    # Para mostrar en consola las consultas SQL ejecutadas
)

# Creamos la fábrica de sesiones asíncronas
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

# Base declarativa para los modelos
class Base(DeclarativeBase):
    pass

# Dependencia para obtener una sesión en cada operación
async def get_session():
    async with async_session() as session:
        yield session
"""

# 🗂️ Alembic ini básico para migraciones
contenido_alembic_ini = """
[alembic]
script_location = alembic

[alembic:exclude]
tables = spatial_ref_sys
"""

contenido_routes_init = """
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}
""".strip()

# Script de migración inicial vacío
contenido_alembic_env_py = """
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""
# 🧪 test_app.py
contenido_test_app = """
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
""".strip()
