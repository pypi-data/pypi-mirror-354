import os
import getmac
from dotenv import load_dotenv, set_key
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
import platform
import subprocess
import json
import logging
import socket

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurer le logger pour avoir plus de détails
logger = logging.getLogger("uvicorn")

# Créer un middleware pour la clé API
api_key_header = APIKeyHeader(name="WATCHMAN-API-KEY")


def create_env_file(api_key):
    # Utiliser le répertoire courant d'exécution, normalement ton projet local
    project_root = os.getcwd()  # <-- dossier d'où tu lances la commande
    config_dir = os.path.join(project_root, 'watchman_http_server', 'config')
    os.makedirs(config_dir, exist_ok=True)

    env_path = os.path.join(config_dir, '.env')

    set_key(env_path, "WATCHMAN_API_KEY", api_key)
    load_dotenv(env_path, override=True)


def api_key_required(api_key: str = Depends(api_key_header)):
    from watchman_http_server.config import settings
    if api_key != settings.WATCHMAN_API_KEY:
        raise HTTPException(
            status_code=403, detail="Forbidden: Invalid API Key"
        )


# fonction pour recupérer les infos du system
def get_system_info():
    """Récupère les infos système : OS, IP, MAC, etc."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Récupération propre de l'adresse MAC
    mac_address = getmac.get_mac_address()

    architecture = platform.machine()
    os_info = f"{platform.system()} {platform.release()}"

    return {
        "hostname": hostname,
        "ip": ip_address,
        "mac": mac_address,
        "architecture": architecture,
        "os": os_info
    }


# fonction pour recupérer les applications installées sur le system
def get_installed_apps():
    """Récupère la liste des applications installées selon l'OS."""
    system = platform.system()
    apps = []

    if system == "Windows":
        try:
            output = subprocess.check_output(
                ["wmic", "product", "get", "name,vendor,version"],
                universal_newlines=True,
                errors='ignore'
            )
            lines = output.strip().split("\n")

            # Suppression de la première ligne (en-tête)
            if len(lines) > 1:
                lines = lines[1:]
            for line in lines:
                parts = line.strip().split("  ")
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) == 3:
                    apps.append({"name": parts[0], "vendor": parts[1], "version": parts[2], "type": "application"})

        except Exception as e:
            logging.error(f"Error retrieving applications on Windows: {e}")
            return {"error": str(e)}

    elif system == "Linux":
        try:
            output = subprocess.check_output(
                ["dpkg-query", "-W", "-f=${Package} ${Version} ${Maintainer}\n"],
                universal_newlines=True,
                errors='ignore'
            )
            for line in output.strip().split("\n"):
                parts = line.split(" ")
                if len(parts) >= 3:
                    name = parts[0]
                    version = parts[1]
                    vendor = " ".join(parts[2:])
                    apps.append({"name": name, "vendor": vendor, "version": version, "type": "application"})
        except Exception as e:
            logging.error(f"Error retrieving applications on Linux: {e}")
            return {"error": str(e)}

    elif system == "Darwin":  # macOS
        try:
            output = subprocess.check_output(["system_profiler", "SPApplicationsDataType", "-json"],
                                             universal_newlines=True, errors='ignore')
            data = json.loads(output)
            if "SPApplicationsDataType" in data:
                for app in data["SPApplicationsDataType"]:
                    name = app.get("_name", "Unknown")
                    version = app.get("version", "Unknown")
                    vendor = app.get("obtained_from", "Unknown")
                    apps.append({"name": name, "vendor": vendor, "version": version, "type": "application"})
        except Exception as e:
            logging.error(f"Error retrieving applications on macOS: {e}")
            return {"error": str(e)}

    return apps


# endpoint de récupération des  infos et les applications installées du system
@app.get("/apps")
def list_apps(api_key: str = Depends(api_key_required)):
    """Endpoint pour récupérer les applications installées avec infos système."""
    system_info = get_system_info()
    applications = get_installed_apps()

    # Ajouter l'OS en tant qu'application
    system_info_app = {
        "name": system_info["os"],
        "version": platform.release(),
        "vendor": system_info["os"],
        "type": "os"
    }

    response = {
        "system_info": system_info,
        "applications": [system_info_app] + applications
    }

    return response


# Liste des IPs autorisées
ENABLE_IP_FILTERING = os.getenv("ENABLE_IP_FILTERING", "false").lower() == "true"

if ENABLE_IP_FILTERING:
    @app.middleware("http")
    async def check_ip(request: Request, call_next):
        client_ip = request.client.host
        allowed_ips = os.getenv("ALLOWED_IPS", "127.0.0.1").replace("'", "").split(",")
        allowed_ips = [ip.strip() for ip in allowed_ips]

        # print(f"Client IP: {client_ip}")
        # print(f"Allowed IPs: {allowed_ips}")

        try:
            if client_ip in allowed_ips:
                return await call_next(request)
            return JSONResponse(status_code=403, content={"error": f"Unauthorized IP: {client_ip}"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
async def read_root():
    return {"message": "Hello, authorized user!"}
