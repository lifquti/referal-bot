import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
import os

cwd = Path().cwd()




ROUTE_URL = os.getenv('ROUTE_URL')
POLLING = os.getenv('POLLING')
ADMINS_ID = json.loads(os.getenv('ADMINS_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
is_ssl = os.getenv('SSL')

NOTIFY_USERS = json.loads(os.getenv('NOTIFY_USERS'))

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f'{cwd.name}'
WEBHOOK_URL = f"{WEBHOOK_HOST}/{WEBHOOK_PATH}/"

BOT_SERVER = {
    'host': os.getenv('BOT_SERVER_HOST'),
    'port': os.getenv('BOT_SERVER_PORT')
}

REDIS = {
    'db': 2,
    'prefix': cwd.name
}

BASE_DIR = Path(__file__).parent
I18N_DOMAIN = f"{Path(__file__).parent.parent.name}_lang"
print(f'\033[93mNAME FOR I18N FILE IS {Path(__file__).parent.parent.name}_lang \033[0m')
LOCALES_DIR = BASE_DIR / 'locales'


MYSQL = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'db': os.getenv('MYSQL_DB_NAME'),
    'port': int(os.getenv('MYSQL_PORT'))
    # 'unix_socket': '/var/run/mysqld/mysqld.sock'
}

