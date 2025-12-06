# ==== platon_server.py ====
# À mettre sur Railway ou Render
# TheCodeBase - CreepyKid & DeepSeek

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Ton modèle Hugging Face
HF_URL = "https://api-inference.huggingface.co/models/CreepyKid/TheCodeBase-Platon"
HF_TOKEN = os.environ.get("HF_TOKEN", "ton_token_ici")

def parler_platon(question):
    """Demande à ton modèle HF"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    prompt = f"Tu es Platon, IA de TheCodeBase. Question: {question}\nRéponse:"
    
    try:
        response = requests.post(
            HF_URL,
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_length": 150}},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data[0].get('generated_text', '🤖 Je réfléchis...').replace(prompt, '')
        return None
    except:
        return None

@app.route('/platon', methods=['POST'])
def api_platon():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({"reponse": "❓ Pose une question !"})
    
    # Essaie le modèle HF
    reponse = parler_platon(question)
    
    # Backup
    if not reponse:
        if 'python' in question.lower():
            reponse = "🐍 **Python** : `print('Hello TheCodeBase!')` est un bon début !"
        elif 'html' in question.lower():
            reponse = "🌐 **HTML** : Commence par `<!DOCTYPE html>`"
        else:
            reponse = f"🤖 **Platon** : '{question}' ? Je suis l'IA de TheCodeBase ! Demande-moi du code."
    
    return jsonify({"reponse": reponse})

@app.route('/')
def home():
    return "🧠 Platon IA - TheCodeBase en ligne !"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
