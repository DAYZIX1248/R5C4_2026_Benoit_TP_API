from .database import get_db_connection


def get_parties_data(limit, offset, tri_colonne, ordre, filtres):
    query_base = '''
        FROM parties p
        JOIN serveurs s ON p.serveur_id = s.id
        JOIN files f ON p.file_id = f.id
        JOIN jeux j ON f.jeu_id = j.id
        WHERE 1=1
    '''

    conditions = []
    params = []

    if 'annee' in filtres:
        conditions.append("strftime('%Y', p.debut) = ?")
        params.append(filtres['annee'])
    if 'serveur' in filtres:
        conditions.append("s.code = ?")
        params.append(filtres['serveur'])
    if 'jeu' in filtres:
        conditions.append("j.nom = ?")
        params.append(filtres['jeu'])
    if 'file' in filtres:
        conditions.append("f.nom = ?")
        params.append(filtres['file'])

    if conditions:
        query_base += " AND " + " AND ".join(conditions)

    conn = get_db_connection()
    try:
        # Calcul du total
        total = conn.execute(f"SELECT COUNT(p.id) {query_base}", params).fetchone()[0]

        # Récupération des données
        data_query = f'''
            SELECT p.id, j.nom as jeu, s.code as serveur, f.nom as file, 
                   p.debut, p.attente_secondes, p.duree_minutes
            {query_base}
            ORDER BY {tri_colonne} {ordre.upper()}
            LIMIT ? OFFSET ?
        '''
        data_params = params + [limit, offset]
        parties = conn.execute(data_query, data_params).fetchall()

        return [dict(p) for p in parties], total
    finally:
        conn.close()