# NutriCheck

**NutriChecker** is a Python library designed to analyze the nutritional value of food items, evaluate them based on user-specific health profiles, and provide smarter recommendations for healthier eating. Ideal for nutritionists, health apps, or anyone who wants to improve their dietary decisions through intelligent data analysis.

---

## 🚀 Features

- 🔍 Fetch nutritional data for common foods (via API or fallback to dummy data)
- 🧠 Evaluate food intake against daily nutritional needs
- 🧮 Built-in BMI and BMR calculation
- 🗂️ Save historical analysis to JSON storage
- 🥗 Recommend healthier alternatives using cosine similarity
- 📊 Nutrition scoring (0–100)
- 🔧 Configurable user profiles: age, weight, height, activity level

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/nutricheck.git
cd nutrichecker
pip install -r requirements.txt

## Usage Example
     
from nutricheck.core import NutritionAnalyzer

user = {
    "age": 28,
    "weight": 65,
    "height": 170,
    "activity_level": "moderate"
}

analyzer = NutritionAnalyzer(user)
result = analyzer.analyze(["banana", "salmon", "quinoa"])

print("Score:", result["score"])
print("Total Nutrition:", result["nutrition"])
print("Recommendations:", result["recommendations"])

# Requirements
       pip install requests scikit-learn loguru numpy

# Question And Suggestions
       For questions, email: aeden6877@gmail.com 