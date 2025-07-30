import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), 'watchman_http_server', 'config', '.env')
load_dotenv(dotenv_path, override=True)  # Charge les variables

WATCHMAN_API_KEY = os.getenv('WATCHMAN_API_KEY')
