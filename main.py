from flask import Flask
from calendario import app1  # Importa il blueprint dal file bp1.py

# from bp2 import bp2  # Importa il blueprint dal file bp2.py

app = Flask(__name__)

# Registrazione dei Blueprints
app.register_blueprint(app1)
# app.register_blueprint(bp2)

if __name__ == "__main__":
    app.run(port=5000)
