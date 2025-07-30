# nutricheck/config.py
"""
Module config.py:
Menyimpan konfigurasi dan API key menggunakan python-decouple.
"""

from decouple import config

# Endpoint API untuk pengambilan data nutrisi; gunakan API publik atau dummy
API_ENDPOINT = config("API_ENDPOINT", default="https://api.example.com/nutrition")

# API KEY untuk otentikasi ke API
API_KEY = config("API_KEY", default="dummy_api_key")

# Konfigurasi lainnya jika diperlukan
DEBUG_MODE = config("DEBUG_MODE", default=True, cast=bool)

if DEBUG_MODE:
    print("NutriCheck sedang berjalan dalam mode DEBUG.")
