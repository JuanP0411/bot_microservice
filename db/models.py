from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship

from .database import Base

class User(Base) :
    __tablename__ = "users"

    id= Column(Integer,primary_key=True)
    username = Column(String, unique=True)
    password_hash= Column(String)
    session_data=Column(JSON)
    role = Column(String)

    formulas = relationship("Formula",  back_populates="userf")


class Formula(Base):

    __tablename__ = "user_signals"

    id = Column(Integer,primary_key=True)
    username = Column(String,ForeignKey('users.username'))
    signal_name = Column(String)
    formula = Column(String)
    threshold = Column(Float)
    invert = Column(Boolean)
    graph_type = Column(String(255))
    graph_detail = Column(String)
    widget_data = Column(JSON)

    userf = relationship("User", back_populates="formulas")
