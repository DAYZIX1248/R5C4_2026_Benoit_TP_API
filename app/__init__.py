from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import des routes (Blueprints)
    from app.routes.references import ref_bp
    from app.routes.parties import part_bp

    # Enregistrement avec le préfixe de versionnage global
    app.register_blueprint(ref_bp, url_prefix='/api/v1')
    app.register_blueprint(part_bp, url_prefix='/api/v1')

    return app