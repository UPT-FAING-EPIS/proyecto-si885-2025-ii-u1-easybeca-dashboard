import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Carpeta local sincronizada con OneDrive/SharePoint
TARGET_DIR = os.getenv(
    "SYNC_ONEDRIVE_PATH",
    r"C:\Users\Angel\UNIVERSIDAD PRIVADA DE TACNA\SCRAPING - Documentos\Becas",
)
# Tipos de archivo a copiar (separados por ';')
FILE_GLOBS = [g.strip() for g in os.getenv("SYNC_FILE_GLOBS", "*.csv;*.json").split(";") if g.strip()]

REPO_DIR = Path(__file__).resolve().parent
TARGET_PATH = Path(TARGET_DIR)

EXCLUDE_SUFFIXES = {".log", ".pbix"}


def ensure_target():
    TARGET_PATH.mkdir(parents=True, exist_ok=True)


def copy_matches():
    copied = []
    for pattern in FILE_GLOBS:
        for src in REPO_DIR.glob(pattern):
            if src.suffix.lower() in EXCLUDE_SUFFIXES:
                continue
            dest = TARGET_PATH / src.name
            shutil.copy2(src, dest)
            copied.append((src.name, str(dest)))
    return copied


if __name__ == "__main__":
    ensure_target()
    results = copy_matches()
    print(f"Archivos copiados: {len(results)} → {TARGET_PATH}")
    for name, dest in results:
        print(f" - {name} -> {dest}")