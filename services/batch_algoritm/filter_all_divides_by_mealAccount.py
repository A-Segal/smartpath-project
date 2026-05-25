#הפונקציה מסננת את המילון שהתקבל
#כך שמחזירה מילון מסונן לפי כמות מנות


from sqlalchemy.orm import Session
from models.recipient_request import RecipientRequest
from models.DS_request import DS_Request
from services.batch_algoritm.dict_of_all_options_divides import dict_of_all_options_divides


def filter_all_divides_by_mealAccount(db: Session):
    all_options = dict_of_all_options_divides(db)
    ds_requests = db.query(DS_Request).all()
    rec_requests = db.query(RecipientRequest).all()

    # יצירת מאפינגים
    ds_map = {}
    rec_map = {}

    for d in ds_requests:
        cid = int(d.DistributionCenterID)
        ds_map[cid] = ds_map.get(cid, 0) + int(d.amount_of_meals)

    for r in rec_requests:
        rid = int(r.RecipientID)
        rec_map[rid] = rec_map.get(rid, 0) + int(r.amount_of_meals)

    filtered = []
    for opt in all_options:

        center_id = opt.get("distribution_center_id")
        recipient_id = opt.get("recipient_id")

        if center_id is None or recipient_id is None:
            continue

        center_id = int(center_id)
        recipient_id = int(recipient_id)

        center_meals = ds_map.get(center_id, 0)
        recipient_meals = rec_map.get(recipient_id, 0)

        if center_meals < recipient_meals:
            continue

        filtered.append({
            "center_id": center_id,
            "recipient_id": recipient_id,
            "distance_km": opt["distance_km"],
            "capacity": center_meals,
            "demand": recipient_meals
        })
    return filtered