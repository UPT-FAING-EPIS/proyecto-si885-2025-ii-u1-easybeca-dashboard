#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sube archivos .json/.csv del proyecto a OneDrive o SharePoint usando Microsoft Graph.
Evita el gateway: el PBIX puede conectarse a la biblioteca/documento en la nube y refrescarse en el servicio.

Requisitos:
- Variables de entorno (se cargan desde .env si existe):
  TENANT_ID, CLIENT_ID, CLIENT_SECRET
  GRAPH_TARGET = onedrive | sharepoint
  GRAPH_CLOUD_FOLDER = /Becas (carpeta destino en la nube)
  Para OneDrive: GRAPH_USER_UPN = usuario@dominio.com
  Para SharePoint: SHAREPOINT_SITE_ID, SHAREPOINT_DRIVE_ID
  Opcional: GRAPH_AUTH = app | device (device permite login interactivo del usuario para OneDrive)

Permisos:
- App-only (GRAPH_AUTH=app):
  - OneDrive: Files.ReadWrite.All (Application) + admin consent
  - SharePoint: Sites.Selected (Application) asignado al sitio; o Sites.ReadWrite.All
- User (GRAPH_AUTH=device, solo OneDrive):
  - Delegados: Files.ReadWrite (normalmente sin admin consent)
"""
import os
import sys
import requests
from msal import ConfidentialClientApplication, PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
BASE_URL = "https://graph.microsoft.com/v1.0"

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TARGET = os.getenv("GRAPH_TARGET", "onedrive").lower()
CLOUD_FOLDER = os.getenv("GRAPH_CLOUD_FOLDER", "/Becas")
USER_UPN = os.getenv("GRAPH_USER_UPN")
SITE_ID = os.getenv("SHAREPOINT_SITE_ID")
DRIVE_ID = os.getenv("SHAREPOINT_DRIVE_ID")
AUTH_MODE = os.getenv("GRAPH_AUTH", "app").lower()


def get_token_app() -> str:
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
        raise RuntimeError("Faltan TENANT_ID/CLIENT_ID/CLIENT_SECRET en entorno")
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    res = app.acquire_token_for_client(scopes=GRAPH_SCOPE)
    if "access_token" not in res:
        raise RuntimeError(f"No se pudo obtener token Graph (app-only): {res}")
    return res["access_token"]


def get_token_device() -> str:
    if not all([TENANT_ID, CLIENT_ID]):
        raise RuntimeError("Faltan TENANT_ID/CLIENT_ID para login de usuario")
    pca = PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    )
    # Solo OneDrive con permisos delegados del usuario
    scopes = ["Files.ReadWrite"]
    flow = pca.initiate_device_flow(scopes=scopes)
    if not flow or "user_code" not in flow:
        raise RuntimeError("No se pudo iniciar el device code flow")
    print("Autenticación de usuario requerida. Ve a https://microsoft.com/devicelogin y pega este código:")
    print(flow["user_code"])
    print("Luego vuelve aquí. Esperando confirmación...")
    res = pca.acquire_token_by_device_flow(flow)
    if "access_token" not in res:
        raise RuntimeError(f"No se pudo obtener token Graph (device): {res}")
    return res["access_token"]


def get_token() -> str:
    if AUTH_MODE == "device":
        if TARGET != "onedrive":
            raise RuntimeError("Login de usuario (device) solo compatible con OneDrive. Usa GRAPH_AUTH=app para SharePoint.")
        return get_token_device()
    return get_token_app()


def drive_root_url() -> str:
    if TARGET == "onedrive":
        if not USER_UPN:
            raise RuntimeError("GRAPH_USER_UPN es requerido para OneDrive")
        return f"{BASE_URL}/users/{USER_UPN}/drive"
    if TARGET == "sharepoint":
        if not SITE_ID or not DRIVE_ID:
            raise RuntimeError("SHAREPOINT_SITE_ID y SHAREPOINT_DRIVE_ID requeridos para SharePoint")
        return f"{BASE_URL}/sites/{SITE_ID}/drives/{DRIVE_ID}"
    raise RuntimeError("GRAPH_TARGET debe ser 'onedrive' o 'sharepoint'")


def ensure_folder(token: str, folder_path: str) -> None:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    path = folder_path.strip("/")
    if not path:
        return
    parts = path.split("/")
    parent = ""
    for name in parts:
        current = f"{parent}/{name}" if parent else name
        # Comprobar existencia
        check_url = f"{drive_root_url()}/root:/{current}"
        r = requests.get(check_url, headers=headers)
        if r.status_code == 404:
            # Crear dentro del padre
            if parent:
                create_url = f"{drive_root_url()}/root:/{parent}:/children"
            else:
                create_url = f"{drive_root_url()}/root/children"
            body = {"name": name, "folder": {}, "@microsoft.graph.conflictBehavior": "fail"}
            r2 = requests.post(create_url, headers=headers, json=body)
            if r2.status_code not in (201, 409):
                raise RuntimeError(f"No se pudo crear carpeta '{current}': {r2.status_code} {r2.text}")
        parent = current


def upload_file(token: str, local_path: str, cloud_folder: str) -> None:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"}
    fname = os.path.basename(local_path)
    cloud_path = f"{cloud_folder.strip('/')}/{fname}" if cloud_folder else fname
    url = f"{drive_root_url()}/root:/{cloud_path}:/content"
    with open(local_path, "rb") as f:
        r = requests.put(url, headers=headers, data=f)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Error subiendo {fname}: {r.status_code} {r.text}")
    item = r.json()
    print(f"✓ Subido {fname} -> {item.get('webUrl')}")


def main():
    token = get_token()
    print(f"Destino: {TARGET} | Auth: {AUTH_MODE} | Carpeta nube: {CLOUD_FOLDER}")
    ensure_folder(token, CLOUD_FOLDER)
    base = os.path.dirname(__file__)
    nombres = os.listdir(base)
    to_upload = [os.path.join(base, n) for n in nombres if n.lower().endswith((".json", ".csv"))]
    excluir = {"requirements.txt"}
    to_upload = [p for p in to_upload if os.path.basename(p) not in excluir]
    if not to_upload:
        print("No hay archivos .json/.csv para subir.")
        return
    for path in to_upload:
        upload_file(token, path, CLOUD_FOLDER)


if __name__ == "__main__":
    main()