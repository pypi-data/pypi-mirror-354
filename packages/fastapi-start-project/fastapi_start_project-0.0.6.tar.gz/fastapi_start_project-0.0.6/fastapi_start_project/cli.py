# main.py

from rich.console import Console
from rich.panel import Panel
import questionary
import sys
import json
from pathlib import Path


# Importar funciones personalizadas
try:
    from utils import limpiar_consola
    from config_app import configurar_app
except ImportError as e:
    print(f"[ERROR] No se pudieron importar los módulos necesarios: {e}")
    sys.exit(1)

# Crear consola Rich
console = Console()

def main():
    # 🎉 Mostrar mensaje de bienvenida
    console.print()
    console.print(Panel.fit(
        "[bold green]Bienvenido a tu configurador de aplicaciones con FastAPI[/]",
        title="🚀 FastAPI Start App ⚡"
    ))

    # 📝 Nombre de la app
    nombre_app = questionary.text("📝 Nombre de la app:").ask()
    if not nombre_app or not nombre_app.strip():
        console.print("[bold red]❌ Nombre no válido.[/]")
        sys.exit(1)

    # 📦 Base de datos
    data_base = questionary.select(
        "📦 Elige tu base de datos:",
        choices=["MySQL", "SQLite", "PostgreSQL", "Ninguna"]
    ).ask()
    if data_base is None:
        sys.exit()

    # 🗃️ Alembic
    alembic = questionary.confirm("🗃️ ¿Usar migraciones con Alembic?").ask()
    if alembic is None:
        sys.exit()

    # 🧩 Jinja2
    templates = questionary.confirm("🧩 ¿Agregar soporte para plantillas Jinja2?").ask()
    if templates is None:
        sys.exit()

    # 🚢 Docker
    docker = questionary.confirm("🚢 ¿Configurar entornos con Docker?").ask()
    if docker is None:
        sys.exit()

    # 📦 Entornos
    entornos = None
    if docker:
        entornos = questionary.select(
            "¿Qué entornos deseas configurar?",
            choices=[
                "Pruebas, Desarrollo y Despliegue",
                "Desarrollo y Despliegue",
                "Desarrollo y Pruebas",
                "Despliegue y Pruebas",
                "Solo Desarrollo",
                "Solo Pruebas",
                "Solo Despliegue"
            ]
        ).ask()
        if entornos is None:
            sys.exit()

    # 🧾 Mostrar resumen
    limpiar_consola()
    console.print("\n[bold cyan]Resumen de configuración:[/]")
    console.print(f"\nNombre del proyecto: [bold green]{nombre_app}[/]")
    console.print(f"🔗 Base de datos elegida: [bold yellow]{data_base}[/]")
    console.print(f"🗃️ Migraciones con Alembic: [bold yellow]{'Sí' if alembic else 'No'}[/]")
    console.print(f"🧩 Uso de Jinja2: [bold yellow]{'Sí' if templates else 'No'}[/]")
    console.print(f"🚢 Uso de Docker: [bold yellow]{'Sí' if docker else 'No'}[/]")
    if entornos:
        console.print(f"📦 Entornos a configurar: [bold yellow]{entornos}[/]")
    console.print()

    # ✅ Confirmación
    confirmacion = questionary.select(
        "¿Proceder con la configuración actual?",
        choices=["Continuar", "Cancelar"]
    ).ask()

    if confirmacion != "Continuar":
        console.print("\n[bold red]❌ Configuración cancelada por el usuario.[/]")
        sys.exit()

    # 📦 Diccionario de configuración
    config_data = {
        "nombre_app": nombre_app,
        "base_de_datos": data_base,
        "alembic": alembic,
        "templates": templates,
        "docker": docker,
        "entornos": entornos if docker else None
    }

    try:
        limpiar_consola()
        configurar_app(nombre_app, config_data)
        console.print(f"""\nEjecuta:
        cd {nombre_app};
        python -m venv venv;
        Windows: venv/scripts/activate;
        Linux:source venv/bin/activate;
        pip install -r requirements.txt;
        uvicorn main:app --reload;
""")
    except Exception as e:
        console.print(f"[bold red]❌ Ocurrió un error al generar el proyecto: {e}[/]")
        sys.exit(1)

# 🔁 Punto de entrada
if __name__ == "__main__":
    main()
