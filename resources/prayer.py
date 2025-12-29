from flask import Blueprint
from datetime import date
from adhan import PrayerTimes, CalculationMethod, Madhab
import pytz

prayer_bp = Blueprint("prayer", __name__)

TIMEZONE = pytz.timezone("Africa/Tunis")

DEFAULT_LOCATION = {
    "city": "tunis",
    "lat": 36.8065,
    "lon": 10.1815
}

# ✅ ALL your cities preserved
CITIES = {
    "tunis": (36.8065, 10.1815),
    "ariana": (36.8665, 10.1647),
    "ben_arous": (36.7435, 10.2310),
    "manouba": (36.8080, 10.0972),

    "nabeul": (36.4513, 10.7350),
    "zaghouan": (36.4029, 10.1429),

    "bizerte": (37.2746, 9.8739),
    "beja": (36.7333, 9.1833),
    "jendouba": (36.5011, 8.7802),
    "kef": (36.1675, 8.7047),
    "siliana": (36.0848, 9.3708),

    "kairouan": (35.6781, 10.0963),
    "kasserine": (35.1676, 8.8365),
    "sidi_bouzid": (35.0382, 9.4849),

    "sousse": (35.8256, 10.6084),
    "monastir": (35.7770, 10.8262),
    "mahdia": (35.5047, 11.0622),

    "sfax": (34.7406, 10.7603),

    "gabes": (33.8815, 10.0982),
    "medenine": (33.3549, 10.5055),
    "tataouine": (32.9297, 10.4518),

    "gafsa": (34.4250, 8.7842),
    "tozeur": (33.9197, 8.1335),
    "djerba": (33.8076, 10.8451),
    "kebili": (33.7077, 8.9711)
}

params = CalculationMethod.MUSLIM_WORLD_LEAGUE.parameters
params.madhab = Madhab.SHAFI


def calculate_prayer_times(lat, lon):
    prayers = PrayerTimes(
        coordinates=(lat, lon),
        date=date.today(),
        calculation_parameters=params
    )

    return {
        "fajr": prayers.fajr.astimezone(TIMEZONE).strftime("%H:%M"),
        "dhuhr": prayers.dhuhr.astimezone(TIMEZONE).strftime("%H:%M"),
        "asr": prayers.asr.astimezone(TIMEZONE).strftime("%H:%M"),
        "maghrib": prayers.maghrib.astimezone(TIMEZONE).strftime("%H:%M"),
        "isha": prayers.isha.astimezone(TIMEZONE).strftime("%H:%M")
    }


# 🔹 GET /prayer
@prayer_bp.route("/", methods=["GET"])
def get_all_prayers():
    timings = calculate_prayer_times(
        DEFAULT_LOCATION["lat"],
        DEFAULT_LOCATION["lon"]
    )

    return {
        "location": DEFAULT_LOCATION["city"],
        "prayers": timings
    }, 200


# 🔹 GET /prayer/city/tunis
@prayer_bp.route("/city/<string:city>", methods=["GET"])
def get_prayers_by_city(city):
    city = city.lower()

    if city not in CITIES:
        return {"error": "City not supported"}, 404

    lat, lon = CITIES[city]
    timings = calculate_prayer_times(lat, lon)

    return {
        "location": city,
        "prayers": timings
    }, 200


# 🔹 GET /prayer/name/fajr
@prayer_bp.route("/name/<string:prayer_name>", methods=["GET"])
def get_single_prayer(prayer_name):
    prayer_name = prayer_name.lower()

    timings = calculate_prayer_times(
        DEFAULT_LOCATION["lat"],
        DEFAULT_LOCATION["lon"]
    )

    if prayer_name not in timings:
        return {"error": "Invalid prayer name"}, 404

    return {
        "prayer": prayer_name,
        "time": timings[prayer_name]
    }, 200
