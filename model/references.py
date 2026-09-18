from .database import get_db_connection

def get_all_jeux():
    conn = get_db_connection()
    jeux = conn.execute('SELECT id, nom FROM jeux').fetchall()
    conn.close()
    return [dict(j) for j in jeux]

def get_all_serveurs():
    conn = get_db_connection()
    serveurs = conn.execute('SELECT id, code, nom, region FROM serveurs').fetchall()
    conn.close()
    return [dict(s) for s in serveurs]

def get_all_files():
    conn = get_db_connection()
    files = conn.execute('''
        SELECT f.id, f.nom as file_nom, j.nom as jeu_nom 
        FROM files f 
        JOIN jeux j ON f.jeu_id = j.id
    ''').fetchall()
    conn.close()
    return [dict(f) for f in files]