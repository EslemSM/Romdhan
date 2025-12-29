from flask import Blueprint
from datetime import datetime, timedelta
from models.sunnah_prayer import SunnahPrayer
from resources.prayer import calculate_prayer_times, DEFAULT_LOCATION

sunnah_bp = Blueprint("sunnah_prayer", __name__)


def calculate_sunnah_time(name, timings, sunrise_time=None):
    
    if name == "duha":
        if sunrise_time:
            return f"After Sunrise ({sunrise_time})"
        return "After Sunrise (approximately 15-20 minutes after Fajr)"

    if name == "taraweeh":
        isha_time = timings.get('isha')
        if isha_time:
            return f"After Isha ({isha_time})"
        return "After Isha"

    if name == "tahajjud":
        fajr_time = timings.get('fajr')
        if fajr_time:
            return f"Last third of the night (before Fajr at {fajr_time})"
        return "Last third of the night (before Fajr)"

    return None


@sunnah_bp.route("/", methods=["GET"])
def get_all_sunnah_prayers():
    sunnah_prayers = SunnahPrayer.query.all()
    timings = calculate_prayer_times(
        DEFAULT_LOCATION["lat"],
        DEFAULT_LOCATION["lon"]
    )

    # Calculate approximate sunrise time (for duha)
    # Sunrise is approximately 15-20 minutes after Fajr
    fajr_hour, fajr_min = timings.get('fajr', '00:00').split(':')
    fajr_dt = datetime.today().replace(hour=int(fajr_hour), minute=int(fajr_min))
    sunrise_dt = fajr_dt + timedelta(minutes=18)  # Approximate 18 minutes
    sunrise_time = sunrise_dt.strftime("%H:%M")

    result = []
    for sp in sunnah_prayers:
        result.append({
            "name": sp.name,
            "is_ramadhan_only": sp.is_ramadhan_only,
            "time": calculate_sunnah_time(sp.name, timings, sunrise_time)
        })

    return result, 200


@sunnah_bp.route("/<string:name>", methods=["GET"])
def get_sunnah_by_name(name):
    sp = SunnahPrayer.query.filter_by(name=name).first_or_404()
    timings = calculate_prayer_times(
        DEFAULT_LOCATION["lat"],
        DEFAULT_LOCATION["lon"]
    )

    # Calculate approximate sunrise time (for duha)
    fajr_hour, fajr_min = timings.get('fajr', '00:00').split(':')
    fajr_dt = datetime.today().replace(hour=int(fajr_hour), minute=int(fajr_min))
    sunrise_dt = fajr_dt + timedelta(minutes=18)  # Approximate 18 minutes
    sunrise_time = sunrise_dt.strftime("%H:%M")

    return {
        "name": sp.name,
        "is_ramadhan_only": sp.is_ramadhan_only,
        "time": calculate_sunnah_time(sp.name, timings, sunrise_time)
    }, 200
