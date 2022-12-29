from sqlalchemy.orm import Session
from sqlalchemy.sql import extract, label, func

from . import models


def get_all_farmers(db: Session):
    records = db.query(models.Farmer.firstname.label('firstName'),
                       models.Farmer.lastname.label('surname')) \
        .all()
    return records