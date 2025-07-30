from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).parent.parent
ANKIPAN_ROOT = PROJECT_ROOT / 'ankipan'
HTML_TEMPLATE_DIR = ANKIPAN_ROOT / 'html_templates'
ANKI_COLLECTIONS_DIR = PROJECT_ROOT / 'anki_collections'

DATA_DIR = PROJECT_ROOT / '.data'
USER_DATA_FILE = PROJECT_ROOT / '.user_data.yaml'
if USER_DATA_FILE.exists():
    with open(USER_DATA_FILE, 'r') as f:
        USER_DATA = yaml.safe_load(f)
else:
    USER_DATA = {}

# TODO: run server remotely and change this
ANKIPAN_DB_ADDR = 'http://localhost:5000'

from .util import *
from .anki_manager import AnkiManager
from .reader import Reader, File
from .scraper import Scraper, CardSection
from .card import Card
from .deck import Deck
from .collection import Collection
