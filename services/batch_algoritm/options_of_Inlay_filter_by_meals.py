# ------------------------------------------------------------
# פונקציה:
# בניית אפשרויות שיבוץ + סינון לפי זמינות מנות כבר בשלב היצירה
#
# לוגיקה:
# - מחשב קיבולת לכל מוקד
# - מחשב דרישה לכל נזקק
# - יוצר רק התאמות חוקיות:
#   * מוקד קיים
#   * נזקק קיים
#   * יש קיבולת > 0
#   * יש דרישה > 0
#   * דרישה <= קיבולת  (חובה)
# - מחשב מרחק בלבד עבור התאמות תקפות
# ------------------------------------------------------------

from datetime import date, datetime
from sqlalchemy.orm import Session

from models.recipient import Recipient
from models.distribution_center import DistributionCenter
from models.recipient_request import RecipientRequest
from models.DS_request import DS_Request
from services.googleMaps import distance_between_points


def dict_of_valid_divide_options(db: Session):

    today = date.today()

    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    # ---------------------------
    # Requests (today only)
    # ---------------------------
    ds_requests = db.query(DS_Request).filter(
        DS_Request.request_date.between(start_of_day, end_of_day)
    ).all()

    recipient_requests = db.query(RecipientRequest).filter(
        RecipientRequest.request_date.between(start_of_day, end_of_day)
    ).all()

    # ---------------------------
    # Preload tables
    # ---------------------------
    centers = {c.id: c for c in db.query(DistributionCenter).all()}
    recipients = {r.id: r for r in db.query(Recipient).all()}

    # ---------------------------
    # Capacity map (center -> meals)
    # ---------------------------
    ds_map = {}
    for d in ds_requests:
        cid = int(d.DistributionCenterID)
        ds_map[cid] = ds_map.get(cid, 0) + int(d.amount_of_meals)

    # ---------------------------
    # Demand map (recipient -> meals)
    # ---------------------------
    rec_map = {}
    for r in recipient_requests:
        rid = int(r.RecipientID)
        rec_map[rid] = rec_map.get(rid, 0) + int(r.amount_of_meals)

    results = []

    # ---------------------------
    # Build ONLY valid matches
    # ---------------------------
    for ds in ds_requests:

        center = centers.get(ds.DistributionCenterID)
        if not center:
            continue

        center_id = int(center.id)
        center_capacity = ds_map.get(center_id, 0)

        if center_capacity <= 0:
            continue

        c_lat = float(center.location_lat)
        c_lng = float(center.location_lng)

        for rr in recipient_requests:

            recipient = recipients.get(rr.RecipientID)
            if not recipient:
                continue

            recipient_id = int(recipient.id)
            recipient_demand = rec_map.get(recipient_id, 0)

            if recipient_demand <= 0:
                continue

            # חובה: סינון התאמה לוגית
            if recipient_demand > center_capacity:
                continue

            if recipient.location_lat is None or recipient.location_lng is None:
                continue

            distance = distance_between_points(
                c_lat,
                c_lng,
                float(recipient.location_lat),
                float(recipient.location_lng)
            )

            results.append({
                "center_id": center_id,
                "recipient_id": recipient_id,
                "distance_km": distance,
                "capacity": center_capacity,
                "demand": recipient_demand
            })

    return results