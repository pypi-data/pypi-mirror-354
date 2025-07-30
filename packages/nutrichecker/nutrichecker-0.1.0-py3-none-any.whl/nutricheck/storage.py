# nutricheck/storage.py
"""
Module storage.py:
Bertanggung jawab untuk menyimpan dan mengambil histori analisis
ke/dari database lokal menggunakan TinyDB.
"""

import os
import json
from tinydb import TinyDB, Query
from loguru import logger

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "nutricheck_db.json")
db = TinyDB(DB_PATH)

def save_analysis(analysis: dict) -> None:
    """
    Menyimpan hasil analisis ke TinyDB.
    """
    db.insert(analysis)
    logger.info("Analisis telah disimpan ke database.")

def load_all_analyses() -> list:
    """
    Mengambil semua hasil analisis yang disimpan.
    """
    return db.all()

def search_analysis(keyword: str) -> list:
    """
    Cari histori berdasarkan keyword di makanan yang dikonsumsi.
    """
    Analysis = Query()
    results = db.search(Analysis.foods.any([keyword]))
    logger.debug(f"Ditemukan {len(results)} hasil untuk keyword '{keyword}'")
    return results
