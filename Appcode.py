from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(_name_)
CORS(app)

TRANSLATIONS = {
    "en": {
        "pest_risk": "Pest risk",
        "climate_sensitivity": "Climate sensitivity",
        "ensure_irrigation": "Ensure proper irrigation.",
        "great_conditions": "Great conditions for growth!",
        "rotation_penalty": "Reduced score due to recent rotation of this crop",
        "primary": "Primary Crop",
        "backup": "Backup Crop",
        "sustainable": "Most Sustainable Crop"
    },
    "hi": {
        "pest_risk": "कीट का खतरा",
        "climate_sensitivity": "जलवायु संवेदनशीलता",
        "ensure_irrigation": "सुनिश्चित करें कि सिंचाई सही हो।",
        "great_conditions": "विकास के लिए बेहतरीन स्थिति!",
        "rotation_penalty": "हाल ही में यह फसल उगाई गई है, इस कारण स्कोर कम किया गया",
        "primary": "मुख्य फ़सल",
        "backup": "बैकअप फ़सल",
        "sustainable": "सबसे स्थायी फ़सल"
    },
    "ta": {
        "pest_risk": "பூச்சி ஆபத்து",
        "climate_sensitivity": "காலநிலை உணர்வு",
        "ensure_irrigation": "சரி நீர்ப்பாசனம் உறுதி செய்க.",
        "great_conditions": "வளர்ச்சிக்கு சிறந்த சூழல்!",
        "rotation_penalty": "சமீபத்தில் இது பயிரிடப்பட்டது, ஆகையால் மதிப்பெண் குறைக்கப்பட்டது",
        "primary": "முதன்மை பயிர்",
        "backup": "மறுஉதவிப் பயிர்",
        "sustainable": "மிகவும் நிலைத்த பண்புடைய பயிர்"
    },
    "te": {
        "pest_risk": "పీటలు ప్రమాదం",
        "climate_sensitivity": "వాతావరణ సున్నితత్వం",
        "ensure_irrigation": "సరైన సాగు నీటిని అందించండి.",
        "great_conditions": "వృద్ధికి మంచి పరిస్థితులు!",
        "rotation_penalty": "ఇటీవల ఈ పంట పెరిగింది కాబట్టి స్కోర్ తగ్గింది",
        "primary": "ప్రధాన పంట",
        "backup": "మరుసటి పంట",
        "sustainable": "అత్యంత సుస్థిర పంట"
    },
    "mr": {
        "pest_risk": "किडीचा धोका",
        "climate_sensitivity": "हवामान संवेदनशीलता",
        "ensure_irrigation": "योग्य सिंचन सुनिश्चित करा.",
        "great_conditions": "वाढीसाठी उत्कृष्ट परिस्थिती!",
        "rotation_penalty": "या पीकाचा अलीकडेच वापर केल्याने गुण कमी झाले",
        "primary": "प्राथमिक पीक",
        "backup": "बॅकअप पीक",
        "sustainable": "सर्वाधिक शाश्वत पीक"
    },
    "kn": {
        "pest_risk": "ಪದರಕೆಂತು ಅಪಾಯ",
        "climate_sensitivity": "ಹವಾಮಾನ ಸ್ಮರಣೆ",
        "ensure_irrigation": "ಸರಿಯಾದ ನೀರಾವರಿ ಖಚಿತಪಡಿಸಿ.",
        "great_conditions": "ಬೆಳೆಗಾಗಿ ಉತ್ತಮ ಪರಿಸ್ಥಿತಿ!",
        "rotation_penalty": "ಈ ಬೆಳೆ ಇತ್ತೀಚೆಗೆ ಬೆಳೆದಿದ್ದರಿಂದ ಅಂಕ ಕಡಿಮೆಯಾಗಿದೆ",
        "primary": "ಪ್ರಾಥಮಿಕ ಬೆಳೆ",
        "backup": "ಬ್ಯಾಕಪ್ ಬೆಳೆ",
        "sustainable": "ಅತ್ಯಂತ ಸ್ಥಿರ ಬೆಳೆ"
    },
    "pa": {
        "pest_risk": "ਕੀੜੇ ਦਾ ਖ਼ਤਰਾ",
        "climate_sensitivity": "ਮੌਸਮ ਸੰਵੇਦਨਸ਼ੀਲਤਾ",
        "ensure_irrigation": "ਸੋਚ ਸਮਝ ਕੇ ਸਿੰਚਾਈ ਕਰੋ।",
        "great_conditions": "ਵਧੀਆ ਬੜ੍ਹਤ ਲਈ ਹਾਲਾਤ!",
        "rotation_penalty": "ਇਹ ਫਸਲ ਹਾਲ ਹੀ ਵਿੱਚ ਵਧੀ ਹੈ, ਇਸ ਲਈ ਸਕੋਰ ਘਟਾਇਆ ਗਿਆ",
        "primary": "ਮੁੱਖ ਫਸਲ",
        "backup": "ਬੈਕਅੱਪ ਫਸਲ",
        "sustainable": "ਸਭ ਤੋਂ ਟਿਕਾਉ ਫਸਲ"
    },
}

