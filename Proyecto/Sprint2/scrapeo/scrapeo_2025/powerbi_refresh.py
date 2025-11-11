#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refresca automáticamente un dataset de Power BI después del scraping.
- Busca el dataset por nombre (ej.: "Proyecto - Mapas ya incluidos ACTUAL").
- Si se indica WORKSPACE_ID, opera en ese workspace; sino, usa "My Workspace".

Requisitos de entorno (variables):
  TENANT_ID         -> ID del tenant Azure AD
  CLIENT_ID         -> ID de la App Registration (confidential client)
  CLIENT_SECRET     -> Secreto de la App Registration
  WORKSPACE_ID      -> (opcional) ID del workspace de Power BI

Uso:
  python powerbi_refresh.py --dataset "Proyecto - Mapas ya incluidos ACTUAL"
  python powerbi_refresh.py --workspace "<name>" --dataset "<dataset name>"  # si quieres resolver por nombre

Permisos necesarios en la App:
  - API Microsoft Power BI: Dataset.ReadWrite.All
  - Habilitar "Allow service principals to use Power BI APIs" en el tenant.
"""

import os
import sys
import time
import argparse
import requests
from dotenv import load_dotenv
load_dotenv()

try:
    from msal import ConfidentialClientApplication
except Exception as e:
    print("Falta dependencia 'msal'. Ejecuta: pip install msal")
    raise

API_ROOT = "https://api.powerbi.com/v1.0/myorg"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]


def get_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    app = ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in result:
        raise RuntimeError(f"No se pudo obtener token: {result}")
    return result["access_token"]


def resolve_workspace_id(token: str, workspace_name: str | None) -> str | None:
    if not workspace_name:
        return None  # usar My Workspace
    # Permite especificar explícitamente 'My Workspace' / 'Mi área de trabajo'
    if workspace_name.strip().lower() in ("my workspace", "mi área de trabajo", "mi area de trabajo"):
        return None
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API_ROOT}/groups", headers=headers)
    r.raise_for_status()
    groups = r.json().get("value", [])
    for g in groups:
        if g.get("name") == workspace_name:
            return g.get("id")
    raise RuntimeError(f"Workspace '{workspace_name}' no encontrado.")


def find_dataset(token: str, dataset_name: str, workspace_id: str | None) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    if workspace_id:
        url = f"{API_ROOT}/groups/{workspace_id}/datasets"
    else:
        url = f"{API_ROOT}/datasets"  # My Workspace
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    datasets = r.json().get("value", [])
    for d in datasets:
        if d.get("name") == dataset_name:
            return d.get("id")
    raise RuntimeError(f"Dataset '{dataset_name}' no encontrado en {'workspace '+workspace_id if workspace_id else 'My Workspace'}.")


def trigger_refresh(token: str, dataset_id: str, workspace_id: str | None) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {"notifyOption": "MailOnFailure"}
    if workspace_id:
        url = f"{API_ROOT}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    else:
        url = f"{API_ROOT}/datasets/{dataset_id}/refreshes"
    r = requests.post(url, headers=headers, json=body)
    if r.status_code not in (200, 202):
        raise RuntimeError(f"Error al lanzar refresh ({r.status_code}): {r.text}")
    print("✓ Refresh lanzado correctamente")


def wait_for_refresh(token: str, dataset_id: str, workspace_id: str | None, timeout_sec: int = 600) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    if workspace_id:
        url = f"{API_ROOT}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    else:
        url = f"{API_ROOT}/datasets/{dataset_id}/refreshes"
    start = time.time()
    last_status = "unknown"
    while time.time() - start < timeout_sec:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        items = r.json().get("value", [])
        if items:
            status = items[0].get("status")
            last_status = status
            print(f"  Estado último refresh: {status}")
            if status in ("Completed", "Failed", "Unknown"):
                return status
        time.sleep(5)
    return last_status


def main():
    parser = argparse.ArgumentParser(description="Refrescar dataset de Power BI")
    parser.add_argument("--dataset", required=True, help="Nombre del dataset publicado")
    parser.add_argument("--workspace", help="Nombre del workspace (opcional)")
    args = parser.parse_args()

    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    workspace_id_env = os.getenv("WORKSPACE_ID")

    if not all([tenant_id, client_id, client_secret]):
        print("✗ Faltan variables de entorno TENANT_ID, CLIENT_ID o CLIENT_SECRET")
        sys.exit(1)

    token = get_token(tenant_id, client_id, client_secret)
    # Priorizar el workspace pasado por argumento (si se especifica)
    ws_id = resolve_workspace_id(token, args.workspace) if args.workspace else workspace_id_env
    ds_id = find_dataset(token, args.dataset, ws_id)

    print(f"Workspace: {ws_id or 'My Workspace'} | Dataset: {args.dataset} ({ds_id})")
    trigger_refresh(token, ds_id, ws_id)
    status = wait_for_refresh(token, ds_id, ws_id, timeout_sec=600)
    print(f"Resultado del refresh: {status}")
    if status != "Completed":
        sys.exit(2)


if __name__ == "__main__":
    main()