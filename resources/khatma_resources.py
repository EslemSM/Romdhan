from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate
from datetime import date

from models.khatma import Khatma
from models.db import db
from schemas import KhatmaSchema

khatma_bp = Blueprint(
    "khatma_bp",
    __name__,
    description="Khatma (reading) sessions management"
)


khatma_schema = KhatmaSchema()
khatma_list_schema = KhatmaSchema(many=True)


class StartKhatmaSchema(Schema):
    # only allow expected unit values to make docs clearer
    unit = fields.Str(required=True, validate=validate.OneOf(["juz", "hizb"]))

class AddProgressSchema(Schema):
    amount = fields.Int(required=True)

class UpdateKhatmaSchema(Schema):
    unit = fields.Str(required=True, validate=validate.OneOf(["juz", "hizb"]))
    current_progress = fields.Int(required=True)


def compute_total_completed(current_progress, unit):
    limit = 30 if unit == "juz" else 60
    return (current_progress / limit) * 100 if limit > 0 else 0.0



@khatma_bp.route("/", methods=["GET"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.response(200, khatma_schema)
@jwt_required()
def get_current_khatma():
    """Get the current active khatma for the authenticated user."""
    user_id = get_jwt_identity()

    khatma = Khatma.query.filter_by(user_id=user_id, status="in_progress").first()
    if not khatma:
        abort(404, message="No active khatma")

    # attach computed field (OpenAPI will still show KhatmaSchema fields)
    khatma.total_completed = compute_total_completed(khatma.current_progress, khatma.unit)

    return khatma


@khatma_bp.route("/history", methods=["GET"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.response(200, khatma_list_schema)
@jwt_required()
def khatma_history():
    """Get completed khatma history for the authenticated user."""
    user_id = get_jwt_identity()
    history = Khatma.query.filter_by(user_id=user_id, status="completed").all()

    # populate computed percentages on each returned object (if your schema ignores unknown attrs,
    # you can return a list of dicts instead; this keeps model objects for consistency)
    for k in history:
        k.total_completed = compute_total_completed(k.current_progress, k.unit)
    return history


@khatma_bp.route("/", methods=["POST"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.arguments(StartKhatmaSchema, location="json")
@khatma_bp.response(201)  # returns message only
@jwt_required()
def start_khatma(data):
    """Start a new khatma for the authenticated user."""
    user_id = get_jwt_identity()

    # prevent multiple active khatmas
    active = Khatma.query.filter_by(user_id=user_id, status="in_progress").first()
    if active:
        abort(400, message="Active khatma already exists")

    khatma = Khatma(user_id=user_id, unit=data["unit"])
    db.session.add(khatma)
    db.session.commit()

    return {"message": "Khatma started"}


@khatma_bp.route("/<int:id>", methods=["PATCH"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.arguments(AddProgressSchema, location="json")
@khatma_bp.response(200)
@jwt_required()
def add_progress(data, id):
    """Add reading progress (amount) to an active khatma."""
    user_id = get_jwt_identity()

    khatma = Khatma.query.filter_by(id=id, user_id=user_id, status="in_progress").first_or_404()

    khatma.current_progress += data.get("amount", 0)
    khatma.total_completed = compute_total_completed(khatma.current_progress, khatma.unit)

    # Auto completion
    if khatma.total_completed >= 100:
        khatma.status = "completed"
        khatma.completion_date = date.today()
        khatma.completion_doua = (
           "اللَّهُمَّ وَفِّقْنَا فِي لَيْلَتِنَا هَذِهِ إِلَى مَا تُحِبُّ وَتَرْضَى، وَفِي كُلِّ أَعْمَالِنَا يَا حَيُّ يَا قَيُّومُ، اللَّهُمَّ اجْعَلْنَا لِكِتَابِكَ مِنَ التَّالِينَ وَعِنْدَ خِتْمِهِ مِنَ الْفَائِزِينَ، اللَّهُمَّ قَدْ خَتَمْنَا كِتَابَكَ وَلَذَّنَا بِجِنَابِكَ فَلَا تَطْرُدْنَا عَنْ بَابِكَ، فَإِنْ طَرَدْتَنَا فَإِنَّهُ لَا حَوْلَ لَنَا وَلَا قُوَّةَ إِلَّا بِكَ، لَا إِلَهَ إِلَّا اللَّهُ عَدَدَ مَا مَشَى فَوْقَ السَّمَوَاتِ وَالْأَرْضِينَ وَدَرَجَ، وَالْحَمْدُ لِلَّهِ الَّذِي بِيَدِهِ مَفَاتِيحُ الْفَرَجِ، يَا فَرَجَنَا إِذَا أُغْلِقَتِ الْأَبْوَابُ، وَيَا رَجَاءَنَا إِذَا انْقَطَعَتِ الْأَسْبَابُ، اللَّهُمَّ يَا سَامِعَ الصَّوْتِ وَيَا كَاسِيَ الْعِظَامِ لَحْمًا بَعْدَ الْمَوْتِ، نَسْأَلُكَ أَنْ تَجْعَلَنَا مِنْ أَهْلِ الْجَنَّةِ الَّذِينَ لَا خَوْفٌ عَلَيْهِمْ وَلَا هُمْ يَحْزَنُونَ، وَأَنْ تَعْتِقَ رِقَابَنَا مِنَ النَّارِ بِمَنِّكَ وَكَرَمِكَ يَا رَحْمَنُ، اللَّهُمَّ اغْفِرْ لِجَمِيعِ مُوتَى الْمُسْلِمِينَ الَّذِينَ شَهِدُوا لَكَ بِالْوَحْدَانِيَّةِ، وَلِنَبِيِّكَ بِالرِّسَالَةِ وَمَاتُوا عَلَى ذَلِكَ، اللَّهُمَّ اغْفِرْ لَهُمْ وَارْحَمْهُمْ وَعَافِهِمْ وَاعْفُ عَنْهُمْ وَأَكْرِمْ نُزُلَهُمْ وَوَسِّعْ مَدْخَلَهُمْ، وَاغْسِلْهُمْ بِالْمَاءِ وَالثَّلْجِ وَالْبَرْدِ، وَنَقِّهِمْ مِنَ الذُّنُوبِ وَالْخَطَايَا كَمَا يُنَقَّى الثَّوْبُ الْأَبْيَضُ مِنَ الدَّنَسِ، اللَّهُمَّ وَجَازِهِمْ بِالْحَسَنَاتِ إِحْسَانًا وَبِالسَّيِّئَاتِ عَفْوًا وَغُفْرَانًا، اللَّهُمَّ ارْحَمْنَا إِذَا صِرْنَا إِلَى مَا صَارُوا إِلَيْهِ، تَحْتَ الْجَنَادِلِ وَالْتُّرَابِ وَحْدَنَا، اللَّهُمَّ اجْعَلِ الْقُرْآنَ رَبِيعَ قُلُوبِنَا وَنُورَ صُدُورِنَا وَجَلَاءَ أَحْزَانِنَا… اللَّهُمَّ تَقَبَّلْ مِنَّا مَا قَرَأْنَا وَاجْعَلْنَا مِنَ الَّذِينَ يَسْمَعُونَ الْقَوْلَ فَيَتَّبِعُونَ أَحْسَنَهُ، وَصَلِّ اللَّهُمَّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلِّمْ تَسْلِيمًا كَثِيرًا"  
  
        )
        db.session.commit()
        return {"message": "Khatma completed", "completion_doua": khatma.completion_doua}

    db.session.commit()
    return {"message": "Progress updated"}


@khatma_bp.route("/<int:id>", methods=["PUT"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.arguments(UpdateKhatmaSchema, location="json")
@khatma_bp.response(200)
@jwt_required()
def update_progress(data, id):
    """Replace progress and/or unit for a khatma (PUT)."""
    user_id = get_jwt_identity()

    khatma = Khatma.query.filter_by(id=id, user_id=user_id).first_or_404()

    khatma.unit = data["unit"]
    khatma.current_progress = data["current_progress"]
    khatma.total_completed = compute_total_completed(khatma.current_progress, khatma.unit)

    # Auto completion
    if khatma.total_completed >= 100:
        khatma.status = "completed"
        khatma.completion_date = date.today()
        khatma.completion_doua = (
            "اللَّهُمَّ وَفِّقْنَا فِي لَيْلَتِنَا هَذِهِ إِلَى مَا تُحِبُّ وَتَرْضَى، وَفِي كُلِّ أَعْمَالِنَا يَا حَيُّ يَا قَيُّومُ، اللَّهُمَّ اجْعَلْنَا لِكِتَابِكَ مِنَ التَّالِينَ وَعِنْدَ خِتْمِهِ مِنَ الْفَائِزِينَ، اللَّهُمَّ قَدْ خَتَمْنَا كِتَابَكَ وَلَذَّنَا بِجِنَابِكَ فَلَا تَطْرُدْنَا عَنْ بَابِكَ، فَإِنْ طَرَدْتَنَا فَإِنَّهُ لَا حَوْلَ لَنَا وَلَا قُوَّةَ إِلَّا بِكَ، لَا إِلَهَ إِلَّا اللَّهُ عَدَدَ مَا مَشَى فَوْقَ السَّمَوَاتِ وَالْأَرْضِينَ وَدَرَجَ، وَالْحَمْدُ لِلَّهِ الَّذِي بِيَدِهِ مَفَاتِيحُ الْفَرَجِ، يَا فَرَجَنَا إِذَا أُغْلِقَتِ الْأَبْوَابُ، وَيَا رَجَاءَنَا إِذَا انْقَطَعَتِ الْأَسْبَابُ، اللَّهُمَّ يَا سَامِعَ الصَّوْتِ وَيَا كَاسِيَ الْعِظَامِ لَحْمًا بَعْدَ الْمَوْتِ، نَسْأَلُكَ أَنْ تَجْعَلَنَا مِنْ أَهْلِ الْجَنَّةِ الَّذِينَ لَا خَوْفٌ عَلَيْهِمْ وَلَا هُمْ يَحْزَنُونَ، وَأَنْ تَعْتِقَ رِقَابَنَا مِنَ النَّارِ بِمَنِّكَ وَكَرَمِكَ يَا رَحْمَنُ، اللَّهُمَّ اغْفِرْ لِجَمِيعِ مُوتَى الْمُسْلِمِينَ الَّذِينَ شَهِدُوا لَكَ بِالْوَحْدَانِيَّةِ، وَلِنَبِيِّكَ بِالرِّسَالَةِ وَمَاتُوا عَلَى ذَلِكَ، اللَّهُمَّ اغْفِرْ لَهُمْ وَارْحَمْهُمْ وَعَافِهِمْ وَاعْفُ عَنْهُمْ وَأَكْرِمْ نُزُلَهُمْ وَوَسِّعْ مَدْخَلَهُمْ، وَاغْسِلْهُمْ بِالْمَاءِ وَالثَّلْجِ وَالْبَرْدِ، وَنَقِّهِمْ مِنَ الذُّنُوبِ وَالْخَطَايَا كَمَا يُنَقَّى الثَّوْبُ الْأَبْيَضُ مِنَ الدَّنَسِ، اللَّهُمَّ وَجَازِهِمْ بِالْحَسَنَاتِ إِحْسَانًا وَبِالسَّيِّئَاتِ عَفْوًا وَغُفْرَانًا، اللَّهُمَّ ارْحَمْنَا إِذَا صِرْنَا إِلَى مَا صَارُوا إِلَيْهِ، تَحْتَ الْجَنَادِلِ وَالْتُّرَابِ وَحْدَنَا، اللَّهُمَّ اجْعَلِ الْقُرْآنَ رَبِيعَ قُلُوبِنَا وَنُورَ صُدُورِنَا وَجَلَاءَ أَحْزَانِنَا… اللَّهُمَّ تَقَبَّلْ مِنَّا مَا قَرَأْنَا وَاجْعَلْنَا مِنَ الَّذِينَ يَسْمَعُونَ الْقَوْلَ فَيَتَّبِعُونَ أَحْسَنَهُ، وَصَلِّ اللَّهُمَّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلِّمْ تَسْلِيمًا كَثِيرًا"  
  # truncated for readability; keep your original text
        )
        db.session.commit()
        return {"message": "Khatma completed", "completion_doua": khatma.completion_doua}

    db.session.commit()
    return {"message": "Progress replaced"}


@khatma_bp.route("/<int:id>", methods=["DELETE"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.response(200)
@jwt_required()
def delete_khatma(id):
    """Delete a khatma session (only by owner)."""
    user_id = get_jwt_identity()
    khatma = Khatma.query.filter_by(id=id, user_id=user_id).first_or_404()

    db.session.delete(khatma)
    db.session.commit()
    return {"message": "Khatma deleted"}


@khatma_bp.route("/history", methods=["DELETE"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.response(200)
@jwt_required()
def delete_khatma_history():
    """Delete all completed khatma history for the user."""
    user_id = get_jwt_identity()
    deleted_count = Khatma.query.filter_by(user_id=user_id, status="completed").delete()
    db.session.commit()
    return {"message": f"History deleted ({deleted_count} khatmas removed)"}


@khatma_bp.route("/history/<int:id>", methods=["DELETE"])
@khatma_bp.doc(security=[{"bearerAuth": []}])
@khatma_bp.response(200)
@jwt_required()
def delete_single_khatma_history(id):
    """Delete a single completed khatma from history."""
    user_id = get_jwt_identity()
    khatma = Khatma.query.filter_by(id=id, user_id=user_id, status="completed").first_or_404()
    db.session.delete(khatma)
    db.session.commit()
    return {"message": "History item deleted"}
