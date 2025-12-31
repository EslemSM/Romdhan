import requests
from flask_smorest import Blueprint, abort

tafseer_bp = Blueprint("quran_tafsir", __name__, description = "Tafseer Quran")

BASE_URL_AYAH = "https://api.alquran.cloud/v1/ayah"  # For plain ayah text
BASE_URL_TAFSIR = "https://api.alquran.cloud/v1/ayah"  # For tafsir (with /ar.muyassar)

@tafseer_bp.route("/<int:surah>/<int:ayah>", methods=["GET"])
def get_tafsir(surah, ayah):
    try:
        # Step 1: Fetch the plain ayah text
        ayah_url = f"{BASE_URL_AYAH}/{surah}:{ayah}"
        ayah_response = requests.get(ayah_url)
        ayah_response.raise_for_status()
        ayah_data = ayah_response.json()["data"]
        ayah_text = ayah_data["text"]  # Plain Quran ayah

        # Step 2: Fetch the tafsir
        tafsir_url = f"{BASE_URL_TAFSIR}/{surah}:{ayah}/ar.muyassar"
        tafsir_response = requests.get(tafsir_url)
        tafsir_response.raise_for_status()
        tafsir_data = tafsir_response.json()["data"]
        tafsir_text = tafsir_data["text"]  # Tafsir explanation

        # Step 3: Return the combined response
        return {
            "surah": surah,
            "ayah": ayah,
            "ayah_text": ayah_text,  # Now the plain ayah
            "tafsir_text": tafsir_text,  # Now the tafsir
            "reference": "Tafsir Al-Muyassar"
        }, 200

    except requests.exceptions.RequestException as e:
        # Handle API errors (e.g., invalid surah/ayah, network issues)
        return {"error": f"API request failed: {str(e)}"}, 500
    except KeyError as e:
        # Handle missing data in API response
        return {"error": f"Invalid API response: missing key {str(e)}"}, 500
    except Exception as e:
        # General error handling
        return {"error": str(e)}, 500