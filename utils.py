# rag_accuracy_evaluator/utils.py
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text: str, api_key: str, base_url: str, model: str = "text-embedding-3-small"):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": text.replace("\n", " ")
    }
    response = requests.post(f"{base_url}/embeddings", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def calculate_cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1).reshape(1, -1)
    vec2 = np.array(vec2).reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]
