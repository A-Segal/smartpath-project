from sqlalchemy.orm import Session
from models.distribution_center import DistributionCenter

class DistributionCenterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_distribution_center(
        self,
        fname: str,
        lname: str,
        username: str,
        password: str,
        mail: str,
        phone: str,
        location_lat: float,
        location_lng: float,
        meal_count: int,
        request: str = None
    ) -> DistributionCenter:
        center = DistributionCenter(
            fname=fname,
            lname=lname,
            username=username,
            password=password,
            mail=mail,
            phone=phone,
            location_lat=location_lat,
            location_lng=location_lng,
            request=request
        )
        self.db.add(center)
        self.db.commit()
        self.db.refresh(center)
        return center

    def get_distribution_center(self, centerID: int) -> DistributionCenter | None:
        return self.db.query(DistributionCenter).filter(DistributionCenter.id == centerID).first()

    def get_distribution_center_by_password(self, password: str) -> DistributionCenter | None:
        return self.db.query(DistributionCenter).filter(DistributionCenter.password == password).first()
    def get_all_distribution_centers(self) -> list[DistributionCenter]:
        return self.db.query(DistributionCenter).all()

    def update_distribution_center(
        self,
        centerID: int,
        fname: str = None,
        lname: str = None,
        username: str = None,
        password: str = None,
        mail: str = None,
        phone: str = None,
        location_lat: float = None,
        location_lng: float = None,
        request: str = None
    ) -> DistributionCenter | None:
        center = self.get_distribution_center(centerID)
        if center:
            if fname is not None:
                center.fname = fname
            if lname is not None:
                center.lname = lname
            if username is not None:
                center.username = username
            if password is not None:
                center.password = password
            if mail is not None:
                center.mail = mail
            if phone is not None:
                center.phone = phone
            if location_lat is not None:
                center.location_lat = location_lat
            if location_lng is not None:
                center.location_lng = location_lng

            if request is not None:
                center.request = request
            self.db.commit()
            self.db.refresh(center)
        return center

    def delete_distribution_center(self, centerID: int) -> bool:
        center = self.get_distribution_center(centerID)
        if center:
            self.db.delete(center)
            self.db.commit()
            return True
        return False