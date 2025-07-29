from rich.console import Console
from pathlib import Path
import json

from fastapi_start_project.utils import crear_estructura
from fastapi_start_project.files_content import (
    contenido_main_base, contenido_main_jinja2,
    contenido_docker, contenido_docker_compose,
    contenido_env, contenido_readme,
    base_html, index_html, estilos_index_jinja2,
    contenido_requisitos_base, contenido_jinja2,
    contenido_mysql, contenido_postgresql,
    contenido_routes_init, contenido_test_app, database_config
)

console = Console()

# 🧾 Generar database_config.py
def generar_database_config(nombre_app, db_url):
    if not db_url:
        return

    contenido_archivo = database_config(db_url)
    ruta = Path(nombre_app) / "database" / "database_config.py"
    ruta.write_text(contenido_archivo.rstrip() + "\n", encoding="utf-8")

# 🧪 Generar entornos
def generar_entornos(nombre_app, entornos):
    if not entornos:
        return

    ent_list = [e.strip() for e in entornos.split(",") if e.strip()]

    for entorno in ent_list:
        nombre_env = f".env.{entorno.lower()}"
        ruta_env = Path(nombre_app) / nombre_env
        contenido_env_file = contenido_env(extra_vars={"ENV_NAME": entorno.upper()})
        ruta_env.write_text(contenido_env_file.rstrip() + "\n", encoding="utf-8")

        nombre_dc = f"docker-compose.{entorno.lower()}.yml"
        ruta_dc = Path(nombre_app) / nombre_dc
        contenido_dc_file = contenido_docker_compose(nombre_app, entorno)
        ruta_dc.write_text(contenido_dc_file.rstrip() + "\n", encoding="utf-8")

        print(f"🛠️  Archivos para entorno '{entorno}' generados.")
    print(f"✅ Todos los entornos [{', '.join(ent_list)}] han sido configurados.")

# ⚙️ Configurar la aplicación
def configurar_app(nombre_app: str = "FastAPI-APP", configuracion: dict = None):
    if configuracion is None:
        raise ValueError("La configuración no puede ser None")

    ruta_app = Path(nombre_app)

    templates_activo = bool(configuracion.get("templates", False))
    base_datos = str(configuracion.get("base_de_datos", "")).lower()
    usar_docker = bool(configuracion.get("docker", False))

    estructura = {
        "models": ["__init__.py"],
        "routes": ["__init__.py"],
        "schemas": ["__init__.py"],
        "services": ["__init__.py"],
        "database": ["__init__.py"]
    }

    if templates_activo:
        estructura["templates"] = ["base.html", "index.html"]
        estructura["static/js"] = ["index.js"]
        estructura["static/styles"] = ["style.css"]
        estructura["static/images"] = []
        estructura["static/audio"] = []

    crear_estructura(nombre_app, estructura)

    # routes/__init__.py
    (ruta_app / "routes" / "__init__.py").write_text(contenido_routes_init.rstrip() + "\n", encoding="utf-8")

    # main.py
    contenido_main = contenido_main_jinja2 if templates_activo else contenido_main_base
    (ruta_app / "main.py").write_text(contenido_main.strip() + "\n", encoding="utf-8")

    # Docker
    if usar_docker:
        (ruta_app / "Dockerfile").write_text(contenido_docker.strip() + "\n", encoding="utf-8")
        entornos = configuracion.get("entornos", None)
        (ruta_app / "docker-compose.yml").write_text(
            contenido_docker_compose(nombre_app, entornos).strip() + "\n", encoding="utf-8"
        )
        generar_entornos(nombre_app, entornos)

    # .env y database_config.py
    if base_datos == "mysql":
        db_url = "mysql+asyncmy://user:password@localhost/dbname"
    elif base_datos == "postgresql":
        db_url = "postgresql+asyncpg://user:password@localhost/dbname"
    elif base_datos == "sqlite":
        db_url = "sqlite+aiosqlite:///./app.db"
    else:
        db_url = ""
        console.print("[yellow]⚠️ Base de datos no reconocida. Se omitió la configuración de conexión.[/]")

    extra_env_vars = configuracion.get("extra_env_vars", None)
    (ruta_app / ".env").write_text(
        contenido_env(db_url, extra_env_vars).strip() + "\n", encoding="utf-8"
    )
    generar_database_config(nombre_app, db_url)

    # README.md
    (ruta_app / "README.md").write_text(
        contenido_readme(nombre_app).strip() + "\n", encoding="utf-8"
    )

    # requirements.txt
    requisitos = contenido_requisitos_base[:]
    if templates_activo:
        requisitos.append(contenido_jinja2.strip())
    if base_datos == "mysql":
        requisitos.append(contenido_mysql.strip())
    elif base_datos == "postgresql":
        requisitos.append(contenido_postgresql.strip())
    requisitos.append("pytest")

    (ruta_app / "requirements.txt").write_text("\n".join(requisitos) + "\n", encoding="utf-8")

    # Archivos de templates y estáticos
    if templates_activo:
        for carpeta in [
            ruta_app / "templates",
            ruta_app / "static" / "js",
            ruta_app / "static" / "styles",
            ruta_app / "static" / "images",
            ruta_app / "static" / "audio",
        ]:
            carpeta.mkdir(parents=True, exist_ok=True)

        (ruta_app / "templates" / "base.html").write_text(base_html.strip() + "\n", encoding="utf-8")
        (ruta_app / "templates" / "index.html").write_text(index_html.strip() + "\n", encoding="utf-8")
        (ruta_app / "static" / "styles" / "style.css").write_text(estilos_index_jinja2.strip() + "\n", encoding="utf-8")
        (ruta_app / "static" / "js" / "index.js").write_text("// JavaScript inicial\n", encoding="utf-8")

    # test_app.py
    tests_path = ruta_app / "tests"
    tests_path.mkdir(parents=True, exist_ok=True)
    (tests_path / "test_app.py").write_text(contenido_test_app.rstrip() + "\n", encoding="utf-8")

    # config.json
    with open(ruta_app / "config.json", "w", encoding="utf-8") as f:
        json.dump(configuracion, f, indent=4, ensure_ascii=False)

    console.print(f"\n[bold green]✅ ¡Configuración completada! Aplicación {nombre_app} generada con éxito.[/]")
