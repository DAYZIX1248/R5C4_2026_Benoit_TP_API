import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Définition du chemin absolu pour pointer vers le sous-dossier contenant la DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'R5C54_2026_SUJET', 'parties.db')


def get_db_connection():
    """Établit la connexion à la base de données."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# ROUTES DES RÉFÉRENTIELS
# ==========================================

@app.route('/api/v1/jeux', methods=['GET'])
def get_jeux():
    """Renvoie la liste de tous les jeux."""
    conn = get_db_connection()
    jeux = conn.execute('SELECT id, nom FROM jeux').fetchall()
    conn.close()
    return jsonify([dict(j) for j in jeux])


@app.route('/api/v1/serveurs', methods=['GET'])
def get_serveurs():
    """Renvoie la liste de tous les serveurs."""
    conn = get_db_connection()
    serveurs = conn.execute('SELECT id, code, nom, region FROM serveurs').fetchall()
    conn.close()
    return jsonify([dict(s) for s in serveurs])


@app.route('/api/v1/files', methods=['GET'])
def get_files():
    """Renvoie la liste des files d'attente avec le jeu associé."""
    conn = get_db_connection()
    files = conn.execute('''
        SELECT f.id, f.nom as file_nom, j.nom as jeu_nom 
        FROM files f 
        JOIN jeux j ON f.jeu_id = j.id
    ''').fetchall()
    conn.close()
    return jsonify([dict(f) for f in files])


# ==========================================
# ROUTE PRINCIPALE : PARTIES
# ==========================================

@app.route('/api/v1/parties', methods=['GET'])
def get_parties():
    """Consulte les parties avec pagination, filtres et tri."""
    # 1. Validation des paramètres de pagination
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"erreur": "Les paramètres 'limit' et 'offset' doivent être des entiers."}), 400

    # 2. Validation des paramètres de tri et d'ordre
    tri = request.args.get('tri', 'date').lower()
    ordre = request.args.get('ordre', 'asc').lower()

    colonnes_tri_autorisees = {'date': 'p.debut', 'attente': 'p.attente_secondes'}
    if tri not in colonnes_tri_autorisees:
        return jsonify({
            "erreur": f"Colonne de tri inconnue. Valeurs acceptées : {', '.join(colonnes_tri_autorisees.keys())}"
        }), 400

    if ordre not in ['asc', 'desc']:
        return jsonify({"erreur": "Ordre inconnu. Valeurs acceptées : asc, desc"}), 400

    # 3. Construction dynamique de la requête et des filtres
    query_base = '''
        FROM parties p
        JOIN serveurs s ON p.serveur_id = s.id
        JOIN files f ON p.file_id = f.id
        JOIN jeux j ON f.jeu_id = j.id
        WHERE 1=1
    '''
    filters = []
    params = []

    # Filtre: Année
    annee = request.args.get('annee')
    if annee:
        filters.append("strftime('%Y', p.debut) = ?")
        params.append(annee)

    # Filtre: Serveur
    serveur = request.args.get('serveur')
    if serveur:
        filters.append("s.code = ?")
        params.append(serveur)

    # Filtre: Jeu
    jeu = request.args.get('jeu')
    if jeu:
        filters.append("j.nom = ?")
        params.append(jeu)

    # Filtre: File
    file = request.args.get('file')
    if file:
        filters.append("f.nom = ?")
        params.append(file)

    # Ajout des filtres à la requête de base
    if filters:
        query_base += " AND " + " AND ".join(filters)

    conn = get_db_connection()

    try:
        # 4. Calcul du total global (sans pagination)
        count_query = f"SELECT COUNT(p.id) {query_base}"
        total = conn.execute(count_query, params).fetchone()[0]

        # 5. Récupération des données triées et paginées
        data_query = f'''
            SELECT p.id, j.nom as jeu, s.code as serveur, f.nom as file, 
                   p.debut, p.attente_secondes, p.duree_minutes
            {query_base}
            ORDER BY {colonnes_tri_autorisees[tri]} {ordre.upper()}
            LIMIT ? OFFSET ?
        '''

        data_params = params + [limit, offset]
        parties = conn.execute(data_query, data_params).fetchall()

    finally:
        conn.close()

    # 6. Renvoi de la réponse formatée
    return jsonify({
        "data": [dict(p) for p in parties],
        "total": total,
        "limit": limit,
        "offset": offset
    })


if __name__ == '__main__':
    # Le serveur Flask se lance sur le port 5000
    app.run(debug=True, port=5000)