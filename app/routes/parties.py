from flask import Blueprint, request, jsonify
from app.models.parties import get_parties_data
from app.schemas.schemas import format_parties_response

part_bp = Blueprint('parties', __name__)


@part_bp.route('/parties', methods=['GET'])
def parties():
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"erreur": "Les paramètres 'limit' et 'offset' doivent être des entiers."}), 400

    tri = request.args.get('tri', 'date').lower()
    ordre = request.args.get('ordre', 'asc').lower()

    colonnes_tri_autorisees = {'date': 'p.debut', 'attente': 'p.attente_secondes'}
    if tri not in colonnes_tri_autorisees:
        return jsonify({
                           "erreur": f"Colonne de tri inconnue. Valeurs acceptées : {', '.join(colonnes_tri_autorisees.keys())}"}), 400
    if ordre not in ['asc', 'desc']:
        return jsonify({"erreur": "Ordre inconnu. Valeurs acceptées : asc, desc"}), 400

    filtres = {}
    if request.args.get('annee'): filtres['annee'] = request.args.get('annee')
    if request.args.get('serveur'): filtres['serveur'] = request.args.get('serveur')
    if request.args.get('jeu'): filtres['jeu'] = request.args.get('jeu')
    if request.args.get('file'): filtres['file'] = request.args.get('file')

    data, total = get_parties_data(limit, offset, colonnes_tri_autorisees[tri], ordre, filtres)
    response = format_parties_response(data, total, limit, offset)

    return jsonify(response)