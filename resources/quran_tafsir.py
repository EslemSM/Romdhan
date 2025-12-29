import requests
from flask import Blueprint

tafseer_bp = Blueprint("quran_tafsir", __name__)

BASE_URL = "https://api.alquran.cloud/v1/ayah"


@tafseer_bp.route("/<int:surah>/<int:ayah>", methods=["GET"])
def get_tafsir(surah, ayah):
    try:
        url = f"{BASE_URL}/{surah}:{ayah}/ar.muyassar"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()["data"]

        return {
            "surah": surah,
            "ayah": ayah,
            "ayah_text": data["text"],
            "tafsir_text": data["text"],
            "reference": "Tafsir Al-Muyassar"
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500
