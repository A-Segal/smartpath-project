from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime

Base = declarative_base()

class Volunteer(Base):
    __tablename__ = 'Volunteer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    mail = Column(String(100))
    phone = Column(String(20))
    username = Column(String(50), nullable=False)