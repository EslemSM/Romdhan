from flask import Blueprint
from datetime import datetime, timedelta, date
from models.sunnah_prayer import SunnahPrayer
from resources.prayer import calculate_prayer_times, DEFAULT_LOCATION

sunnah_bp = Blueprint("sunnah_prayer", __name__)

def calculate_sunnah_time(name, timings):
    try:
        # Parse prayer times into datetime objects (assuming today's date)
        today = date.today()
        fajr_str = timings.get('fajr', '00:00')
        dhuhr_str = timings.get('dhuhr', '00:00')
        maghrib_str = timings.get('maghrib', '00:00')
        isha_str = timings.get('isha', '00:00')

        fajr = datetime.combine(today, datetime.strptime(fajr_str, "%H:%M").time())
        dhuhr = datetime.combine(today, datetime.strptime(dhuhr_str, "%H:%M").time())
        maghrib = datetime.combine(today, datetime.strptime(maghrib_str, "%H:%M").time())
        isha = datetime.combine(today, datetime.strptime(isha_str, "%H:%M").time())

        # Approximate sunrise (Fajr + 18 min, as in your code)
        sunrise = fajr + timedelta(minutes=18)

        if name == "duha":
            duha_start = sunrise + timedelta(minutes=15)
            duha_end = dhuhr - timedelta(minutes=10)
            return f"{duha_start.strftime('%H:%M')}-{duha_end.strftime('%H:%M')}"

        if name == "taraweeh":
            taraweeh_start = isha + timedelta(minutes=10)
            # Fajr is the end (next day, but since it's the same day context, use today's Fajr)
            taraweeh_end = fajr
            return f"{taraweeh_start.strftime('%H:%M')}-{taraweeh_end.strftime('%H:%M')}"

        if name == "tahajjud":
            # Get Fajr for next day
            tomorrow = today + timedelta(days=1)
            next_day_timings = calculate_prayer_times(DEFAULT_LOCATION["lat"], DEFAULT_LOCATION["lon"])
            fajr_next_str = next_day_timings.get('fajr', '00:00')
            fajr_next = datetime.combine(tomorrow, datetime.strptime(fajr_next_str, "%H:%M").time())
            
            # Night duration = Fajr (next) - Maghrib
            night_duration = fajr_next - maghrib
            last_third_start = maghrib + (night_duration * 2 / 3)
            # Interval: Start to Fajr (next)
            return f"{last_third_start.strftime('%H:%M')}-{fajr_next.strftime('%H:%M')}"

        return None
    except Exception as e:
        # Fallback if parsing fails
        return "Time calculation error"

@sunnah_bp.route("/", methods=["GET"])
def get_all_sunnah_prayers():
    sunnah_prayers = SunnahPrayer.query.all()
    timings = calculate_prayer_times(
        DEFAULT_LOCATION["lat"],
        DEFAULT_LOCATION["lon"]
    )

    result = []
    for sp in sunnah_prayers:
        result.append({
            "name": sp.name,
            "is_ramadhan_only": sp.is_ramadhan_only,
            "time": calculate_sunnah_time(sp.name, timings)
        })

    return result, 200

@sunnah_bp.route("/<string:name>", methods=["GET"])
def get_sunnah_by_name(name):
    sp = SunnahPrayer.query.filter_by(name=name).first_or_404()
    timings = calculate_prayer_times(
        DEFAULT_LOCATION["lat"],
        DEFAULT_LOCATION["lon"]
    )

    return {
        "name": sp.name,
        "is_ramadhan_only": sp.is_ramadhan_only,
        "time": calculate_sunnah_time(sp.name, timings)
    }, 200