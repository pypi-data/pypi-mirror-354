# nutricheck/recommender.py
"""
Module recommender.py:
Menggunakan metode similarity sederhana untuk memberikan rekomendasi makanan
pengganti yang lebih sehat berdasarkan daftar makanan yang dikonsumsi.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from loguru import logger

# Data dummy database makanan dan nilai nutrisi (normalisasi)
HEALTHY_FOOD_DB = {
    "broccoli": np.array([55, 3.7, 0.6, 11, 2.6]),
    "spinach": np.array([23, 2.9, 0.4, 3.6, 2.2]),
    "salmon": np.array([208, 20, 13, 0, 0]),
    "quinoa": np.array([120, 4.4, 1.9, 21.3, 2.8]),
    "blueberries": np.array([57, 0.7, 0.3, 14.5, 2.4])
}

def compute_similarity(nutrition_vector: np.array, candidate_vector: np.array) -> float:
    """
    Menghitung similarity antara dua vector nutrisi menggunakan cosine similarity.
    """
    similarity = cosine_similarity([nutrition_vector], [candidate_vector])[0][0]
    return similarity

def recommend_healthier_alternatives(food_items: list) -> list:
    """
    Memberikan rekomendasi makanan sehat berdasarkan input daftar makanan.
    Implementasi:
        1. Hitung rata-rata nutrisi dari daftar makanan.
        2. Bandingkan dengan database makanan sehat.
        3. Rekomendasikan makanan dengan similarity tertinggi.
    """
    logger.debug("Mulai rekomendasi makanan sehat.")
    # Dummy: hitung rata-rata dari data dummy setiap makanan
    dummy_values = {
        "apple": np.array([95, 0.5, 0.3, 25, 4.4]),
        "banana": np.array([105, 1.3, 0.4, 27, 3.1]),
        "chicken breast": np.array([165, 31, 3.6, 0, 0])
    }
    vectors = []
    for item in food_items:
        vectors.append(dummy_values.get(item, np.array([50, 2, 1, 12, 2])))
    avg_vector = np.mean(vectors, axis=0)
    logger.debug(f"Rata-rata vector nutrisi: {avg_vector}")

    # Cari kandidat dengan cosine similarity tertinggi
    recommendations = []
    max_similarity = 0
    best_candidate = None
    for food, vector in HEALTHY_FOOD_DB.items():
        sim = compute_similarity(avg_vector, vector)
        logger.debug(f"Similarity dengan {food}: {sim:.2f}")
        if sim > max_similarity:
            max_similarity = sim
            best_candidate = food

    if best_candidate:
        recommendations.append(best_candidate)
    else:
        recommendations.append("Tidak ada rekomendasi yang tersedia")

    return recommendations

# Fungsi tambahan untuk melakukan evaluasi rekomendasi jika diperlukan
def evaluate_recommendations(food_items: list, recommendations: list) -> dict:
    """
    Fungsi dummy untuk evaluasi hasil rekomendasi.
    Return:
        dict: evaluasi hasil rekomendasi.
    """
    return {"confidence": 0.85, "notes": "Rekomendasi dihitung secara sederhana."}
