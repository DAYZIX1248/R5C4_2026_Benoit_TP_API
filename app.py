from flask import Flask

# Import des contrôleurs (Blueprints)
from controllers.ref_controller import ref_bp
from controllers.part_controller import part_bp

app = Flask(__name__)

# Enregistrement des routes avec leur préfixe
app.register_blueprint(ref_bp, url_prefix='/api/v1')
app.register_blueprint(part_bp, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True, port=5000)