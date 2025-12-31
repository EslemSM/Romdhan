from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.khatma import Khatma
from models.db import db
from schemas import KhatmaSchema
from datetime import date

khatma_bp = Blueprint('khatma', __name__)

schema = KhatmaSchema()
list_schema = KhatmaSchema(many=True)

def compute_total_completed(current_progress, unit):
    limit = 30 if unit == "juz" else 60
    return (current_progress / limit) * 100 if limit > 0 else 0.0


# ✅ GET current active khatma
@khatma_bp.route("/", methods=["GET"])
@jwt_required()
def get_current_khatma():
    user_id = get_jwt_identity()

    khatma = Khatma.query.filter_by(
        user_id=user_id, status="in_progress"
    ).first()

    if not khatma:
        return {"message": "No active khatma"}, 404
    
    total_completed = compute_total_completed(khatma.current_progress, khatma.unit)

    return {
        "id": khatma.id,
        "unit": khatma.unit,
        "current_progress": khatma.current_progress,
        "total_completed": total_completed
    }, 200


# ✅ GET khatma history (completed)
@khatma_bp.route("/history", methods=["GET"])
@jwt_required()
def khatma_history():
    user_id = get_jwt_identity()
    history = Khatma.query.filter_by(
        user_id=user_id, status="completed"
    ).all()

    return [
        {
            "id": k.id,
            "unit": k.unit,
            "total_completed": compute_total_completed(k.current_progress, k.unit),  # Now a percentage
            "completion_date": k.completion_date
        } for k in history
    ], 200

# ✅ POST start new khatma
@khatma_bp.route("/", methods=["POST"])
@jwt_required()
def start_khatma():
    user_id = get_jwt_identity()
    data = request.get_json()

    # prevent multiple active khatmas
    active = Khatma.query.filter_by(
        user_id=user_id, status="in_progress"
    ).first()
    if active:
        return {"error": "Active khatma already exists"}, 400

    khatma = Khatma(
        user_id=user_id,
        unit=data["unit"]
    )
    db.session.add(khatma)
    db.session.commit()

    return {"message": "Khatma started"}, 201

