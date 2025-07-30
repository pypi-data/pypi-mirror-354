# nutricheck/fetch.py
"""
Module fetch.py:
Berisi fungsi untuk mengambil data gizi dari API eksternal atau data dummy.
"""

import requests
from loguru import logger
from .config import API_ENDPOINT, API_KEY
from random import randint

def fetch_nutrition_data(food_item: str) -> dict:
    """
    Mengambil data nutrisi dari API untuk makanan yang diberikan.
    Jika API gagal, akan mengembalikan data dummy.
    
    Parameter:
        food_item (str): Nama makanan yang dicari.
    Return:
        dict: Data nutrisi (kalori, protein, fat, carbs, fiber).
    """
    logger.debug(f"Mencari data nutrisi untuk {food_item}")
    url = f"{API_ENDPOINT}?food={food_item}&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Data API untuk {food_item}: {data}")
        return {
            "calories": data.get("calories", 0),
            "protein": data.get("protein", 0),
            "fat": data.get("fat", 0),
            "carbs": data.get("carbs", 0),
            "fiber": data.get("fiber", 0)
        }
    except Exception as e:
        logger.warning(f"API gagal untuk {food_item}: {e}. Menggunakan data dummy.")
        # Data dummy jika API gagal
        return {
            "calories": randint(50, 200),
            "protein": randint(1, 20),
            "fat": randint(1, 15),
            "carbs": randint(10, 40),
            "fiber": randint(1, 10)
        }

# Fungsi tambahan untuk mendukung fetch jika diperlukan di masa depan
def fetch_bulk_nutrition_data(food_items: list) -> dict:
    """
    Mengambil data untuk sejumlah makanan sekaligus.
    Return:
        dict: Mapping food_item -> nutrition data.
    """
    results = {}
    for food in food_items:
        results[food] = fetch_nutrition_data(food)
    return results
