import os
from pathlib import Path

import dotenv

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv(Path(THIS_DIR) / 'config/.env')

ELASTIC_USER = os.environ.get('ELASTIC_USER')
ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')
CERT_PATH = os.environ.get('CERT_PATH')
ELASTIC_URL = os.environ.get('ELASTIC_URL')
SEARCH_CONFIGS_DIR = os.path.join(THIS_DIR, 'search_configs')
FRONTEND_URL = os.environ.get('FRONTEND_URL')
