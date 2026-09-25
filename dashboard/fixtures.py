# Filtres simulés
FILTRES_JEUX = [{"id": 1, "nom": "League of Legends"}, {"id": 2, "nom": "Valorant"}]
FILTRES_SERVEURS = [{"id": 1, "code": "EUW", "nom": "Europe West"}, {"id": 2, "code": "NA", "nom": "North America"}]
FILTRES_FILES = [{"id": 1, "file_nom": "Ranked Solo 5v5"}, {"id": 2, "file_nom": "ARAM"}]

# Données de la page 1 (Liste et Pagination)
PARTIES_DATA = {
    "data": [
        {"id": 1, "jeu": "League of Legends", "serveur": "EUW", "file": "Ranked Solo 5v5", "debut": "2024-01-01 12:00:00", "attente_secondes": 120, "duree_minutes": 35.5},
        {"id": 2, "jeu": "League of Legends", "serveur": "EUW", "file": "Ranked Solo 5v5", "debut": "2024-01-01 12:15:00", "attente_secondes": 45, "duree_minutes": 20.0},
        {"id": 3, "jeu": "Valorant", "serveur": "NA", "file": "Competitive", "debut": "2024-01-01 14:00:00", "attente_secondes": 80, "duree_minutes": 42.1},
    ],
    "total": 150,
    "limit": 3,
    "offset": 0
}

# Données de la page 2 (Indicateurs et YoY)
INDICATEURS_DATA = {
    "indicateurs": {
        "volume_parties": 150,
        "attente_moyenne_sec": 81.6,
        "attente_max_sec": 120
    },
    "comparaison_n_1": {
        "evolution_volume_pct": 5.2,
        "evolution_attente_pct": -12.4
    }
}