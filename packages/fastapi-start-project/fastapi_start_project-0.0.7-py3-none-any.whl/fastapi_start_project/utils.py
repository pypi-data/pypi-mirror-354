# utils.py

"""
Este modulo contiene todas varidad de funciones utiles para el proyecto
"""
from pathlib import Path
import os

# Limpiar la consola
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Crear carpetas y archivos
def crear_estructura(base_path, estructura):
    """
    Crea carpetas y archivos según la estructura dada.

    :param base_path: Ruta base donde se crea todo.
    :param estructura: Diccionario con nombres de carpetas y lista de archivos.
                       Ejemplo: {"carpeta1": ["a.txt", "b.py"], "carpeta2": []}
    """
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)

    for carpeta, archivos in estructura.items():
        carpeta_path = base_path / carpeta
        carpeta_path.mkdir(parents=True, exist_ok=True)

        for archivo in archivos:
            archivo_path = carpeta_path / archivo
            archivo_path.touch(exist_ok=True)  # Crea el archivo si no existe
            # Opcional: escribe contenido por defecto
            archivo_path.write_text(f"# Archivo generado: {archivo}", encoding="utf-8")

