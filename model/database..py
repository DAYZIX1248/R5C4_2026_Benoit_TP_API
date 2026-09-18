import os
import sqlite3

# On remonte d'un dossier depuis 'models' pour trouver la racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'R5C54_2026_SUJET', 'parties.db')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn