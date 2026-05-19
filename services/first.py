from datetime import date
from sqlalchemy.orm import Session
from models.recipient import Recipient
from models.distribution_center import DistributionCenter
from models.recipient_request import RecipientRequest

from models.DS_request import DS_Request
from services.googleMaps import  distance_between_points

def calculate_distances_between_hubs_and_recipients(db: Session):
    """
    מחשבת מרחקים בין כל מוקדי חלוקה למקבלי הארוחות עם בקשות ליום הנוכחי.
    מחזירה רשימה של מילונים עם מזהה מוקד, מזהה מקבל, ובמרחק בקילומטרים.
    """

    today = date.today()

    # שליפה של כל הבקשות של המוקדים להיום
    ds_requests_today = db.query(DS_Request).filter(
        DS_Request.request_date == today
    ).all()

    # שליפה של כל בקשות המקבלים להיום
    recipient_requests_today = db.query(RecipientRequest).filter(
        Recipient.request_date == today
    ).all()

    results = []

    for ds_req in ds_requests_today:
        hub = db.query(DistributionCenter).filter(
            DistributionCenter.id == ds_req.DistributionCenterID
        ).first()

        for rec_req in recipient_requests_today:
            rec = db.query(Recipient).filter(
                Recipient.id == rec_req.RecipientID
            ).first()

            # חישוב מרחק בין מוקד למקבל
            distance_km = distance_between_points(
                float(hub.location_lat),
                float(hub.location_lng),
                float(rec.location_lat),
                float(rec.location_lng)
            )

            results.append({
                "hub_id": hub.id,
                "recipient_id": rec.id,
                "distance_km": distance_km
            })

    return results