CROPS = [
    {"crop": "Rice", "pH_range": (5.5, 7.5), "moisture": (0.6, 1.0), "yield": 2500, "profit_per_kg": 8, "sustainability": 80},
    {"crop": "Wheat", "pH_range": (6.0, 7.5), "moisture": (0.4, 0.8), "yield": 2000, "profit_per_kg": 12, "sustainability": 100},
    {"crop": "Sugarcane", "pH_range": (6.0, 7.5), "moisture": (0.7, 1.0), "yield": 3400, "profit_per_kg": 17.6, "sustainability": 70},
    {"crop": "Maize", "pH_range": (5.5, 7.0), "moisture": (0.4, 0.7), "yield": 2200, "profit_per_kg": 8.2, "sustainability": 85},
]

FARMSETU_API_URL = "https://api.farmsetu.co/api/v1/mandi-prices"

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    soil_pH = data.get("soil_pH", 6.5)
    moisture = data.get("moisture", 0.6)
    rainfall = data.get("rainfall", "medium")
    temperature = data.get("temperature", 28)
    farm_size = data.get("farm_size", 2)
    priority = data.get("priority", "balanced")
    user_yield = data.get("user_yield")
    language = data.get("language", "en")
    past_crops = data.get("past_crops", [])

    tr = TRANSLATIONS.get(language, TRANSLATIONS["en"])

    try:
        response = requests.get(FARMSETU_API_URL, timeout=5)
        response.raise_for_status()
        mandi_data = response.json()
        price_map = {item["commodity"]: float(item["modal_price"]) for item in mandi_data["data"]}
    except Exception as e:
        print(f"Error fetching FarmSetu API data: {e}")
        price_map = {crop["crop"]: crop["profit_per_kg"] for crop in CROPS}

    recommendations = []
    for crop in CROPS:
        ph_ok = crop["pH_range"][0] <= soil_pH <= crop["pH_range"][1]
        moisture_ok = crop["moisture"][0] <= moisture <= crop["moisture"][1]
        score = 0
        if ph_ok:
            score += 0.5
        if moisture_ok:
            score += 0.5

        penalty = 0
        penalty_reason = ""
        if crop["crop"] in past_crops:
            penalty = 0.3
            penalty_reason = tr["rotation_penalty"]

        score = max(score - penalty, 0)

        recommended_yield = user_yield if user_yield is not None else crop["yield"] * farm_size
        price = price_map.get(crop["crop"], crop["profit_per_kg"])
        profit = recommended_yield * price

        # Adjust profit based on priority
        if priority == "profit":
            adj_profit = profit * 1.1
        elif priority == "sustainability":
            adj_profit = profit * (crop["sustainability"] / 100)
        else:
            adj_profit = profit * ((crop["sustainability"] + 100) / 200)

        risks = []
        if score < 1:
            risks = [tr["pest_risk"], tr["climate_sensitivity"]]
        if penalty_reason:
            risks.append(penalty_reason)

        advice = tr["ensure_irrigation"] if moisture < 0.5 else tr["great_conditions"]

        recommendations.append({
            "crop": crop["crop"],
            "score": round(score, 2),
            "yield": recommended_yield,
            "profit": int(adj_profit),
            "price_per_kg": price,
            "sustainability": crop["sustainability"],
            "risks": risks,
            "advice": advice
        })

    recommendations = sorted(recommendations, key=lambda x: (-x["score"], -x["profit"]))

    return jsonify({
        "recommendations": recommendations,
        tr["primary"]: recommendations[0]["crop"] if recommendations else None,
        tr["backup"]: recommendations[1]["crop"] if len(recommendations) > 1 else None,
        tr["sustainable"]: max(recommendations, key=lambda x: x["sustainability"])["crop"] if recommendations else None
    })

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000, debug=True)