# ✅ PATCH add reading session
@khatma_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def add_progress(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    khatma = Khatma.query.filter_by(
        id=id, user_id=user_id, status="in_progress"
    ).first_or_404()

    khatma.current_progress += data.get("amount", 0)
    khatma.total_completed = compute_total_completed(khatma.current_progress, khatma.unit)

    # Auto completion: check if percentage >= 100
    if khatma.total_completed >= 100:
        khatma.status = "completed"
        khatma.completion_date = date.today()
        khatma.completion_doua = "اللَّهُمَّ وَفِّقْنَا فِي لَيْلَتِنَا هَذِهِ إِلَى مَا تُحِبُّ وَتَرْضَى، وَفِي كُلِّ أَعْمَالِنَا يَا حَيُّ يَا قَيُّومُ، اللَّهُمَّ اجْعَلْنَا لِكِتَابِكَ مِنَ التَّالِينَ وَعِنْدَ خِتْمِهِ مِنَ الْفَائِزِينَ، اللَّهُمَّ قَدْ خَتَمْنَا كِتَابَكَ وَلَذَّنَا بِجِنَابِكَ فَلَا تَطْرُدْنَا عَنْ بَابِكَ، فَإِنْ طَرَدْتَنَا فَإِنَّهُ لَا حَوْلَ لَنَا وَلَا قُوَّةَ إِلَّا بِكَ، لَا إِلَهَ إِلَّا اللَّهُ عَدَدَ مَا مَشَى فَوْقَ السَّمَوَاتِ وَالْأَرْضِينَ وَدَرَجَ، وَالْحَمْدُ لِلَّهِ الَّذِي بِيَدِهِ مَفَاتِيحُ الْفَرَجِ، يَا فَرَجَنَا إِذَا أُغْلِقَتِ الْأَبْوَابُ، وَيَا رَجَاءَنَا إِذَا انْقَطَعَتِ الْأَسْبَابُ، اللَّهُمَّ يَا سَامِعَ الصَّوْتِ وَيَا كَاسِيَ الْعِظَامِ لَحْمًا بَعْدَ الْمَوْتِ، نَسْأَلُكَ أَنْ تَجْعَلَنَا مِنْ أَهْلِ الْجَنَّةِ الَّذِينَ لَا خَوْفٌ عَلَيْهِمْ وَلَا هُمْ يَحْزَنُونَ، وَأَنْ تَعْتِقَ رِقَابَنَا مِنَ النَّارِ بِمَنِّكَ وَكَرَمِكَ يَا رَحْمَنُ، اللَّهُمَّ اغْفِرْ لِجَمِيعِ مُوتَى الْمُسْلِمِينَ الَّذِينَ شَهِدُوا لَكَ بِالْوَحْدَانِيَّةِ، وَلِنَبِيِّكَ بِالرِّسَالَةِ وَمَاتُوا عَلَى ذَلِكَ، اللَّهُمَّ اغْفِرْ لَهُمْ وَارْحَمْهُمْ وَعَافِهِمْ وَاعْفُ عَنْهُمْ وَأَكْرِمْ نُزُلَهُمْ وَوَسِّعْ مَدْخَلَهُمْ، وَاغْسِلْهُمْ بِالْمَاءِ وَالثَّلْجِ وَالْبَرْدِ، وَنَقِّهِمْ مِنَ الذُّنُوبِ وَالْخَطَايَا كَمَا يُنَقَّى الثَّوْبُ الْأَبْيَضُ مِنَ الدَّنَسِ، اللَّهُمَّ وَجَازِهِمْ بِالْحَسَنَاتِ إِحْسَانًا وَبِالسَّيِّئَاتِ عَفْوًا وَغُفْرَانًا، اللَّهُمَّ ارْحَمْنَا إِذَا صِرْنَا إِلَى مَا صَارُوا إِلَيْهِ، تَحْتَ الْجَنَادِلِ وَالْتُّرَابِ وَحْدَنَا، اللَّهُمَّ اجْعَلِ الْقُرْآنَ رَبِيعَ قُلُوبِنَا وَنُورَ صُدُورِنَا وَجَلَاءَ أَحْزَانِنَا… اللَّهُمَّ تَقَبَّلْ مِنَّا مَا قَرَأْنَا وَاجْعَلْنَا مِنَ الَّذِينَ يَسْمَعُونَ الْقَوْلَ فَيَتَّبِعُونَ أَحْسَنَهُ، وَصَلِّ اللَّهُمَّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلِّمْ تَسْلِيمًا كَثِيرًا"  

        db.session.commit()
        return {
            "message": "Khatma completed",
            "completion_doua": khatma.completion_doua
        }, 200

    db.session.commit()
    return {"message": "Progress updated"}, 200

    
# ✅ PUT replace progress
@khatma_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_progress(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    khatma = Khatma.query.filter_by(
        id=id, user_id=user_id
    ).first_or_404()

    # Update unit and current_progress
    khatma.unit = data["unit"]
    khatma.current_progress = data["current_progress"]
    # Recompute total_completed as percentage based on new unit/current_progress
    khatma.total_completed = compute_total_completed(khatma.current_progress, khatma.unit)

    # Auto completion: check if percentage >= 100
    if khatma.total_completed >= 100:
        khatma.status = "completed"
        khatma.completion_date = date.today()
        khatma.completion_doua = "اللَّهُمَّ وَفِّقْنَا فِي لَيْلَتِنَا هَذِهِ إِلَى مَا تُحِبُّ وَتَرْضَى، وَفِي كُلِّ أَعْمَالِنَا يَا حَيُّ يَا قَيُّومُ، اللَّهُمَّ اجْعَلْنَا لِكِتَابِكَ مِنَ التَّالِينَ وَعِنْدَ خِتْمِهِ مِنَ الْفَائِزِينَ، اللَّهُمَّ قَدْ خَتَمْنَا كِتَابَكَ وَلَذَّنَا بِجِنَابِكَ فَلَا تَطْرُدْنَا عَنْ بَابِكَ، فَإِنْ طَرَدْتَنَا فَإِنَّهُ لَا حَوْلَ لَنَا وَلَا قُوَّةَ إِلَّا بِكَ، لَا إِلَهَ إِلَّا اللَّهُ عَدَدَ مَا مَشَى فَوْقَ السَّمَوَاتِ وَالْأَرْضِينَ وَدَرَجَ، وَالْحَمْدُ لِلَّهِ الَّذِي بِيَدِهِ مَفَاتِيحُ الْفَرَجِ، يَا فَرَجَنَا إِذَا أُغْلِقَتِ الْأَبْوَابُ، وَيَا رَجَاءَنَا إِذَا انْقَطَعَتِ الْأَسْبَابُ، اللَّهُمَّ يَا سَامِعَ الصَّوْتِ وَيَا كَاسِيَ الْعِظَامِ لَحْمًا بَعْدَ الْمَوْتِ، نَسْأَلُكَ أَنْ تَجْعَلَنَا مِنْ أَهْلِ الْجَنَّةِ الَّذِينَ لَا خَوْفٌ عَلَيْهِمْ وَلَا هُمْ يَحْزَنُونَ، وَأَنْ تَعْتِقَ رِقَابَنَا مِنَ النَّارِ بِمَنِّكَ وَكَرَمِكَ يَا رَحْمَنُ، اللَّهُمَّ اغْفِرْ لِجَمِيعِ مُوتَى الْمُسْلِمِينَ الَّذِينَ شَهِدُوا لَكَ بِالْوَحْدَانِيَّةِ، وَلِنَبِيِّكَ بِالرِّسَالَةِ وَمَاتُوا عَلَى ذَلِكَ، اللَّهُمَّ اغْفِرْ لَهُمْ وَارْحَمْهُمْ وَعَافِهِمْ وَاعْفُ عَنْهُمْ وَأَكْرِمْ نُزُلَهُمْ وَوَسِّعْ مَدْخَلَهُمْ، وَاغْسِلْهُمْ بِالْمَاءِ وَالثَّلْجِ وَالْبَرْدِ، وَنَقِّهِمْ مِنَ الذُّنُوبِ وَالْخَطَايَا كَمَا يُنَقَّى الثَّوْبُ الْأَبْيَضُ مِنَ الدَّنَسِ، اللَّهُمَّ وَجَازِهِمْ بِالْحَسَنَاتِ إِحْسَانًا وَبِالسَّيِّئَاتِ عَفْوًا وَغُفْرَانًا، اللَّهُمَّ ارْحَمْنَا إِذَا صِرْنَا إِلَى مَا صَارُوا إِلَيْهِ، تَحْتَ الْجَنَادِلِ وَالْتُّرَابِ وَحْدَنَا، اللَّهُمَّ اجْعَلِ الْقُرْآنَ رَبِيعَ قُلُوبِنَا وَنُورَ صُدُورِنَا وَجَلَاءَ أَحْزَانِنَا… اللَّهُمَّ تَقَبَّلْ مِنَّا مَا قَرَأْنَا وَاجْعَلْنَا مِنَ الَّذِينَ يَسْمَعُونَ الْقَوْلَ فَيَتَّبِعُونَ أَحْسَنَهُ، وَصَلِّ اللَّهُمَّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلِّمْ تَسْلِيمًا كَثِيرًا" 

        db.session.commit()
        return {
            "message": "Khatma completed",
            "completion_doua": khatma.completion_doua
        }, 200

    db.session.commit()
    return {"message": "Progress replaced"}, 200


# ✅ DELETE session
@khatma_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_khatma(id):
    user_id = get_jwt_identity()
    khatma = Khatma.query.filter_by(
        id=id, user_id=user_id
    ).first_or_404()

    db.session.delete(khatma)
    db.session.commit()
    return {"message": "Khatma deleted"}, 200

# ✅ DELETE khatma history 
@khatma_bp.route("/history", methods=["DELETE"])
@jwt_required()
def delete_khatma_history():
    user_id = get_jwt_identity()
    
    # Delete all completed khatmas for this user
    deleted_count = Khatma.query.filter_by(
        user_id=user_id, status="completed"
    ).delete()
    
    db.session.commit()
    
    return {"message": f"History deleted ({deleted_count} khatmas removed)"}, 200


# ... (existing code remains unchanged)

# ✅ DELETE a single khatma from history (by ID, only if completed)
@khatma_bp.route("/history/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_single_khatma_history(id):
    user_id = get_jwt_identity()
    
    # Find and delete only if it's completed and belongs to the user
    khatma = Khatma.query.filter_by(
        id=id, user_id=user_id, status="completed"
    ).first_or_404()
    
    db.session.delete(khatma)
    db.session.commit()
    
    return {"message": "History item deleted"}, 200

# ... (rest of the file remains unchanged)
