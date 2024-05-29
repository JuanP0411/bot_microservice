from typing import List
from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit : int = 100)-> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()