import os

import environ
from dotenv import load_dotenv

env = environ.Env()

env.read_env()

config_dir = os.path.join(os.getcwd(), 'watchman_http_server', 'config')
os.makedirs(config_dir, exist_ok=True)
dotenv_path = os.path.join(config_dir, '.env')


# Charger les variables depuis .env
success = load_dotenv(dotenv_path, override=True)

# Récupérer la clé d'API
WATCHMAN_API_KEY = os.getenv('WATCHMAN_API_KEY')
