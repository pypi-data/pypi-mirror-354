# nutricheck/utils.py
"""
Module utils.py:
Berisi fungsi-fungsi utilitas seperti perhitungan BMI, kebutuhan kalori harian,
dan konversi satuan.
"""

def calculate_bmi(weight: float, height: float) -> float:
    """
    Menghitung BMI (Body Mass Index).
    Parameter:
        weight (float): Berat badan dalam kilogram.
        height (float): Tinggi badan dalam centimeter.
    Return:
        float: BMI.
    """
    height_m = height / 100.0
    if height_m == 0:
        return 0
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def daily_nutrition_needs(user_profile: dict) -> dict:
    """
    Menghitung kebutuhan nutrisi harian berdasarkan profil pengguna.
    
    Parameter:
        user_profile (dict): {'age': int, 'weight': float, 'height': float, 'activity_level': str}
    Return:
        dict: Kebutuhan kalori, protein, lemak, karbohidrat, dan serat.
    """
    age = user_profile.get("age", 30)
    weight = user_profile.get("weight", 70)
    height = user_profile.get("height", 170)
    activity_level = user_profile.get("activity_level", "moderate")

    # Perhitungan kebutuhan energi basal (BMR) menggunakan rumus Mifflin-St Jeor
    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # untuk pria, bisa disesuaikan untuk wanita

    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    factor = activity_factors.get(activity_level.lower(), 1.55)
    calories_needed = int(bmr * factor)

    # Distribusi makronutrien: perkiraan sederhana
    protein = round(weight * 1.2, 2)         # gram per hari
    fat = round((calories_needed * 0.25) / 9, 2)   # gram per hari
    carbs = round((calories_needed - (protein * 4 + fat * 9)) / 4, 2)
    fiber = 25 + (age // 10)  # contoh sederhana

    return {
        "calories": calories_needed,
        "protein": protein,
        "fat": fat,
        "carbs": carbs,
        "fiber": fiber
    }

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Fungsi dummy untuk konversi satuan (belum diimplementasi penuh).
    """
    # Implementasi konversi sederhana bisa ditambahkan di sini.
    return value

# Fungsi tambahan sebagai placeholder untuk validasi data masukan
def validate_profile(profile: dict) -> bool:
    """
    Validasi apakah profil pengguna memiliki semua informasi penting.
    """
    required_keys = ["age", "weight", "height", "activity_level"]
    for key in required_keys:
        if key not in profile:
            return False
    return True
