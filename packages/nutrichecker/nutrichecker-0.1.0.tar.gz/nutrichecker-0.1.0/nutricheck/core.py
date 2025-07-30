# nutricheck/core.py
"""
Module core.py:
Berisi kelas utama NutritionAnalyzer yang mengorkestrasi alur analisis gizi,
pengambilan data, evaluasi, dan penyimpanan hasil analisis.
"""

from .fetch import fetch_nutrition_data
from .utils import calculate_bmi, daily_nutrition_needs
from .recommender import recommend_healthier_alternatives
from .storage import save_analysis
from loguru import logger

class NutritionAnalyzer:
    """
    NutritionAnalyzer melakukan analisis berdasarkan makanan yang diinputkan
    serta profil pengguna.
    """
    def __init__(self, user_profile: dict):
        """
        Inisialisasi dengan data profil pengguna.
        Parameter:
            user_profile (dict): {'age': int, 'weight': float, 'height': float, 'activity_level': str}
        """
        self.user_profile = user_profile
        self.analysis_result = {}

    def analyze(self, food_items: list) -> dict:
        """
        Melakukan analisis terhadap daftar makanan.
        Parameter:
            food_items (list): List nama makanan.
        Return:
            dict: Hasil analisis yang mencakup total nutrisi, kebutuhan, skor,
                  dan rekomendasi.
        """
        logger.info(f"Mulai analisis untuk: {food_items}")
        total_nutrition = {
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0,
            "fiber": 0
        }

        # Ambil data untuk setiap makanan
        for item in food_items:
            data = fetch_nutrition_data(item)
            logger.debug(f"Data untuk {item}: {data}")
            for key in total_nutrition.keys():
                total_nutrition[key] += data.get(key, 0)

        # Menghitung kebutuhan nutrisi harian dari profil pengguna
        needs = daily_nutrition_needs(self.user_profile)
        logger.debug(f"Kebutuhan nutrisi harian: {needs}")

        # Evaluasi skor analisis: semakin kecil selisih, semakin baik
        score = self.evaluate(total_nutrition, needs)
        logger.info(f"Skor evaluasi: {score:.2f}")

        # Buat rekomendasi makanan sehat jika perlu
        recommendations = recommend_healthier_alternatives(food_items)
        logger.info(f"Rekomendasi: {recommendations}")

        self.analysis_result = {
            "user": self.user_profile,
            "foods": food_items,
            "nutrition": total_nutrition,
            "needs": needs,
            "score": score,
            "recommendations": recommendations
        }

        # Simpan histori analisis ke storage lokal
        save_analysis(self.analysis_result)
        return self.analysis_result

    def evaluate(self, total: dict, needs: dict) -> float:
        """
        Evaluasi kesesuaian total nutrisi dengan kebutuhan harian.
        Menggunakan Mean Squared Error (MSE) sebagai dasar perhitungan.
        """
        try:
            from sklearn.metrics import mean_squared_error
        except ImportError:
            logger.error("scikit-learn diperlukan untuk evaluasi.")
            raise

        # Buat list numerik untuk perhitungan
        actual = [total.get(k, 0) for k in needs.keys()]
        expected = [needs.get(k, 0) for k in needs.keys()]
        mse = mean_squared_error(expected, actual)
        score = max(0, 100 - (mse ** 0.5 * 10))
        return score

# Blok eksekusi untuk debug jika dijalankan langsung
if __name__ == "__main__":
    profile = {"age": 30, "weight": 70, "height": 170, "activity_level": "moderate"}
    analyzer = NutritionAnalyzer(profile)
    results = analyzer.analyze(["apple", "banana", "chicken breast"])
    print("Hasil Analisis:", results)
