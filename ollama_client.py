import requests

OLLAMA_API_URL = "http://localhost:11434/api"

def query_ollama(prompt, model="llama3.2"):
    """Envoie une requête au modèle Ollama et renvoie la réponse."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(f"{OLLAMA_API_URL}/chat", json=payload)

    if response.status_code == 200:
        return response.json().get("message", "Aucune réponse trouvée.")
    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")
