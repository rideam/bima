from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from .db import get_db
from .functions import get_all_farmers

router = APIRouter()


@router.get("/farmers/", tags=["Function"])
def farmers(db: Session = Depends(get_db)):
    return get_all_farmers(db=db)
