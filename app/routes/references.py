from flask import Blueprint, jsonify
from app.models.references import get_all_jeux, get_all_serveurs, get_all_files

ref_bp = Blueprint('references', __name__)

@ref_bp.route('/jeux', methods=['GET'])
def jeux():
    return jsonify(get_all_jeux())

@ref_bp.route('/serveurs', methods=['GET'])
def serveurs():
    return jsonify(get_all_serveurs())

@ref_bp.route('/files', methods=['GET'])
def files():
    return jsonify(get_all_files())